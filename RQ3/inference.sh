

python load_peft_and_inference.py --model Llama-2-13b-chat-hf --temp 1 --device 0 --split valid
python load_peft_and_inference.py --model Llama-2-13b-chat-hf --temp 0.7 --device 0 --split valid
python load_peft_and_inference.py --model Llama-2-13b-chat-hf --temp 0 --device 0 --split valid

# python load_peft_and_inference.py --model Llama-2-13b-chat-hf --temp 1 --device 0 --split test
# python load_peft_and_inference.py --model Llama-2-13b-chat-hf --temp 0.7 --device 0 --split test
# python load_peft_and_inference.py --model Llama-2-13b-chat-hf --temp 0 --device 0 --split test


python load_peft_and_inference.py --model Baichuan2-13B-Chat --temp 1 --device 0 --split valid
python load_peft_and_inference.py --model Baichuan2-13B-Chat --temp 0.7 --device 0 --split valid
python load_peft_and_inference.py --model Baichuan2-13B-Chat --temp 0 --device 0 --split valid

# python load_peft_and_inference.py --model Baichuan2-13B-Chat --temp 1 --device 0 --split test
# python load_peft_and_inference.py --model Baichuan2-13B-Chat --temp 0.7 --device 0 --split test
# python load_peft_and_inference.py --model Baichuan2-13B-Chat --temp 0 --device 0 --split test


python load_peft_and_inference.py --model openbuddy-llama2-13b-v8.1-fp16 --temp 1 --device 1 --split valid
python load_peft_and_inference.py --model openbuddy-llama2-13b-v8.1-fp16 --temp 0.7 --device 1 --split valid
python load_peft_and_inference.py --model openbuddy-llama2-13b-v8.1-fp16 --temp 0 --device 1 --split valid

# python load_peft_and_inference.py --model openbuddy-llama2-13b-v8.1-fp16 --temp 1 --device 1 --split test
# python load_peft_and_inference.py --model openbuddy-llama2-13b-v8.1-fp16 --temp 0.7 --device 1 --split test
# python load_peft_and_inference.py --model openbuddy-llama2-13b-v8.1-fp16 --temp 0 --device 1 --split test