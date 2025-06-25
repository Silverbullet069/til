# Sequential Thinking Best Practices

<!-- tl;dr starts -->

An MCP server implementation that provides a tool for "dynamic and reflective problem-solving" through a structured thinking process.

<!-- tl;dr ends -->

- Break down unclear, complex problems into smaller steps.
- Automatic refining thoughts.
- Interactive manual review thoughts:
  - Filter out irrelevant information.
  - Add your own reasoning.
  - ...
- If there are multiple solutions at some points, branch into alternative paths of reasoning.

```jsonc
{
  "thought": "", // string, the current thining step. It's a little hard to read it.
  "thoughtNumber": 2, // integer, current thought number
  "totalThoughts": 3, // integer, estimated total thoughts needed
  "nextThoughtNeeded": true, // boolean, whether another thought step is needed. If set to "true" and hit Continer, it will bump the "thoughtNumber" by 1 unit and refine "thoughts". To continue, set it to false.

  /** ============================= OPTIONAL ============================== **/

  "isRevision": false, // boolean, whether this changes from previous thinking
  "revisesThought": 1, // integer, if there is a thought that you want to reconsider, specify its "thoughtNumber" here
  "branchFromThought": 1, // integer, which thought is being reconsidered
  "branchId": "", // string, branch identifier
  "needsMoreThoughts": false // boolean, if more thoughts are needed
}
```
