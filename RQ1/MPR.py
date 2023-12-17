import openai

with open("../data/atomic_sentences_p.txt","r",encoding='utf-8') as f:
    sentence1 = f.readlines()
    sentence1 = [line.strip() for line in sentence1]

with open("../data/atomic_sentences_q.txt","r",encoding='utf-8') as f:
    sentence2 = f.readlines()
    sentence2 = [line.strip() for line in sentence2]

pattern1_list = []

for i in sentence1:
    for j in sentence2:
        pattern1 = "Suppose that \"If " + i[:len(i)-1] + ", then " + j + "\" and \"" + i + "\" are true. What is the conclusion? (If there is a conclusion, you only response the conclusion without any analysis. Otherwise, you should only answer \"there is no conclusion\")"
        pattern1_list.append(pattern1)

openai.api_key = '' #The API key provided by openAI
pattern1_results = []
import time

i = 0
while i < len(pattern1_list):
    pattern1_dict = {}
    try:
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[
                {"role": "user", "content": pattern1_list[i]}
            ],
            temperature = 1.0
        )
    except:
        print('warning!!!!!!')
        continue
    else:
        result = ''
        for choice in response.choices:
            result += choice.message.content
        pattern1_dict['question'] = pattern1_list[i]
        pattern1_dict['response'] = result
        pattern1_results.append(pattern1_dict)
        print('the {}-th turn:'.format(i), pattern1_dict)
        time.sleep(10)
        i += 1

import json
with open("MPR.json","w",encoding = "utf-8") as f:
    json_str = json.dumps(pattern1_results)
    f.write(json_str)

