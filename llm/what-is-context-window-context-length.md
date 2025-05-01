# What is Context window or Context length?

<!-- tl;dr starts -->

**TL;DR**: LLMs have "memory".

<!-- tl;dr ends -->

_Definition:_ Context window can be viewed as a LLM's "memory":

- A large context window (~200K) lets the model understand and work with bigger, more complex prompts.
- A smaller context window (~32K) limits how well the model can handle long prompts or keep track of what's being discussed in a long conversation.

_Characteristics:_

- Progressive token accumulation: the more you chat, the more tokens that get accumulated into context window.
- Linear growth pattern: Context window = Length of entire conversation history + length of current turn's input prompt + length of current turn's Claude's output response.
- 200k token capacity: ~150k words, ~650k unicode characters, ~300 single-spaced pages (according to Anthropic's estimation).
- Input-output flow: each turn consists of input phase and output phase.

_Extended thinking:_

- Extended thinking tokens are billed as output tokens only once.
- **Stripping extended thinking**: Previous turns' extended thinking blocks are generated during each turn's output phase, but are not carried forward as input tokens for subsequent turns.

_Extended thinking + tool use:_

Skipped.
