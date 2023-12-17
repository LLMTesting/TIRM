# Automatic Testing and Improvement for the Reasoning Ability of Large Language Models
The repository is for the paepr "Automatic Testing and Improvement for the Reasoning Ability of Large Language Models", and TIRM is the abbreviation for our method.

## Datasets
According to the reasoning patterns we propose, we use atomic sentences to generate test cases, and we put the atomic sentences we wrote in the folder "data".

## Testing Subject
We test the most advanced online LLMs ChatGPT and Claude, and three open-source LLMs, Llama, OpenBuddy, and Baichuan.

## Our Approach
Our method TIRM comprises the following three steps:

(1) **Test generation.** We design six logical reasoning patterns to generate test cases, which follow the reasoning rules applied in boolean logic and are easy to understand for humans. We aim to employ generated test cases to detect whether LLMs have the essential reasoning ability.

(2) **Answer Evaluation.** In this step, we compare the answer of the LLM to the logical reasoning test with the expected answer we design. When the similarity between the two is lower than a certain threshold, we judge that the LLM has a wrong answer.

(3) **Model Prompting.** When logical reasoning errors are detected in the LLM, we hope to correct its error through reasonable prompting. For this reason, we design three different answer prompting methods and explore what kind of prompting methods are helpful to the LLM to correct the error.

## Experiments
We organize the codes in the repository according to RQs, and the codes of RQ1-3 are stored in folders with corresponding names, the code is named according to the name of the inference pattern:

(1) RQ1 is the test result of a single round of question and answer, and the code is stored in the "RQ1" folder. RQ1a is the experimental result of 10 questions and answers in one dialogue, and the code is stored in the "RQ2" folder.

(2) RQ2 is the impact of the 3 model prompting methods on logical reasoning. This folder is divided into three parts according to the name of the prompting methods, i.e., FP, RP and HP.

(3) RQ3 is the effectiveness of fine-tuning on three open-source LLMs, and the code is in the "RQ3" folder.

# Snapshot

We put the screenshots of the ChatGPT examples used in the paper in the snapshot folder, including the examples in Section 6.1.

**The snapshots in the results of case study (Section 6.1):**

We asked the same question in 10 conversations, and all of them got wrong reasoning conclusions. Since the answers are the same ten times, we only chose the screenshot of one of them as a representative:

![motivation](https://github.com/LLMTesting/TIRM/blob/master/snapshot/case1.png 'case study 1')

![motivation](https://github.com/LLMTesting/TIRM/blob/master/snapshot/case2.png 'case study 2')
