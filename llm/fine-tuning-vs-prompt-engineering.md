# Fine Tuning Vs Prompt Engineering

<!-- tl;dr starts -->

There are differnt ways to control model behavior. When to use which?

<!-- tl;dr ends -->

<!-- prettier-ignore -->
|**Techinque**|**Prompt Engineering**|**Finetuning**|
|---|---|---|
|**Time**|Instant|Hours, even days|
|**Resource**|Friendly, only text input needed|High-end GPUs with large VRAM|
|**Cost**|Cheap, only use base model|Expensive, either being charged substantially on cloud-based AI services or spending lots of money buying high-VRAM GPUs|
|**Data**|Minimal, required zero-shot, few-shot learning|Scarce, expensive task-specific, labeled data|
|**Maintainability**|Work across base model versions without needing to change anything|Retraining might needed|
|**Flexibility**|Rapid iteration by trying various approaches to tweak prompts and see immediate results|Very difficult|
|**Domain adaptation**|Very easy, by providing domain-specific context in prompts|Retraining required|
|**Comprehensive improvement**|Best for utilize external content|Retraining required for something ad-hoc|
|**General knowledge preservation**|Models maintain its broad capabilities|Models risk catastrophic forgetting general knowledge|
|**Transparency**|Prompts are human-readable, easy to understand and debug|Model weights are just numbers, they are incomprehensible|
|**In general**|More performant, easier, take less time|Unknown performent, harder, take more time|
