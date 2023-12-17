import openai

with open("../data/atomic_sentences_p.txt","r",encoding='utf-8') as f:
    sentence1 = f.readlines()
    sentence1 = [line.strip() for line in sentence1]

with open("../data/atomic_sentences_q.txt","r",encoding='utf-8') as f:
    sentence2 = f.readlines()
    sentence2 = [line.strip() for line in sentence2]

pattern6_list = []

for i in sentence1:
    for j in sentence2:
        pattern6 = "Suppose that \"" + i[:len(
            i) - 1] + ", or " + j + "\" and \"" + i + "\" are true. What is the conclusion? (If there is a conclusion, you only response the conclusion without any analysis. Otherwise, you should only answer \"there is no conclusion\")"
        pattern6_list.append(pattern6)

openai.api_key = '' #The API key provided by openAI
pattern6_results = []
import time

i = 0
while i < len(pattern6_list):
    pattern6_dict = {}
    try:
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[
                {"role": "assistant", "content": pattern6_list[i]}
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
        pattern6_dict['question'] = pattern6_list[i]
        pattern6_dict['response'] = result
        pattern6_results.append(pattern6_dict)
        print('the {}-th turn:'.format(i), pattern6_dict)
        time.sleep(10)
        i += 1

import json
with open("FDSR.json","w",encoding = "utf-8") as f:
    json_str = json.dumps(pattern6_results)
    f.write(json_str)

