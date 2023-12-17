import openai

with open("../data/atomic_sentences_p.txt","r",encoding='utf-8') as f:
    sentence1 = f.readlines()
    sentence1 = [line.strip() for line in sentence1]

with open("../data/atomic_sentences_q.txt","r",encoding='utf-8') as f:
    sentence2 = f.readlines()
    sentence2 = [line.strip() for line in sentence2]

pattern4_list = []

for i in sentence1:
    for j in sentence2:
        pattern4 = "Suppose that \"If " + i[:len(
            i) - 1] + ", then " + j + "\" and \"" + i[0] + ' do not' + i[
                                                                       1:] + "\" are true. What is the conclusion? (If there is a conclusion, you only response the conclusion without any analysis. Otherwise, you should only answer \"there is no conclusion\")"
        pattern4_list.append(pattern4)

openai.api_key = '' #The API key provided by openAI
pattern4_results = []
import time

i = 0
while i < len(pattern4_list):
    pattern4_dict = {}
    try:
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[
                {"role": "assistant", "content": pattern4_list[i]}
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
        pattern4_dict['question'] = pattern4_list[i]
        pattern4_dict['response'] = result
        pattern4_results.append(pattern4_dict)
        print('the {}-th turn:'.format(i), pattern4_dict)
        time.sleep(10)
        i += 1

import json
with open("FMTR.json","w",encoding = "utf-8") as f:
    json_str = json.dumps(pattern4_results)
    f.write(json_str)

