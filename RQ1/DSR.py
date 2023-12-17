import openai

with open("../data/atomic_sentences_p.txt","r",encoding='utf-8') as f:
    sentence1 = f.readlines()
    sentence1 = [line.strip() for line in sentence1]
print(sentence1)

with open("../data/atomic_sentences_q.txt","r",encoding='utf-8') as f:
    sentence2 = f.readlines()
    sentence2 = [line.strip() for line in sentence2]

pattern5_list = []

for i in sentence1:
    for j in sentence2:
        pattern5 = "Suppose that \"" + i[:len(i) - 1] + ", or " + j + "\" and \"" + i[0] + ' do not' + i[
                                                                                                       1:] + "\" are true. What is the conclusion? (If there is a conclusion, you only response the conclusion without any analysis. Otherwise, you should only answer \"there is no conclusion\")"
        pattern5_list.append(pattern5)

openai.api_key = '' #The API key provided by openAI
pattern5_results = []
import time

i = 0
while i < len(pattern5_list):
    pattern5_dict = {}
    try:
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[
                {"role": "assistant", "content": pattern5_list[i]}
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
        pattern5_dict['question'] = pattern5_list[i]
        pattern5_dict['response'] = result
        pattern5_results.append(pattern5_dict)
        print('the {}-th turn:'.format(i), pattern5_dict)
        time.sleep(10)
        i += 1

import json
with open("DSR.json","w",encoding = "utf-8") as f:
    json_str = json.dumps(pattern5_results)
    f.write(json_str)

