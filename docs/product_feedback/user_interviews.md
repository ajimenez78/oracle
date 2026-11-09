# Oracle — User Interviews & Customer Discovery

**Period:** October–November 2026  
**Source:** Exploratory conversations in the [r/secondbrain](https://www.reddit.com/r/secondbrain/) community  
**Status:** Initial exploratory research, provisionally closed to prepare the MVP  
**Objective:** Identify real difficulties people face in managing and making use of personal knowledge, particularly during the **Express** stage of Tiago Forte's CODE method.

> **Evidence limitations:** These findings come from written exchanges and comments by a small number of participants, not structured interviews or a representative sample. It is important to distinguish participants' reported problems from our interpretations and hypotheses for Oracle.

## 1. Background and approach

**Oracle** began as a proposal for a personal assistant connected to a user's *Second Brain* (for example, Notion), capable of retrieving previously captured knowledge and helping put it to use. The initial concept included information ingestion, indexing and retrieval through RAG, and a conversational interface.

After receiving feedback about existing alternatives such as Notion, Obsidian, and general-purpose AI assistants, the team began exploring a more specific value proposition: rather than building another note-taking application or generic chatbot, help users **turn stored knowledge into useful outcomes**.

The research focused on understanding real difficulties across the **CODE** workflow:

1. **Capture:** Collect information.
2. **Organise:** Structure it.
3. **Distil:** Extract useful ideas and conclusions.
4. **Express:** Apply those ideas to create, make decisions, solve problems, or produce a deliverable.

Two potential directions were explored: **Knowledge Resurfacing** (bringing relevant, potentially forgotten information back into view) and **Knowledge Activation** (helping apply that information to a specific project or task). The aim was not to validate a predetermined solution, but to uncover obstacles and patterns.

## 2. Activities undertaken

- Participated in a [thread about the difficulty of reaching the Express stage](https://www.reddit.com/r/secondbrain/comments/1x6o0vj/how_often_does_your_second_brain_actually_get_to/).
- Published a [thread to discuss real Second Brain problems](https://www.reddit.com/r/secondbrain/comments/1xipx4a/second_brain_user_in_problems_and_building_a/).
- Held follow-up exchanges through comments and messages with **mrz999**, **e3e6**, and **vogelke**.
- Received a reference to an external tool (**Hippocampus**) from **Virtual_Loss6666**.
- Qualitatively reviewed the accounts to distinguish pain points, working solutions, and opportunities still requiring validation.

The research did not reach a large sample or include formal, in-depth interviews. Its outcome is an initial collection of accounts and lessons to guide a prototype.

## 3. Conversations by participant

### 3.1. [mrz999](https://www.reddit.com/user/mrz999/)

**What they described:**

- Capturing information can be overwhelming: something that feels essential today may turn out to be an impulsive thought tomorrow.
- They put thoughts, ideas, images, and videos into two inboxes: **Apple Notes** and **Drafts**.
- They have **two daily tasks** to review and empty both inboxes. Each item becomes a time-bound task, a reminder, a time block for a project, or gets deleted. They avoid leaving items indefinitely as “saved for later.”
- They distinguish **known work**, operational activities with familiar steps, from **thinking work**, such as writing, planning, and problem-solving, which requires reflection and does not follow a single standard procedure.
- For thinking work, they maintain a list, review it, and schedule time to make progress.
- Once the thinking is finished, they preserve the result in a **permanent note**, written in their own words, so they can reuse the conclusion rather than work it out again from scratch.

**Explicit problem:** Capture overload and the need to systematically filter what is worth keeping or turning into action.

**Current solution:** A daily processing routine, integration with tasks and calendar, and selective preservation of conclusions.

**Interpretation for Oracle:** Retrieving and applying permanent conclusions in future projects could be valuable. **The participant has not said their current Express process is failing or that they need AI to fix it.** Their behaviour provides an example of an effective workflow worth studying, not validated demand.

### 3.2. [e3e6](https://www.reddit.com/user/e3e6/)

**What they described:**

- Sometimes they **do not write anything because they do not know where to put it**.
- At other times, they know they wrote something down “somewhere” but **cannot find it**.
- Their notes are scattered across multiple applications and Notion workspaces, without a consolidated system.

**Explicit problems:** Friction during capture/organisation and difficulty retrieving information.

**Current solution:** They have not described a method that satisfactorily addresses these problems.

**Interpretation for Oracle:** This is the clearest example of an unmet need involving finding knowledge and reducing the burden of organising it. However, **there is no direct evidence that this participant wants AI-assisted deliverable creation**. Further research would need to establish whether these retrieval difficulties also affect specific tasks or projects.

### 3.3. [vogelke](https://www.reddit.com/user/vogelke/)

**What they described:**

- They use the **Linux/Unix filesystem** rather than a specialised application.
- They save articles and ideas under descriptive filenames with keywords, inside date-based directories. They mark especially useful items with the `GOOD` prefix.
- They use **`locate`** to find files quickly, reporting searches under four seconds on a system containing more than nine million files. They can also search within files when necessary.
- They readily remember dates and the circumstances surrounding information, making their chronological organisation useful.
- When they need material for a project, they create a folder under `$HOME/projects`, copy relevant sources or examples into it, and record their origin in a development log.
- They have previously built overly complex systems and then abandoned them. They warn against **overengineering / the second-system effect**, advocating the elimination of repeated work and keeping only what works.
- When asked directly about friction in connecting and applying information from multiple sources, they said **they do not experience significant difficulty**.

**Current explicit problem:** None of significance involving retrieval or application; they consider their current method good enough.

**Lesson for Oracle:** Users can meet their needs with simple tools and strong habits. A new product must remove real friction rather than impose yet another system or introduce complexity for its own sake. **vogelke should not be treated as evidence of demand for Express.**

**Shared reference:** [Organizing my Stuff](https://bezoar.org/posts/2020/0203/organizing-my-stuff/).

### 3.4. [Virtual_Loss6666](https://www.reddit.com/user/Virtual_Loss6666/)

**Contribution:** Shared only a link to the free [Hippocampus](https://github.com/marcelinollima/hippocampus) repository.

**What it is:** A self-hosted persistent memory system for Claude Code and MCP clients, using Markdown files, hybrid search (BM25, vectors, and links), and automatic contextual recall.

**Interpretation for Oracle:** A useful reference for implementation approaches and existing memory-retrieval solutions. **It is not a user account of a problem, nor evidence of interest in or demand for Oracle.**

## 4. Summary of problems and patterns

| Problem or pattern | Evidence | Participants | Interpretation |
| --- | --- | --- | --- |
| **Capture and filtering overload** | Direct | mrz999 | Collecting information indiscriminately creates extra work; a selection process helps. |
| **Not knowing where to store information** | Direct | e3e6 | Having to choose a location can prevent someone from capturing a note at all. |
| **Being unable to find previously stored information** | Direct | e3e6 | A concrete retrieval problem; this is the clearest unresolved issue in the accounts. |
| **Maintenance burden / system complexity** | Past experience and current solutions | vogelke; indirectly mrz999 | Simplicity, routines, and fewer steps matter. Not everyone experiences this friction today. |
| **Reusing knowledge in projects** | Descriptions of functional processes | mrz999, vogelke | Both demonstrate useful practices for applying knowledge; **neither reports an unmet need in Express**. |
| **Connecting forgotten ideas while working** | Team hypothesis, not validated | None directly | A possible opportunity for Oracle that requires testing through real tasks. |

### Most interesting shared themes

**1. Minimising system friction.** mrz999 follows a repeatable processing routine; vogelke relies on simple tools and avoids repetitive work; e3e6 experiences friction when deciding where to write and when retrieving notes. This is the strongest cross-cutting pattern, although it appears in different ways.

**2. Retrieval must fit each person's way of working.** Retrieval fails for e3e6 but works very well for vogelke. There is no evidence that everyone needs a new semantic search tool.

**3. Knowledge becomes valuable in the context of use.** mrz999 preserves conclusions for later reuse, and vogelke collects sources in project folders. This is consistent with the Express vision, but describes **existing behaviours**, not obstacles Oracle has been shown to solve.

**4. Avoid creating another system to maintain.** A new interface, structure, or routine could make the experience worse if it requires users to duplicate their organisational work.

## 5. Relationship to the CODE stages

| Stage | What we observed | Strength of evidence |
| --- | --- | --- |
| **Capture** | Information overload; uncertainty about where to save a note. | Direct: mrz999, e3e6. |
| **Organise** | Fragmentation and difficulty maintaining structures; working solutions based on routines and simple files. | Direct and historical: e3e6, mrz999, vogelke. |
| **Distil** | Selecting what matters and recording permanent conclusions in one's own words. | Practice described by mrz999; no validated unmet problem. |
| **Express** | Using ideas and sources in projects; reusing conclusions. | Practices described by mrz999 and vogelke; **no demonstrated common pain point or demand**. |

## 6. Product opportunities for Oracle

The following are **candidate hypotheses**, not features supported by validated market demand:

### A. Simple retrieval that tolerates disorganisation

- **Need:** Find a note without remembering where it was stored.
- **Interview support:** Direct, primarily from e3e6.
- **Risk:** Competition from existing search features, and the potential need to support multiple sources for some users.
- **Possible experiment:** Ask participants to locate real content using their usual method, then compare it with a retrieval prototype.

### B. Contextual retrieval while working (*Knowledge Resurfacing*)

- **Hypothesised need:** Surface knowledge relevant to a current project without relying entirely on the user remembering what to search for.
- **Interview support:** Indirect; compatible with project-based workflows but not validated as a problem.
- **Risk:** Irrelevant suggestions that generate more noise and demand more attention.
- **Possible experiment:** Give a participant a real objective and observe whether suggested notes contain useful ideas they would not otherwise have found easily.

### C. Knowledge activation and assisted creation (*Knowledge Activation / Express*)

- **Hypothesised need:** Turn notes and conclusions into an article, design, presentation, or other deliverable.
- **Interview support:** No direct evidence of an unmet need; this remains the team's original vision.
- **Risk:** Becoming just another text generator and replacing some of the thinking the user wants to do themselves.
- **Possible experiment:** Support a real task with source selection, suggested connections, and an optional draft; evaluate what information actually makes it into the final result.

## 7. Conclusions

1. **The research confirms diverse workflows and problems, not a universal need.** Some people struggle to save and find notes; others consider their systems sufficiently effective.
2. **The clearest evidence of an unresolved problem concerns organisation and retrieval**, especially in e3e6's account. This should not be confused with validation of a product centred on Express.
3. **Simplicity is an important product criterion.** Oracle should integrate with existing systems and remove effort rather than become another note-management system users must maintain.
4. **Express remains a promising strategic hypothesis, but it has not been validated.** We have not demonstrated that participants need AI assistance to create, connect ideas, or produce deliverables.
5. **Technology alone is not a differentiator.** RAG, persistent memory, and contextual search already have existing implementations. The value proposition must be justified by a demonstrably better user experience.
6. **The next step should be a small, testable MVP**, rather than indefinitely extending exploratory interviews or attempting to automate the entire CODE process at once.

## 8. Recommended next steps

1. Bring **three distinct opportunities** to the team brainstorming session: simple retrieval, contextual retrieval, and assisted creation.
2. Choose **one target user**, one specific task, and one observable success criterion for the first prototype.
3. If Express is prioritised, implement a minimal workflow based on **a real project + retrieved sources + human selection + a usable result**; do not start with a generic chatbot.
4. Test the prototype with users and compare it with their usual workflow, assessing relevance, friction, time/effort, and actual use of notes in the deliverable.
5. Make uncertainties explicit and revisit the MVP direction based on observed behaviour.

### Open research question

> **When someone needs to create something using knowledge they have saved, is their main difficulty finding the ideas, connecting them, or turning them into a result? To what extent does a new tool genuinely improve their existing workflow?**

---

## References

- [Reddit thread: How often does your Second Brain actually get to “Express”?](https://www.reddit.com/r/secondbrain/comments/1x6o0vj/how_often_does_your_second_brain_actually_get_to/)
- [Reddit thread: Second Brain user in problems and building a…](https://www.reddit.com/r/secondbrain/comments/1xipx4a/second_brain_user_in_problems_and_building_a/)
- [mrz999 profile](https://www.reddit.com/user/mrz999/)
- [e3e6 profile](https://www.reddit.com/user/e3e6/)
- [vogelke profile](https://www.reddit.com/user/vogelke/)
- [Virtual_Loss6666 profile](https://www.reddit.com/user/Virtual_Loss6666/)
- [Organizing my Stuff (vogelke)](https://bezoar.org/posts/2020/0203/organizing-my-stuff/)
- [Hippocampus (GitHub)](https://github.com/marcelinollima/hippocampus)

## Exhibit I
Also Roberto has some user feedback. In addition he can get those users as as beta tester of the MVP:
- Given feedback:
```
Buenas tardes.
Yo lo que os comente, se lo pregunte a dos contactos que tengo que son profesoras de Inglés, y usan mucho Notion.
Lo que me han comentado que la idea les parece muy buena.
Les parece útil que la app sea capaz de clasificar automáticamente las tareas que va apuntando en diferentes categorías según su temática. Por ejemplo, podría identificar si una tarea es administrativa, personal, laboral o pertenece a algún tema concreto.
Sugerir cómo organizar y gestionar esas tareas, haciendo preguntas cuando sea necesario para clasificarlas correctamente.
También sería útil que pudiera detectar y recordar las tareas más urgentes o importantes, ayudando al usuario a priorizar qué debería hacer primero.
```
- You can get more context in the @./product_recap_meeting_notes.md