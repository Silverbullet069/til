# Mermaid Flowchart

<!-- tl;dr starts -->

Flowchart is the most commonly used type of diagram in Mermaid.

<!-- tl;dr ends -->

**Main components: nodes + edges**

> [!WARNING]
>
> 1. Rule of thumb: always add a space before or captalize the first letter.
>
>    A---oB create circle edge
>    A --- oB correct
>
>    A---xB create cross edge
>    A --- xB correct
>
> 2. Do not use the word "end" while naming nodes. Use "End" or "END".

```mermaid
---
title: Node with text
---
%%{init: {"flowchart": {"htmlLabels": false}} }%%

flowchart LR
%% TB, TD, BT, RL, LR %%
  id
  id2["Enclose unicode text ❤ with double quote"]
  markdown["`Use **double quotes** and _backticks_ for ***Markdown***`"]
  newLines["`Line1
  Line2
  Line3`"]
  markdown --> newLines

  single_square[This is a rectangle]
  single_round(This is a round-edge rectangle)
  round_square([This is a button])
  double_square[[This is a scroll]]
  square_round[(This is a cylinder)]
  double_round((This is a circle))
  right_angle_square>This is a ribbon]
  single_curly{This is a rhombus}
  double_curly{{This is a hexagon}}
  square_forward_slash[/This is a parallelogram/]
  square_back_slash[\This is a parallelogram alt\]
  square_forward_backward_square[/This is a trapezoid\]
  square_backward_forward_square[\This is a trapezoid alt/]
  triple_round(((This is a double circle)))

  %% Many more: https://mermaid.js.org/syntax/flowchart.html?id=flowcharts-basic-syntax#complete-list-of-new-shapes %%
  A@{ shape: bolt }
  B@{ shape: manual-input, label: "User Input" }
  C@{ shape: docs, label: "Multiple Documents" }
  D@{ shape: procs, label: "Process Automation"}
  E@{ shape: paper-tape, label: "Paper Records"}
```

```mermaid
flowchart LR
  A --- B
  A --> B

  C -- Two dash on left, Three dash on right --- D
  E ---|Three dash on left, enclosed pipe|F

  G -->|Arrow on left, enclosed pipe|H
  I -- two dash on left, arrow on right --> J
  K -.- L
  M -.-> N
  O -. Enclosed dash dot .-> P
  Q ==> R
  S == Double equals on left, Arrow on right ==> T

  %% alter the default position of a node %%
  R ~~~ U

  V -- test --> W -- test --> X
  a --> b & c --> d
  e & f --> g & h

  A1 e1@--> A2
  e1@{ animate: true, animation: fast }
  A3 e2@==> A4
  e2@{ animate: true, animation: slow }

  %% define class %%
  classDef animate stroke-dasharray: 9,5,stroke-dashoffset: 900,animation: dash 25s linear infinite;
  B1 e3@--> B2
  %% apply class 'animate' to edge e3 %%
  class e3 animate
```

```mermaid
flowchart LR
  A --o B
  A --x B
  A o--o B
  B <--> C
  C x--x D
```

```mermaid
---
config:
  layout: elk
---
flowchart TD
    A[Start] --> B{Is it?}
    B -->|Yes| C[OK]
    C --> D[Rethink]
    D --> B
    B -- No ----> E[End]
    B ----->|No| F[Another End]
    B -.....->|No| G[Another End #2]
    %% extra dash can increase the length of a link %%


```

```mermaid
flowchart LR
  A["A double quote:#quot;"] --> B["A dec char:#9829;"]
```

```mermaid
flowchart TB
  c1 --> a2

  %% set id for subgraph %%
  subgraph id1 [one]
  a1 --> a2
  end

  subgraph id2 [two]
  b1 --> b2
  end

  subgraph three
  c1 --> c2
  end

  id1 --> id2
  three --> id2
  id2 --> c2
```

```mermaid
flowchart LR
  subgraph top
    direction TB

    subgraph B1
      direction RL
      i1 --> f1
    end

    subgraph B2
      direction BT
      i2 --> f2
    end
  end

  A --> top --> B
  B1 --> B2
```

```mermaid
flowchart LR
  %% if a subgraph node is linked to the outside %%
  %% subgraph direction will be ignored %%
  subgraph sg1
    direction TB
    top1[top] --> bot1[bottom]
  end

  subgraph sg2
    direction TB
    top2[top] --> bot2[bottom]
  end

  outside --> sg1
  outside --> top2
```

```mermaid
---
config:
  markdownAutoWrap: false
---

%%{init: {"flowchart": {"htmlLabels": false}} }%%
flowchart LR
subgraph "One"
  a("`The **cat**
  in the hat`") -- "edge label" --> b{{"`The **dog** in the hog`"}}
end
subgraph "`**Two**`"
  c("`The **cat**
  in the hat`") -- "`Bold **edge label**`" --> d("The dog in the hog")
end
```

```
%% Styling should be done via AI
%% 1. style links with `linkStyle`.
%% 2. style line curves.
%% 3. style a node.
%% 4. Use class to define styling.
%% 5. Use fontawesome to embed font (CSS must be included)
%% 6. Use custom fontawesome icons (not free)
```

```mermaid
%% by default, it uses dagre
%% elk renderer is better for larger/more complex diagram
%%{init: {"flowchart": {"defaultRenderer": "elk"}} }%%

flowchart LR
    A[Hard edge] -->|Link text| B(Round edge)
    B --> C{Decision}
    C -->|One| D[Result one]
    C -->|Two| E[Result two]

%% its width can also be tweaked
```
