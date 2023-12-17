import json
from typing import Any, List
import chatproto
import os

from chatproto.conversation.history import ConversationHistory
from chatproto.conversation.models.llama import llama
from chatproto.conversation.models.openbuddy import openbuddy
from chatproto.conversation.models.baichuan2 import baichuan2
import torch
import tqdm
import numpy as np

def batched(data: List[Any], batch_size: int) -> List[List[Any]]:
    batches = []
    for i in range(0, len(data), batch_size):
        batch = data[i:i+batch_size]
        batches.append(batch)
    return batches

def load_dataset(path: str, conv):
    print("loading dataset")
    with open(path, "r", encoding="utf-8") as f:
        objs = json.loads(f.read())
    
    for obj in tqdm.tqdm(objs):
        conversations = obj["conversations"]
        if len(conversations) == 0:
            continue
        messages = []
        for i, msg in enumerate(conversations):
            if i % 2 == 0:
                messages.append((conv.roles[0], msg["value"]))
            else:
                messages.append((conv.roles[1], msg["value"]))
        
        # construct
        history = ConversationHistory(
            "",
            messages=messages,
            offset=0,
            settings=conv
        )
        history_out = history.get_prompt()
        obj["all_prompt"] = history_out

        # construct
        history = ConversationHistory(
            "",
            messages=messages[:-1] + [(conv.roles[1], None)],
            offset=0,
            settings=conv
        )
        history_out = history.get_prompt()
        obj["prompt"] = history_out

    return objs

# , eos_token_id=tokenizer.eos_token_id
def inference_single(model, tokenizer, input: str, max_new_tokens=256, temperature=0, eos_token_id=None, device="cuda"):
    do_sample = temperature != 0
    if do_sample == False:
        temperature_rs = 1.0
    else:
        temperature_rs = temperature
    input_ids = tokenizer([input], return_tensors="pt", padding='longest', max_length=2048, truncation=True)["input_ids"].to(device)
    outputs_ids = model.generate(
        inputs=input_ids,
        max_new_tokens=max_new_tokens,
        pad_token_id=tokenizer.eos_token_id,
        num_beams=1,
        do_sample=do_sample,
        temperature=temperature_rs,
        top_p=1.0,
        eos_token_id=eos_token_id
    )
    outputs = tokenizer.batch_decode(outputs_ids, skip_special_tokens=True)
    output_text = outputs[0]
    return output_text

def inference_batch(model, tokenizer, inputs: List[str], max_new_tokens=256, temperature=0, eos_token_id=None, device="cuda"):
    do_sample = temperature != 0
    if do_sample == False:
        temperature_rs = 1.0
    else:
        temperature_rs = temperature
    input_ids = tokenizer(inputs, return_tensors="pt", padding='longest', max_length=2048, truncation=True)["input_ids"].to(device)
    outputs_ids = model.generate(
        inputs=input_ids,
        max_new_tokens=max_new_tokens,
        pad_token_id=tokenizer.eos_token_id,
        num_beams=1,
        do_sample=do_sample,
        temperature=temperature_rs,
        top_p=1.0,
        eos_token_id=eos_token_id
    )
    outputs = tokenizer.batch_decode(outputs_ids, skip_special_tokens=True)
    return outputs


from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModelForCausalLM, get_peft_config

"""
Llama-2-13b-chat-hf
openbuddy-llama2-13b-v8.1-fp16
Baichuan2-13B-Chat
"""
import argparse

parser = argparse.ArgumentParser(description='模型名称和split参数设置')
parser.add_argument('--model', type=str, help='模型名称')
parser.add_argument('--split', default="valid", type=str, help='数据集的分割方式')
parser.add_argument('--temp', default=0, type=float, help='温度')
parser.add_argument('--device', default=0, type=int, help='设备')
args = parser.parse_args()
print(args)

model_name = args.model
if "openbuddy" in model_name:
    conv = openbuddy
elif "Llama-2" in model_name:
    conv = llama
elif "Baichuan2" in model_name:
    conv = baichuan2
else:
    raise Exception()
split = args.split

temperature = args.temp
device = f"cuda:{args.device}"
batch_size = 1

model_id = f"../models/{model_name}"
model = AutoModelForCausalLM.from_pretrained(model_id, torch_dtype=torch.float16, trust_remote_code=True)
model.to(device)
tokenizer = AutoTokenizer.from_pretrained(model_id, trust_remote_code=True)
# tokenizer.padding_side = 'left'
if "openbuddy" in model_name:
    tokenizer.pad_token = tokenizer.bos_token
    tokenizer.padding_side = "left"
if "Llama-2" in model_name:
    tokenizer.pad_token = tokenizer.bos_token
    tokenizer.padding_side = "left"

dataset = load_dataset(f"{split}_set.json", conv)
# dataset = load_dataset("valid_set.json", conv)[:64]

if "openbuddy" in model_name:
    eos_token_id = tokenizer.eos_token_id
else:
    eos_token_id = None

for step in range(100, 2000, 100):
    save_file = f"checkpoints_predict_{split}_{model_name}_temp{temperature}/out_{step}.json"
    dir_path = os.path.dirname(save_file)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path, exist_ok=True)
    
    if os.path.exists(save_file):
        continue

    peft_model_id = f"./checkpoints_{model_name}/checkpoint-{step}"
    peft_model = PeftModelForCausalLM.from_pretrained(model, peft_model_id)

    # merged_model = peft_model.merge_and_unload()
    # merged_model.save_pretrained("out-checkpoint-4000")

    dataset_len = [-len(data["prompt"]) for data in dataset]
    sort_indices = np.argsort(dataset_len)
    sort_dataset = [dataset[idx] for idx in sort_indices]

    with torch.inference_mode(True):
        sort_out_dataset = []
        for batch in tqdm.tqdm(batched(sort_dataset, batch_size)):
            prompts = [item["prompt"] for item in batch]
            out = inference_batch(peft_model, tokenizer, prompts, temperature=temperature, eos_token_id=eos_token_id, device=device)
            answers = [o[len(prompts[i]):] for i, o in enumerate(out)]

            for i, data in enumerate(batch):
                data["answer"] = answers[i]
                sort_out_dataset.append(data)
        
        out_dataset = [None] * len(sort_out_dataset)
        for i, idx in enumerate(sort_indices):
            out_dataset[idx] = sort_out_dataset[i]

    with open(save_file, "w", encoding="utf-8") as f:
        f.write(json.dumps(out_dataset, ensure_ascii=False))