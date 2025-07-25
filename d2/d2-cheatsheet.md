# D2 Cheatsheet

<!-- tl;dr starts -->

D2 is my most favorite diagraming language. It's much more easier to write and read than other more popular language such as Mermaid.

<!-- tl;dr ends -->

## Cons

* D2's VSCode Extension is far from feature-complete and relies heavily on the community:

  - No language server ([the PR for the language server implementation by BarryNolte has been converted to draft since March 2024](https://github.com/terrastruct/d2-vscode/pull/117))
  - Performance issues: every time a Markdown file that includes D2 code blocks is saved, the extension incurs a slight delay, even when the Preview Pane is not open. The delay duration depends on the complexity of the diagrams.

* It's not supported by GitHub Flavored Markdown, so you would have to replace all of your D2 code blocks with external rendered SVG/PNG images.

* D2 Playground requires WebAssembly enabled.

## Table of Contents

- [Cons](#cons)
- [Template](#template)
- [Shape and labels](#shape-and-labels)
- [Connection](#connection)
- [Containers](#containers)
- [Styles](#styles)
- [Text](#text)
- [Icons](#icons)
- [Position](#position)
- [Classes](#classes)
- [Sequence Diagram](#sequence-diagram)
- [Dimonsions](#dimonsions)
- [Interactive](#interactive)
- [TALA - Terrastruct's AutoLayout Approach](#tala---terrastructs-autolayout-approach)

## Template

This is a more comprehensive D2 template incorporating commonly used elements. You can use this as a starting point for new diagrams.

```d2
# naming convention: snake_case

vars: {
  d2-config: {
    theme-id: 300 # Dark Mauve
    layout-engine: tala # or dagre, elk
    sketch: true # for a hand-drawn look
  }
}

direction: down # Or right, up, left

# Page Title
page_title: "Diagram Title" {
  shape: text
  near: top-center
  style: {
    font-size: 36
    bold: true
  }
}

# --- Basic Shapes & Connections ---
shape_a: "Label A" {
  # shape: rectangle # Default shape
  # icon: "path/to/icon_a.svg"
  # style.fill: "#A9CCE3"
  # tooltip: "Info about A"
  # link: "https://example.com/a"
}

shape_b: "Label B" {
  shape: circle
  # style.fill: "#A2D9CE"
}

shape_a -> shape_b: "Connection Label" {
  # style.stroke: "#27AE60"
  # source-arrowhead: <arrowhead_shape> # e.g., arrow, diamond, circle
  # target-arrowhead: <arrowhead_shape> # e.g., arrow, diamond, circle
}

# --- Containers ---
my_container: "Container Label" {
  # style.fill: "#FADBD8"
  # icon: "path/to/container_icon.svg"

  child_1: "Child 1"
  child_2: "Child 2"
  child_1 -> child_2: "Internal link"

  # nested_container: "Nested" {
  #   grandchild: "Grandchild"
  # }
}
# external_shape -> my_container.child_1 # Example of connecting to a child

# --- Text & Markdown ---
notes: |md
  ## Notes
  - Markdown content here.
  - Supports **bold**, *italic*, lists.
| {
  # shape: text # Optional, default for multiline is rectangle
  # near: bottom-left # Position it as needed
}

# --- Advanced (Commented out by default) ---
# classes: {
#   node_style: {
#     style: { font-size: 12; fill: "#D5DBDB" }
#   }
#   error_style: {
#     style: { fill: "#E74C3C"; font-color: white }
#   }
# }
# styled_shape.class: node_style
# error_shape.class: [node_style, error_style]

# sequence_example: {
#   shape: sequence_diagram
#   user: "User"
#   system: "System"
#   user -> system: "Request"
#   system -> user: "Response"
# }
```

### VSCode Snippet

To generate D2 template insde `.d2` D2 script file or `.md` Markdown file, save the following JSON code to `d2.json` and `markdown.d2.json` in your `.vscode/snippets` directory or user snippet.

```json
{
  "D2 Comprehensive Template": {
    "prefix": "!",
    "body": [
      "# naming convention: snake_case",
      "",
      "vars: {",
      "  d2-config: {",
      "    theme-id: ${1:300} # Dark Mauve",
      "    layout-engine: ${2:tala} # dagre, elk, tala",
      "    # sketch: true # for a hand-drawn look",
      "  }",
      "}",
      "",
      "direction: ${3:down} # Or right, up, left",
      "",
      "# Page Title",
      "page_title: \"${4:Diagram Title}\" {",
      "  shape: text",
      "  near: top-center",
      "  style: {",
      "    font-size: 36",
      "    bold: true",
      "  }",
      "}",
      "",
      "# --- Basic Shapes & Connections ---",
      "shape_a: \"${5:Label A}\" {",
      "  # shape: rectangle # Default shape",
      "  # icon: \"path/to/icon_a.svg\"",
      "  # style.fill: \"#A9CCE3\"",
      "  # tooltip: \"Info about A\"",
      "  # link: \"https://example.com/a\"",
      "}",
      "",
      "shape_b: \"${6:Label B}\" {",
      "  shape: ${7:circle}",
      "  # style.fill: \"#A2D9CE\"",
      "}",
      "",
      "shape_a -> shape_b: \"${8:Connection Label}\" {",
      "  # style.stroke: \"#27AE60\"",
      "  # source-arrowhead: <arrowhead_shape> # e.g., arrow, diamond, circle",
      "  # target-arrowhead: <arrowhead_shape> # e.g., arrow, diamond, circle",
      "}",
      "",
      "# --- Containers ---",
      "my_container: \"${9:Container Label}\" {",
      "  # style.fill: \"#FADBD8\"",
      "  # icon: \"path/to/container_icon.svg\"",
      "",
      "  child_1: \"${10:Child 1}\"",
      "  child_2: \"${11:Child 2}\"",
      "  child_1 -> child_2: \"${12:Internal link}\"",
      "",
      "  # nested_container: \"Nested\" {",
      "  #   grandchild: \"Grandchild\"",
      "  # }",
      "}",
      "# external_shape -> my_container.child_1 # Example of connecting to a child",
      "",
      "# --- Text & Markdown ---",
      "notes: |md",
      "  ## ${13:Notes Title}",
      "  - ${14:Markdown content here}.",
      "  - Supports **bold**, *italic*, lists.",
      "| {",
      "  # shape: text # Optional, default for multiline is rectangle",
      "  # near: bottom-left # Position it as needed",
      "}",
      "",
      "# --- Advanced (Commented out by default) ---",
      "# classes: {",
      "#   node_style: {",
      "#     style: { font-size: 12; fill: \"#D5DBDB\" }",
      "#   }",
      "#   error_style: {",
      "#     style: { fill: \"#E74C3C\"; font-color: white }",
      "#   }",
      "# }",
      "# styled_shape.class: node_style",
      "# error_shape.class: [node_style, error_style]",
      "",
      "# sequence_example: {",
      "#   shape: sequence_diagram",
      "#   user: \"User\"",
      "#   system: \"System\"",
      "#   user -> system: \"Request\"",
      "#   system -> user: \"Response\"",
      "# }"
    ],
    "description": "A comprehensive D2 diagram template with common elements and placeholders."
  }
}
```

[Back to TOC](#table-of-contents)

## Shape and labels

```d2
x -> y: hello world

imAShape     # by def, the shape is a rectangle
im_a_shape
im a shape   # There are SPACEs!
i'm a shape  # There are SPACEs WITH SINGLE QUOTE
a-shape      # hyphens are okay!

SQLite; Cassandra         # multiple on same line
```

```d2
pg: PostgreSQL            # label
Cloud: my cloud
Cloud.shape: cylinder     # changing shape using dot notation
```

[Back to TOC](#table-of-contents)

## Connection

```d2
## There are four connection types
read replica <- master
write replica -> master
read replica 1 -- read replica 2
write replica 1 <-> write replica 2
```

```d2
be: Backend
fe: Frontend

## connections must refer to the "key" of a shape, not its label
Backend -> Frontend     # create new shape
be -> fe                # use existing shapes
```

```d2
## repeated connections
db -> s3: backup
```

```d2
## connection chaining
high mem instance -> ec2 <- high cpu instance: hosted by
```

```d2
## cycle
Stage One -> Stage Two -> Stage Three -> Stage Four
Stage Four -> Stage One: repeat
```

```d2
## override default arrowhead shape
## connection's style can be customized

a: The best way to avoid responsibility is to say, "I've got responsibilities"

b: Whether weary or unweary, O man, do not rest

c: I still maintain the point that designing a monolithic kernel in 1991 is a

# NOTE: arrowhead can only be tweaked in connection
a -> b: To err is human, to moo bovine {
  source-arrowhead: 1
  target-arrowhead: * {
    shape: diamond
    style.filled: true
  }
}

b <-> c: Reality is just a crutch for people who can't handle science fiction {
  source-arrowhead: 1
  target-arrowhead: * {
    shape: diamond
    style.filled: true
  }
}

d: A black cat crossing your path signifies that the animal is going somewhere

d -> a -> c

## There are much more arrowhead options
## Very useful when create UML Class/SQL diagram
# triangle
# arrow
# diamond
# circle
# box
# cf-one, cf-one-required
# cf-many, cf-many-required
```

**Referencing connections:** Use parenthesis and square brackets syntax

```d2
x -> y: hi
x -> y: hello

(x -> y)[0].style.stroke: red
(x -> y)[1].style.stroke: blue
```

[Back to TOC](#table-of-contents)

## Containers

```d2
## Using dot notation to create nested containers
server
server.process
im a parent.im a child
apartment.bedroom.bathroom -> office.spareroom.bathroom: Silent Hill Portal

## nested syntax
clouds: {
  aws: {
    load balancer -> api
    api -> db
  }
  gcloud: {
    auth -> db
  }
  gcloud -> aws
}

users -> clouds.aws.load balancer
users -> clouds.gcloud.auth
ci.deploys -> clouds

# container labels
gcloud: Google Cloud # short
gcloud2: {
  label: Google Cloud # reserved keyword `label`
}
```

```d2
## reference outside of the container from within
christmas: {
  presents
}

birthdays: {
  presents
  _.christmas.presents -> presents: regift
  _.christmas.style.fill: "#ACE1AF"
}
```

[Back to TOC](#table-of-contents)

## Styles

```d2
direction: right

# opacity
x -> y: hi {
  # connection style
  style: {
    opacity: 0.4
  }
}
# shape style
x.style.opacity: 0
y.style.opacity: 0.7

# stroke
x2 -> y2: hi {
  # connection style
  style: {
    stroke: deepskyblue
  }
}
x2.style.stroke: brown

# fill (shape only)
x3 -> y3: hi
x3.style.fill: honeydew
y3.style.fill: cornflowerblue

# stroke-width
# stroke-dash
# border-radius
# shadow
# 3D
x4.style.3d: true
# multiple
x5.style.multiple: true
# double border
x6.shape: circle # rectangle, oval
x6.style.double-border: true

# font: D2 use 4 font families
# - Source Sans Pro for majority
# - Source Code Pro for code blocks and text in Class shape
# - Architect's Daughter and Fuzzy Bubbles for `sketch` mode.

# font-size: true/false
# font-color: true/false
# bold, italic, underline: true/false
# animated: true/false
x7 -> y7: hi {
  style: {
    animated: true
  }
}
x7.style.animated: true

# text transformation
tom -> jerry: hi {
  style: {
    text-transform: capitalize
  }
}
jerry.style.text-transform: uppercase

# root style
# 6 keywords supported
#
# fill
# fill-pattern
# stroke
# stroke-width
# stroke-dash
# double-border
```

[Back to TOC](#table-of-contents)

## Text

```d2
direction: right

explanation: |md
  # Header
  - list item 1
  - list item 2

  And other normal markdown stuff
| # acts as the EOF

# single pipe
code snippet: |js
  console.log("Hello, World")
|

# double pipe
block string: ||ts
  declare function getSmallPet(): Fish | Bird;
||

# triple pipe
block string 2: |||ts
  declare function getSmallPet(): Fish | Bird;
  const works = (a > 1) || (b < 2);
|||

# grave accent/backtick
block string final: |`ts
  declare function getSmallPet(): Fish | Bird;
  const works = (a > 1) || (b < 2);
`|

# Non-Markdown text
title: A winning strategy {
  shape: text
  near: top-center
  style: {
    font-size: 48
    italic: true
  }
}

poll the people -> results
results -> unfavorable -> poll the people
results -> favorable -> will of the people
```

[Back to TOC](#table-of-contents)

## Icons

```d2
# Terrastruct repository: https://icons.terrastruct.com/
# required for production-ready diagram

my network: {
  # icon: https://icons.terrastruct.com/infra/019-network.svg
  icon: "./019-network.svg"
}

# icon placement is automatic
# coexistence with a label + whether it's a container affect where the icon is placed not to obstruct
vpc: VPC 1 10.1.0.0./16 {
  # container icon
  icon: https://icons.terrastruct.com/aws%2F_Group%20Icons%2FVirtual-private-cloud-VPC_light-bg.svg
  style: {
    stroke: green
    font-color: green
    fill: white
  }
  az: Availability Zone A {
    style: {
      stroke: blue
      font-color: blue
      stroke-dash: 3
      fill: white
    }
    firewall: Firewall Subnet A {
      # container icon
      icon: https://icons.terrastruct.com/aws%2FNetworking%20&%20Content%20Delivery%2FAmazon-Route-53_Hosted-Zone_light-bg.svg
      style: {
        stroke: purple
        font-color: purple
        fill: "#e1d5e7"
      }
      ec2: EC2 Instance {
        # non-container icon
        icon: https://icons.terrastruct.com/aws%2FCompute%2F_Instance%2FAmazon-EC2_C4-Instance_light-bg.svg
      }
    }
  }
}

server: {
  shape: image
  icon: https://icons.terrastruct.com/essentials%2F112-server.svg
}

github: {
  shape: image
  icon: https://icons.terrastruct.com/social%2F039-github.svg
}
```

[Back to TOC](#table-of-contents)

## Position

```d2
# keyword near:
#
# top-left
# top-center
# top-right
# center-left
# center-right
# bottom-left
# bottom-cetner
# bottom-right
# default: center (duh)

title: |md
  # A winning strategy
| {
  near: top-center
}

poll the people -> results
results -> unfavorable -> poll the people
results -> favorable -> will of the people

# NOTE: make a legend using positions and dimensions
legend: {
  near: bottom-center

  color1: foo {
    shape: text
    style.font-color: green
  }

  color2: bar {
    shape: text
    style.font-color: red
  }
}

explanation: |md

  # LLMs

  The Large Language Model (LLM) is a powerful AI\

  system that learns from vast amounts of text data.\

  By analyzing patterns and structures in language,\

  it gains an understanding of grammar, facts,\

  and even some reasoning abilities. As users input text,\

  the LLM predicts the most likely next words or phrases\

  to create coherent responses. The model\

  continuously fine-tunes its output, considering both the\

  user's input and its own vast knowledge base.\

  This cutting-edge technology enables LLM to generate human-like text,\

  making it a valuable tool for various applications.

| {
  near: center-left
}

ML Platform -> Pre-trained models

ML Platform -> Model registry

ML Platform -> Compiler

ML Platform -> Validation

ML Platform -> Auditing

Model registry -> Server.Batch Predictor

Server.Online Model Server

direction: right

x -> y

x: worker {
  icon: https://icons.terrastruct.com/essentials%2F005-programmer.svg

  # when positioning labels and icons, an outside- prefix can be added
  icon.near: outside-top-right
}

y: profits {
  label.near: bottom-right

  icon: https://icons.terrastruct.com/essentials%2Fprofits.svg

  icon.near: outside-top-left
}

# near object
# TALA only
aws: {
  load_balancer -> api
  api -> db
}

gcloud: {
  auth -> db
}

gcloud -> aws

explanation: |md
  # Why do we use AWS?

  - It has more uptime than GCloud
  - We have free credits
| {
  near: aws
}
```

[Back to TOC](#table-of-contents)

## Classes

```d2
direction: right

classes: {
  load balancer: {
    # multi-line long labels avoid label collisions
    label: load\nbalancer
    width: 100
    height: 200
    style: {
      stroke-width: 0
      fill: "#44C7B1"
      shadow: true
      border-radius: 5
    }
  }

  unhealthy: {
    style: {
      fill: "#FE7070"
      stroke: "#F69E03"
    }
  }
}

web traffic -> web lb

web lb.class: load balancer

web lb -> api1

web lb -> api2

web lb -> api3

api2.class: unhealthy

api1 -> cache lb

api3 -> cache lb

cache lb.class: load balancer

classes: {
  red: {
    style: {
      stroke: red
    }
  }
}

connection class: {
  # a -> b: {
  #   class: red
  # }
  a -> b
  (a -> b)[0].class: red
}

classes: {
  d2: {
    label: ""
    icon: https://play.d2lang.com/assets/icons/d2-logo.svg
  }
  sphere: {
    shape: circle
    style: {
      stroke-width: 0
    }
  }
}

logo.class: [d2; sphere] # seperated by semicolons

# order matters
classes: {
  uno: {
    label: 1
  }
  dos: {
    label: 2
  }
}

x.class: [uno; dos]
y.class: [dos; uno]
```

[Back to TOC](#table-of-contents)

## Sequence Diagram

```d2
# ==============================================================================
# Sequence Diagram
# ==============================================================================
#

demo sequence diagram: {
  shape: sequence_diagram
  alice -> bob: what does it mean\nto be well-adjusted?
  bob -> alice: The ability to play bridge or\ngolf
}

demo sequence diagram \#2: {
  2007: Office chatter in 2007 {
    shape: sequence_diagram
    alice: Alice
    bob: Bobby
    # group
    awkward small talk: {
      style.fill: white
      alice -> bob: uhm, hi
      bob -> alice: oh, hello
      icebreaker attempt: {
        alice -> bob: what did you have for lunch?
      }
      unfortunate outcome: {
        bob -> alice: that's personal
      }
    }
  }

  2012: Office chatter in 2012 {
    shape: sequence_diagram

    alice: Alice
    bob: Bobby
    alice -> bob: Want to play with ChatGPT?
    bob -> alice: Yes!
    bob -> alice.play: Write a play...
    alice.play -> bob.play: about 2 friends...
    bob.play -> alice.play: who find love...
    alice.play -> bob.play: in a sequence diagram
  }

  2007 -> 2012: Five\nyears\nlater
}

# spans/lifespan/activation box/activation bar
demo sequence diagram \#3: {
  shape: sequence_diagram

  alice.t1 -> bob
  alice.t2 -> bob.a
  alice.t2.a -> bob.a
  alice.t2.a <- bob.a
  alice.t2 <- bob.a
}

# groups/fragments/edge group/frame

demo sequence diagram \#4: {
  shape: sequence_diagram

  # Predefine actors

  alice

  bob

  shower thoughts: {
    alice -> bob: A physicist is an atom's way of knowing about atoms.
    alice -> bob: Today is the first day of the rest of your life.
  }

  life advice: {
    bob -> alice: If all else fails, lower your standards.
  }
}

# notes
demo sequence diagram \#5: {
  shape: sequence_diagram

  alice -> bob

  bob."In the eyes of my dog, I'm a man."

  # Notes can go into groups, too

  important insight: {
    bob."Cold hands, no gloves."
  }

  bob -> alice: Chocolate chip.
}

demo sequence diagram \#6: {
  shape: sequence_diagram

  son -> father: Can I borrow your car?

  friend -> father: Never lend your car to anyone to whom you have given birth.

  father -> father: internal debate ensues
}

# customization
demo sequence diagram \#7: {
  shape: sequence_diagram

  scorer: {shape: person}

  scorer.t -> itemResponse.t: getItem()

  scorer.t <- itemResponse.t: item {
    style.stroke-dash: 5
  }

  scorer.t -> item.t1: getRubric()

  scorer.t <- item.t1: rubric {
    style.stroke-dash: 5
  }

  scorer.t -> essayRubric.t: applyTo(essayResp)

  itemResponse -> essayRubric.t.c

  essayRubric.t.c -> concept.t: match(essayResponse)

  scorer <- essayRubric.t: score {
    style.stroke-dash: 5
  }

  scorer.t -> itemOutcome.t1: new

  scorer.t -> item.t2: getNormalMinimum()

  scorer.t -> item.t3: getNormalMaximum()

  scorer.t -> itemOutcome.t2: setScore(score)

  scorer.t -> itemOutcome.t3: setFeedback(missingConcepts)
}

demo sequence diagram \#8: {
  shape: sequence_diagram

  alice -> bob: What does it mean\nto be well-adjusted?

  bob -> alice: The ability to play bridge or\ngolf as if they were games.

  alice.style: {
    stroke: red

    stroke-dash: 0
  }
}
```

[Back to TOC](#table-of-contents)

## Dimonsions

```d2
# Sometimes it's not appropriate for shapes' size to depend on content.
# Use `width:` and `height:` to set more appropriate dimensions.

direction: right

small jerry: "" {
  shape: image
  icon: https://static.wikia.nocookie.net/tomandjerry/images/4/46/JerryJumbo3-1-.jpg
  width: 200
  height: 200
}

med jerry: "" {
  shape: image
  icon: https://static.wikia.nocookie.net/tomandjerry/images/4/46/JerryJumbo3-1-.jpg
  width: 300
  height: 300
}

big jerry: "" {
  shape: image
  icon: https://static.wikia.nocookie.net/tomandjerry/images/4/46/JerryJumbo3-1-.jpg
  width: 500
  height: 400
}

big jerry -> med jerry -> small jerry
```

[Back to TOC](#table-of-contents)

## Interactive

```d2
# purpose
# - add secondary context
# - tidy

x: {
  tooltip: foo bar
}

y: {
  tooltip: bar bazz
}

x -> y

x2: I'm a Mac {
  link: https://apple.com
}

y2: And I'm a PC {
  link: https://microsoft.com
}

x2 -> y2: Google {
  link: https://google.com
}
```

[Back to TOC](#table-of-contents)

## TALA - Terrastruct's AutoLayout Approach

It's a closed source, proprietary layout engine developed by Terrastruct. It many fixes problems from other archaic layout engines that no longer being supported.

Key points:

- **Symmetry:** shapes are put into positions that make the whole diagram symmetrical.

  ![symmetry diagram](./symmetry.png)

- **Clusters:** multiple shapes connected to the same shape are laid side-by-side with each other.

  ![cluster diagram](./cluster.png)

- **Hierarchy:** structures identified by multiple levels of shapes connected in the same direction. A special set of rules get enforced (e.g. even spacing between levels).
  Write `shape: hierarchy`to force a hierarchical shape.

  ![hierarchy diagram](./hierarchy.png)

- **Balanced connections:** if there is a large number of connections that can't fit entirely on the center space (even after enlarging container), it will reroute some of them to left-and-right space but still symmetrical.

  ![balancing diagram](./balancing.png)

- **Dynamic label positioning:** Label are positioned to where they avoid obstructions (shapes, connections, ...)

  | Shape label             | Connection label          |
  | ----------------------- | ------------------------- |
  | ![label 1](./label.png) | ![label 2](./label-2.png) |

- **Square aspect ratio:** non-connected subgraphs are bin-packed so they feel symmetrical.

  ![bin packing](./bin-packing.png)

- **Direction per container:** specify `direction: up|down|left|right` constraint inside containers, by default it prefers "down-right".

  ![direction per container](./direction.png)

- **Shapes near other shapes:** specify `near: <absolute ID>` constraint targeting other shapes, providing absolute ID if targeting shapes nested inside container.

  ![near](./near.png)

- **SQL table column matching:** if two SQL tables has a foreign key constaint, the `sql_table` connection points the foreign key column of one table to the ID column of another table.

  ![sql](./sql.png)

- **Sequences:** a chain of shapes connected with `steps:` are arranged from tail to head instead of using connections.

  ![sequences](./sequences.png)

- **Self-connections:** `x -> x` occupies a corner. Multiple connections of the same type (directed, undirected, bidirected) reused the same corners.

  ![self-connection](./self-connection.png)

- **Perfer horizontal connections for many labels:** When 2 nodes have 3 or more connections between them, all with labels, those nodes will prefer a horizontal position with each other.

  > **NOTE:** if `direction: down` or `direction: up` is explicitly set, this behavior is ignored.

  ![horizontal](./horizontal.png)

- **Grid edges:** better edge routers

  | Non-TALA grid connections           | TALA grid connections         |
  | ----------------------------------- | ----------------------------- |
  | ![grid-no-tala](./grid-no-tala.png) | ![grid-tala](./grid-tala.png) |

- **Seed:** Specifying different seed values might get you better results on complex diagrams. Note that the more seeds there are, the more computer resources D2 takes.

  ![seed](./seed.png)

- **Relative positioning:** set `top:` and `left:` for top-level objects and nested-level objects will move around it.

  ![relative-positioning](./rel-positioning.png)

  > Processing use Input as anchor, Renderer and Validator use Processing as anchor.

[Back to TOC](#table-of-contents)
