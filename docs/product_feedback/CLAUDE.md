## Product feedback goal
The goal of this phase of the Oracle product development is to demonstrsate that we have identified a concrete problem before start building.
To achieve that goal, we need to generate a comprehensive markdown document for illustrationg the product feedback learning of the works done in this product feedback phase.

## Final artifact format
- We need a comprhensive markdown file that summarize the work done and the achieved conclussions and what we have learned
- We will need to present the content of this document publically in about 10 minutes. We need o presentation for doing that
- The content of both markdown and presentation must be in spanish
- You must follow the plan steps listed in @./PLAN.md
- The final document is @./product_feedback.md

## Scope of this phase
- The artifacts of this phase redefine the scope of the whole project.
- `docs/PRODUCT_BRIEF.md`, `docs/SPEC.md`, `docs/CLOUD_DESIGN.md` and the current code are history and starting context, not constraints. Use them to explain where we come from and what could be reused.
- Do not update those files during this phase.
- The 8-week window in `docs/PRODUCT_BRIEF.md` does not apply for now, so do not treat it as a limit on the MVP.
- The team's limited availability of a few hours per week still applies and does limit the MVP.

## Evidence rules
- Keep user reports, team interpretations and hypotheses clearly separated.
- Name the source of each finding. The sample is small and not representative, so never present a finding as true for the majority of users.
- The feedback from Roberto's contacts is second-hand and is about tasks, not notes. Label it that way.
- PARA comes from the team and from the proof of concept, not from what users said.

## Team responsibilities in the final document
- Imanol adds the AI justification.
- Roberto does the last review and redaction.


## Work that has been done
1. We have identified a concrete target user:
Our initial target user is a 'second brain' system user, or a systematic notetaker who is having difficulties in organizing the information, or keeping it up to date, or using/retieving it when doing meaningful work

2. Interview at least one or two potentian users:
We have post a subreddit in the 'Second brain' Reddit community and we had some conversations with different users to understant their difficulties and what are they doing to solve them. Additionally, we have personally talked with some Notion users that have suggested to us some interesting features. Additionally, the are available to act as beta testers of the MVP
There is more context of this user feedback in @./user_interviews.md

-----------------------
Note: At this point, the Oracle team had a meeting to put results in common and keep in track. The notes of this conversation are in @./product_recap_meeting_notes.md
-----------------------

3. Investigate competitors or alternatives.
Not done yet

4. Document our hipothesys based on our learning.
We have some initial hipothesys, but we need to refine them based on point 3:
- Some users have trouble trying to organize notes. May be a organization assistant, based on second brain (PARA) categories may be helpful
- We need to offer somthing differento to existing solutions like Notion AI, obsidian or Claude as an asisstant
- The 'Express' phase (recover relevant information Just-In-Time when working in a relevant project) has a big potential, but for the MVP, the organization phase is prioritary because seems to be tha main problem for majority of the users
- An assistan chatbot could be unvaluable, but it is not the main focus of the MVP

5. Decide what functionallity we are building for the MVP, what are we modifying and what are we discarding. If the functionallity is going to use AI, explain Why.
- The organization assistan is the functionallity we are building first because it seems to be the main pain for the users when taking notes.
- We are modifying the initial scope that was centered in the 'express' phase. This phase will be postposed for later development and instead of a simple contextual searcher, it will be a work assistant for relevant projects
- A contextual chatbot assistant will also be postposed
- AI will act as assistant for notes categorization and orgqanization. Imanol will revisit this AI features later.
- This initial guidelines could be midified in the future, depending on the market feedback
