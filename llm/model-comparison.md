# Model Comparison

<!-- tl;dr starts -->

Numerous LLM models have emerged since the inception of the AI revolution through the present day. Understanding the capabilities of each model enables optimal selection for specialized use cases and applications.

<!-- tl;dr ends -->

---

This data is from **2025-03-06**:

<!-- prettier-ignore -->
| Model | Claude 3.7 Sonnet | Gemini 2.0 Flash |
| --- | --- | --- |
| **Vendor** | Anthropic | Google |
| **SaaS** | GitHub Copilot | GitHub Copilot, NotebookLM |
| **Description** | Anthropic's most intelligent model | Google's most intelligent *standard* model |
| **Comparative latency** | Fast | Fast |
| **Context window** | 200K (~150K words, ~680K unicode characters) | 1000K (~750K words, ~3400K unicode characters) |
| **Maximum output token** | <dl><dt>Normal</dt><dd>8192</dd><dt>Extended</dt><dd>64K</dd><dt>Beta</dt><dd>128K</dd></dl> | 8192 |
| **Reasoning mode supported** | Yes, toggleable | No, Gemini 2.0 Pro does |
| **Vision supported** | Yes | Yes |
| **Vietnamese supported** | [Unknown performance](https://docs.anthropic.com/en/docs/build-with-claude/multilingual-support) | Yes |
| **Cost (Input/Output per million tokens)** | $3.00 / $15.00 | $0.10 (text / image / video), $0.70 (audio) / $0.40 |
| **Training data cut-off date** | 2024-11 | 2024-06 (some said 2024-08) |
| **Personal opinion** | Best for coding | |

## References

- [Anthropic's All models overview](https://docs.anthropic.com/en/docs/about-claude/models/all-models)
- [Gemini Developer API Pricing](https://ai.google.dev/gemini-api/docs/pricing)
