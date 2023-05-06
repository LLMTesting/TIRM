import openai
from sentence_transformers import SentenceTransformer, util
model = SentenceTransformer('paraphrase-mpnet-base-v2')

with open("../../data/atomic_sentences_p.txt","r",encoding='utf-8') as f:
    sentence1 = f.readlines()
    sentence1 = [line.strip() for line in sentence1]
print(sentence1)

with open("../../data/atomic_sentences_q.txt","r",encoding='utf-8') as f:
    sentence2 = f.readlines()
    sentence2 = [line.strip() for line in sentence2]

pattern5_list = []
ground_truth = []
ground_truth2 = []

for i in sentence1:
    for j in sentence2:
        pattern5 = "Suppose that \"" + i[:len(i) - 1] + ", or " + j + "\" and \"" + i[0] + ' do not' + i[
                                                                                                       1:] + "\" are true. What is the conclusion? (If there is a conclusion, you only response the conclusion without any analysis. Otherwise, you should only answer \"there is no conclusion\")"
        pattern5_list.append(pattern5)
        ground_truth2.append(i[0] + ' do not' + i[1:])
        ground_truth.append(j)



openai.api_key = '' #The API key provided by openAI
pattern1_results = []

import time

i = 0
while i < len(pattern5_list):
    pattern1_dict = {}
    if i % 10 == 0:
        messages = []
        m = 1
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
        flag = 1

        result = ''
        for choice in response.choices:
            result += choice.message.content
        response = {"role": "assistant", "content": result}
        messages.append(response)
        pattern1_dict['question'] = pattern5_list[i]
        pattern1_dict['response'] = result
        print('the {}-th turn:'.format(i), pattern1_dict)
        time.sleep(10)
        sent1 = result
        sent2 = ground_truth[i]
        sent3 = ground_truth2[i]

        # Compute embedding for both lists
        embeddings1 = model.encode(sent1, convert_to_tensor=True)
        embeddings2 = model.encode(sent2, convert_to_tensor=True)
        embeddings3 = model.encode(sent3, convert_to_tensor=True)

        # Compute cosine-similarities
        cosine_scores = util.cos_sim(embeddings1, embeddings2)
        cosine_scores = cosine_scores.numpy()

        cosine_scores2 = util.cos_sim(embeddings1, embeddings3)
        cosine_scores2 = cosine_scores2.numpy()

        if cosine_scores[0][0] < 0.5 and cosine_scores2[0][0] < 0.5 and m < 7:
            try:
                correct = 'The conclusion is wrong, the right one is that: ' + ground_truth[i]
                # correct = 'The conclusion is wrong.'
                # correct = 'The conclusion is wrong. Given \"p or q\" and \"¬p\" are true, where p and q represent statements, we can infer that q is true, so the conclusion is that ' + ground_truth[i] + '\n' + 'You should use this guideline to answer the following questions.'
                message = {"role": "user", "content": correct}
                messages.append(message)
                response = openai.ChatCompletion.create(
                    model='gpt-3.5-turbo',
                    messages=messages,
                    temperature=1.0
                )
            except:
                flag = 0
                k = i % 10
                i = i - i % 10
                print("warning!!!!")
                pattern1_results = pattern1_results[:len(pattern1_results) - k]
            else:
                result = ''
                for choice in response.choices:
                    result += choice.message.content
                response = {"role": "assistant", "content": result}
                messages.append(response)
                pattern1_dict['correct'] = correct
                pattern1_dict['response_correct'] = result
                print('the {}-th turn:'.format(i), pattern1_dict)
                time.sleep(10)
        if flag == 1:
            pattern1_results.append(pattern1_dict)
            i += 1
        m += 1


import json
with open("DSR.json","w",encoding = "utf-8") as f:
    json_str = json.dumps(pattern1_results)
    f.write(json_str)

