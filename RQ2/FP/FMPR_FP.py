import openai
from sentence_transformers import SentenceTransformer, util
model = SentenceTransformer('paraphrase-mpnet-base-v2')

with open("../../data/atomic_sentences_p.txt","r",encoding='utf-8') as f:
    sentence1 = f.readlines()
    sentence1 = [line.strip() for line in sentence1]

with open("../../data/atomic_sentences_q.txt","r",encoding='utf-8') as f:
    sentence2 = f.readlines()
    sentence2 = [line.strip() for line in sentence2]

pattern2_list = []
ground_truth = []

for i in sentence1:
    for j in sentence2:
        pattern2 = "Suppose that \"If " + i[:len(
            i) - 1] + ", then " + j + "\" and \"" + j + "\" are true. What is the conclusion? If there is a conclusion, you only response the conclusion without any analysis. Otherwise, you should only answer \"there is no conclusion\""
        pattern2_list.append(pattern2)
        ground_truth.append('There is no conclusion.')

openai.api_key = '' #The API key provided by openAI
pattern1_results = []

import time

i = 0
while i < len(pattern2_list):
    pattern1_dict = {}
    if i % 10 == 0:
        messages = []
        m = 1
        content = ''
    if m < 6:
        content += str(m) + '. Question: ' + pattern2_list[i] + '\nExplanation: Given \"If p, then q\" and \"q\" are true, where p and q represent statements, we can not infer whether p is true, so there is no conclusion. \nAnswer: there is no conclusion.\n'
        m += 1
        i += 1
        continue
    if m == 6:
        content += str(m) + '. Question: ' + pattern2_list[
            i] + '\nExplanation: Given \"If p, then q\" and \"q\" are true, where p and q represent statements, we can not infer whether p is true, so there is no conclusion. \nAnswer: there is no conclusion.\n'
        content += 'Next, I will ask you some logical reasoning questions. Here are some examples. Please answer the following questions according to the examples and you should only tell me the content in \"Answer\".'
        message = {"role": "user", "content": content}
    if m >= 7:
        message = {"role": "user", "content": pattern2_list[i]}
    messages.append(message)
    try:
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=messages,
            temperature = 1.0
        )
    except:
        k = i % 10 - 5
        i = i - i % 10
        print("warning!!!!")
        pattern1_results = pattern1_results[:len(pattern1_results)-k]

    else:
        result = ''
        for choice in response.choices:
            result += choice.message.content
        response = {"role": "assistant", "content": result}
        messages.append(response)
        pattern1_dict['question'] = pattern2_list[i]
        pattern1_dict['response'] = result
        print('the {}-th turn:'.format(i), pattern1_dict)
        time.sleep(10)
        pattern1_results.append(pattern1_dict)
        i += 1
        m += 1

import json
with open("FMPR.json","w",encoding = "utf-8") as f:
    json_str = json.dumps(pattern1_results)
    f.write(json_str)

