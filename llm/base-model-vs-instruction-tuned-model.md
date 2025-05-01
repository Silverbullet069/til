# Base Model Vs Instruction-tuned Model

<!-- tl;dr starts -->

Every leading AI platforms' services are came from Instruction-tuned Model. Base model is often proprietary and use by company's researchers only, so normal users don't need to know about them.

<!-- tl;dr ends -->

According to [fimbulvntr](https://www.reddit.com/r/LocalLLaMA/comments/1c1sy03/an_explanation_of_base_models_are/), _Base model_ barebone is an "autocomplete model" or a "pattern completer". It can do anything if given patterns. Give it a prompt whose _context_ is a:

- Chat conversation, it will continue as chatting.
- `Task -> Execution -> Task -> Execution -> Task`, it will produce `Execution`.
- Wrong QA answers, it will tell you the wrong answer.

Prompt:

```
Q: What is 1+1? A:5
Q: How many people live in Mumbai? A: 9 billion people
Q: What is the innermost planet in the solar system? A: Mars
Q: What is the capital of France? A:
```

Output:

```
London
```

## Comprehensive Comparison given by Claude 3.7 Sonnet Thinking (2024-03-04)

<!-- prettier-ignore -->
||Base model|Instruction-tuned model|
|---|---|---|
|**Definition**|LLMs trained on massive text corpora using self-supervised learning. By doing so, they learn general language patterns, knowledge and capabilities|_Base model_ that has undergone additional training to follow human instructions. You can say they are "fine-tuned" to understand and respond to specific instructions in a helpful and safe manner|
|**Training Objective**|Next-token Prediction (layman's term: predicting the next word given previous context)|Follow instructions and produce helpful, accurate and safe outputs|
|**Training data**|Massive text corpora from the Internet, Paper books, Old manuscripts, ...|Base model data + Instruction-Response pairs + Human feedback|
|**Training approach**|Self-supervised learning without labels|Fine-tuning via supervised learning + Reinforcement Learning from Human Feedback (RLHF)|
|**Example Process**|Given the text "The capital of France is", the model learns to predict "Paris"|Given an instruction like "Explain quantum computing to a 10-year-old", the model generates an appropriate, simplified explanation|
|**Output**|Same style and tone with input, may contradict itself, may generate harmful, biased or inappropriate content|Helpful assistant-like tone, more consistent, more likely to refuse harmful requests, reduce biases|
|**Use Cases**|<ul><li>Research</li><li>Building blocks for Instruction-tuned Models</li><li>Text generation where creativity is valued over safety</li></ul>|<ul><li>Commercial applications</li><li>Assistant chatbots</li></ul>|
|**Example Vendor**|Proprietary GPT-4 base model|`gpt4o`, `gpt4o-mini`, `claude3.5-sonnet`, `claude3.7-sonnet`...|
