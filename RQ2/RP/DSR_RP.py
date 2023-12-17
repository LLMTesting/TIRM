import openai

with open("../../data/atomic_sentences_p.txt","r",encoding='utf-8') as f:
    sentence1 = f.readlines()
    sentence1 = [line.strip() for line in sentence1]

with open("../../data/atomic_sentences_q.txt","r",encoding='utf-8') as f:
    sentence2 = f.readlines()
    sentence2 = [line.strip() for line in sentence2]

pattern5_list = []

for i in sentence1:
    for j in sentence2:
        pattern5 = "Suppose that \"" + i[:len(i)-1] + ", or " + j + "\" and \"" + i[0] + ' do not' + i[
                                                                       1:] + "\" are true. What is the conclusion? (If there is a conclusion, you only response the conclusion without any analysis. Otherwise, you should only answer \"there is no conclusion\")"
        pattern5_list.append(pattern5)

openai.api_key = ''  #The API key provided by openAI
pattern1_results = []

import time

role = 'Now, please act as a mathematician for the following logical reasoning task.'

i = 0
while i < len(pattern5_list):
    pattern1_dict = {}
    if i % 10 == 0:
        messages = []
        message =  {"role": "user", "content": role}
        messages.append(message)
        try:
            response = openai.ChatCompletion.create(
                model='gpt-3.5-turbo',
                messages=messages,
                temperature=1.0
            )
        except:
            continue
        else:
            result = ''
            for choice in response.choices:
                result += choice.message.content
            response = {"role": "assistant", "content": result}
            messages.append(response)
            pattern1_dict['question'] = role
            pattern1_dict['response'] = result
            print('the {}-th turn:'.format(i), pattern1_dict)

    message = {"role": "user", "content": pattern5_list[i]}
    messages.append(message)
    try:
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=messages,
            temperature = 1.0
        )
    except:
        k = i % 10
        i = i - i % 10
        print("warning!!!!")
        pattern1_results = pattern1_results[:len(pattern1_results)-k]

    else:
        result = ''
        for choice in response.choices:
            result += choice.message.content
        response = {"role": "assistant", "content": result}
        messages.append(response)
        pattern1_dict['question'] = pattern5_list[i]
        pattern1_dict['response'] = result
        pattern1_results.append(pattern1_dict)
        print('the {}-th turn:'.format(i), pattern1_dict)
        time.sleep(10)
        i += 1

import json
with open("DSR.json","w",encoding = "utf-8") as f:
    json_str = json.dumps(pattern1_results)
    f.write(json_str)

