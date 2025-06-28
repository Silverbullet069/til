# Prompt Engineering Prerequisites

<!-- tl;dr starts -->

**TL;DR**: **Define success criteria** and **Create strong empirical evaluations** are two of Anthropic's Prompt Engineering prerequisites. There are **TWELVE** success criteria: **4 strong** criteria and **8 common** criteria. Each success criteria will be evaluated by different evaluation strategies.

<!-- tl;dr ends -->

## Strong success criteria

### 1. Specific

_Definition:_ Define finest-grained level goal.

_Examples:_

- Bad: `good performance`
- Good: `accurate sentiment classification`

### 2. Measurable

_Definition:_ Evaluate with Quantitative methods using Quantitative metrics, Qualitative scales, or a Hybrid between them. Make everything, even vague topics such as ethics and safety can be quantified.

**Quantitative metrics:**

- Task-specific metrics: F1 score, BLEU score, Perplexity.
- Confusion Matrix matrics: Accuracy, Precision, Recall.
- Operational metrics: Response time (ms), Uptime (%).

**Quantitative methods:**

- A/B Testing: calculate the same quantitative metrics between two different models.
- User feedback: track everything came from user.
  - Number of follow-up queries.
  - Response quality graded by users.
  - Time spent.
  - Completion rate.
  - ...
- Edge case analysis: % of edge cases handled without errors.

**Qualitative scales:**

- Likert scales, Ordinal scale.
- Rubrics.

### 3. Achievable

_Definition_: The goal is to make our applications better, but better at which metrics, and how much better? Trial and error could lead to wasting time and money so before getting started in prompt engineering, base the goal on:

- prior experiments.
- industry benchmarks.
- models breakthrough. (Claude 3.5 -> 3.7, GPT4.0 -> 4.5, ...)
- expert knowledge.

### 4. Relevant

_Definition:_ Criteria must come from application's requirements.

_Example:_ A medical assistant chatbot must have empathetic tone when talking with patients, strong citation accuracy and respect patients' privacy information. But less so for casual chatbot.

## Common success criteria

### 5. Task fidelity

_Definition_:

- How well does the model need to perform on the task?
- Task on general cases versus on edge cases where rare or challenging inputs are prompted?

_Evaluation strategy:_ **Exact match evaluation on Sentimental analysis**

- It measures whether the model's output exactly matches a predefined correct answer.
- It's a simple, unambiguous metric.
- It's perfect for tasks with clear-cut, categorical answers like sentiment analysis (positive, negative, neutral).

_Example_: [1000 tweets with human-labeled sentiments](https://docs.anthropic.com/en/docs/build-with-claude/develop-tests#task-fidelity-sentiment-analysis-exact-match-evaluation)

### 6. Consistency

_Definition:_

- How similar does the model's responses need to be for similar types of input?
- How important is it that they get semantically similar answers, if a user asks the same question twice.

_Evaluation strategy:_ **Cosine similarity evaluation on answering FAQ**

- It measure the similarity between 2 vectors (not mathematical vector, but sentence embeddings of the model's output) by computing the cosine of the angle between them. Values **closer to 1** indicate **higher similarity**.
- It's very ideal for evaluating consistency.

_Example_: [50 groups of FAQ with a few paraphrased versions each](https://docs.anthropic.com/en/docs/build-with-claude/develop-tests#consistency-faq-bot-cosine-similarity-evaluation)

### 7. Relevance and coherence

_Definition:_

- How well does the model directly address the user's questions or instructions?
- How important is it for the info to be presented in a logical, easy to follow manner?

_Evaluation strategy:_ **ROUGE-L evaluation on Summarization**

- It evaluates the quality of generated summaries by measuring the length of the longest common subsequence between the candidate and reference summaries.
- High ROUGE-L scores indicate that the generated summary captures key information in a coherent order.

_Example_: [200 articles with reference summaries](https://docs.anthropic.com/en/docs/build-with-claude/develop-tests#relevance-and-coherence-summarization-rouge-l-evaluation)

### 8. Tone and style

_Definition:_ How appropriate is the model's output tone for the target audience? How well does the model's output style match expectations?

_Evaluation strategy_: **LLM-based Likert scale on tone classification**

- It's a psychometric scale that uses an LLM to judge subjective attitudes or perceptions, nuanced aspects like empathy, professionalism, patience that are difficult to quantify with traditional metrics.
- It's common to use a 1-to-5 scale.

_Example:_ [100 customer inquiries with target tone (empathetic, professional, concise, patient on a customer service chatbot)](https://docs.anthropic.com/en/docs/build-with-claude/develop-tests#tone-and-style-customer-service-llm-based-likert-scale)

### 9. Privacy preservation

_Definition_: Does the model contain or reference personal/sensitive information given by users prompts in its responses?

_Evaluation strategy:_ **LLM-based binary classification on Personal Health Information detection**

- It's the oldest classification problem: determine if an input belongs to one of two classes.
- It can understand context and identify subtle or implicit forms of sensitive information that rule-based systems might miss.

_Examples:_ [500 simulated patient queries, some with Personal Health Information](https://docs.anthropic.com/en/docs/build-with-claude/develop-tests#privacy-preservation-medical-chatbot-llm-based-binary-classification)

### 10. Context utilization

_Definition_: How well does it reference and build upon information given in its history?

_Evaluation strategy_: **LLM-based Ordinal scale on context-dependent questions**

- Very similar to Likert scale, the only different is that Likert scale can choose any intervals, for Ordinal scale it measures on a fixed, 1-to-5 scale.
- It can capture the degree to which the model references and builds upon the conversation history, which is key for coherent, personalized interactions.

_Examples:_ [100 multi-turn conversations with context-dependent questions](https://docs.anthropic.com/en/docs/build-with-claude/develop-tests#context-utilization-conversation-assistant-llm-based-ordinal-scale)

### 11. Latency

_Definition:_ The acceptable response time for the model will heavily depend on the application's real-time requirements and user expectation.

### 12. Price

_Definition:_ The budget for running the model:

- Cost per API call: input/output/reasoning token.
- The size of the model: pre-training models or reasoning models.
- Vendor: OpenAI's ChatGPT, Anthropic's Claude, X/Twitter's Grok, Google's Gemini, Meta's Llama, DeepSeek, ...

## Multi-dimensional criteria example

<!-- prettier-ignore -->
||Criteria|
|---|---|
|Bad|The model should classify sentiments well|
|Good|On a held-out test set of 10.000 diverse Twitter posts (Relevant), the sentimental analysis model should achieve (Mesurable, Specific):<ul><li>F1 score >= 0.85</li><li>Non-toxic outputs >= 99.5%</li><li>95% response time < 200ms</li><li>90% of errors causes inconvenience, not egregious</li></ul>Which is a 5% improvement over our current baseline (Achieveable).|

## References

- [Anthropic Documentation's "Build with Claude: Define your success criteria"](https://docs.anthropic.com/en/docs/build-with-claude/define-success)
- [Anthropic Documentation's "Build with Claude: Create strong empirical evaluations"](https://docs.anthropic.com/en/docs/build-with-claude/develop-tests)
