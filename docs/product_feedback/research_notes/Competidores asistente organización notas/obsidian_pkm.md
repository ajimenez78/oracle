# Obsidian with AI plugins and structured PKM apps as competitors for an AI note organization assistant (state as of 2026-11-09)

Evidence labels used below: **[Official]** = vendor docs, pricing, repo or registry data. **[Vendor claim]** = marketing or positioning language. **[User report]** = forum post or GitHub issue. **[Third party]** = independent review, directory or press. **[Rival vendor]** = published by a company selling a competing app, so low trust. All pages and statistics were read on 2026-11-09 unless a date is given.

## Obsidian: which AI organizer plugins matter, what do they do, are they maintained, how many users, and is there native AI?

### Takeaway
Reach and organizing function do not overlap. The two biggest AI plugins (Copilot, Smart Connections) are not organizers, while the most direct organizer (Note Companion, about 44k downloads) is inbox-centered and small by comparison. Obsidian has no native AI assistant that I could find, but it now ships an official CLI that makes generic coding agents a real alternative for reorganizing a vault.

### Cited Findings

**Plugin scoreboard.** Downloads are cumulative counts from the official registry, read 2026-11-09 ([community-plugin-stats.json](https://raw.githubusercontent.com/obsidianmd/obsidian-releases/master/community-plugin-stats.json)). "Last release" is the registry timestamp, converted to a date. Descriptions are from the [official plugin list](https://raw.githubusercontent.com/obsidianmd/obsidian-releases/master/community-plugins.json), which holds 10,161 plugins.

| Plugin | Downloads | Last release | Role for organizing | Relevance |
|---|---:|---|---|---|
| Copilot | 3,367,227 | 2026-11-03 | General chat and agent, no dedicated organizer | High (substitute) |
| Smart Connections | 1,265,240 | 2026-08-06 | Surfaces related notes, does not move or tag | Medium (adjacent) |
| Text Generator | 593,657 | 2026-04-27 | Text generation; organizing role not checked | Marginal |
| Auto Note Mover | 127,706 | 2022-04-16 | Rule-based moves, no AI; stale | Marginal (shows demand) |
| Note Companion (ex File Organizer 2000) | 43,800 | 2026-10-24 in registry | Folder, tag, title and format suggestions | High (direct) |
| Auto Classifier | 17,261 | 2025-07-10 | Tags via ChatGPT API | Marginal |
| AI Tagger Universe | 16,835 | 2026-09-07 | AI tags with review | Medium (narrow) |
| AI Tagger | 14,686 | 2024-12-27 | One-click AI tags; stale | Marginal |
| Auto Tag | 9,513 | 2023-11-19 | Generates tags; stale | Marginal |
| Metadata Auto Classifier | 8,648 | 2026-11-04 | Classifies and applies metadata | Marginal |
| PARA Shortcuts | 8,081 | 2024-02-24 | PARA commands; stale | Marginal |
| PARA Workflower | 4,536 | 2026-11-01 | PARA commands | Marginal |
| Vaultend | 2,594 | 2026-08-02 | Classify, tag, link with per-note review | Low reach, closest to Oracle's concept |
| AI Organiser | 2,481 | 2026-10-26 | Broad AI toolkit including vault auto-tagging | Marginal |
| AI Organizer | 608 | 2026-09-17 | Inbox sorting, batch processing | Marginal |
| OpDoc AI Auto Organizer | 590 | 2026-05-20 | Local Ollama, inbox tag and move | Marginal |
| Tagged | 77 | 2026-10-07 | Uses existing tags, optional filing | Marginal |

**GitHub activity** ([GitHub API](https://api.github.com), read 2026-11-09):
- Copilot: 7,968 stars, 207 open issues, release 4.0.18 on 2026-11-03 — [repo](https://github.com/logancyang/obsidian-copilot).
- Smart Connections: 5,550 stars, 497 open issues, release 4.7.2 on 2026-08-06, last push 2026-10-10 — [repo](https://github.com/brianpetro/obsidian-smart-connections).
- Note Companion: 874 stars, 6 open issues, release 3.6.40 on 2026-11-08, commits on 2026-11-09. The latest commits are about audio and recorder flows into the inbox. Repo dates from 2023-09 and now sits under the Nexus-JPF organization — [repo](https://github.com/Nexus-JPF/note-companion).

**Note Companion**
- [Official] Suggests folder, tags, title and formatting for raw notes or links dropped into an Inbox folder, or applies them automatically — [README](https://github.com/Nexus-JPF/note-companion), [plugin page](https://community.obsidian.md/plugins/fileorganizer2000).
- [Official] Also does transcription, YouTube capture, vault chat and meeting recording, so organizing is only part of the product — [README](https://github.com/Nexus-JPF/note-companion).
- [Official] Cloud needs a paid subscription with a 7-day trial; self-hosting is free with your own keys. Desktop only, and the mobile app is paused — [README](https://github.com/Nexus-JPF/note-companion). I could not verify a price: the [pricing URL](https://www.notecompanion.ai/pricing) I tried returned 404.
- [Official] The site describes the plugin as "auto-organizing inbox notes" — [notecompanion.ai](https://notecompanion.ai).

**Copilot**
- [Official] Agent Chat runs OpenCode, Claude Code or Codex against the vault; its docs list no dedicated organizing feature — [docs](https://docs.obsidiancopilot.com/).
- [Official] Agents can edit notes and rename them with links updated through the Obsidian CLI. Three permission modes (Safe, Plan, Auto). A "Files changed" card gives before-and-after views and a Revoke action — [agent docs](https://docs.obsidiancopilot.com/agent-mode-and-tools/).
- [Official] The Free plan needs no account and works with your own keys or local models. Lite, Plus and Supporter are paid; prices are not on the docs page — [plans](https://docs.obsidiancopilot.com/copilot-plus-and-self-host/).

**Smart Connections**
- [Official] Ships a local embedding model and surfaces semantically related notes. Headline promises time saved on "linking, tagging, and organizing", but the features described are surfacing, dragging links and sending context. No move or tag function is described — [README](https://cdn.jsdelivr.net/gh/brianpetro/obsidian-smart-connections@main/README.md).
- [Official] Core is free and source-available; Pro plugins go to project supporters — [README](https://cdn.jsdelivr.net/gh/brianpetro/obsidian-smart-connections@main/README.md).

**Narrow taggers and small organizers**
- [Third party, 2026-05-26] AI Tagger Universe suggests tags that the user validates or rejects — [Anthem Creation](https://anthemcreation.com/en/artificial-intelligence/ai-plugins-obsidian-2026-comparison/).
- [Official, plugin docs, read via search snippets] Vaultend's Organize Folder suggests tags and links per note, reviewed in a side panel, with nothing changed until "Apply All" — [wiki](https://github.com/dhwang0803-glitch/Vaultend/wiki/Organize-Note), [plugin page](https://community.obsidian.md/plugins/vaultend).
- [Official] AI Organizer covers inbox sorting, batch processing and metadata. Its own page says generated moves and edits should be reviewed before use on important vaults — [plugin page](https://community.obsidian.md/plugins/ai-organizer).
- [Official, read via search snippet] Tagged preserves manual tags and keeps its folder move off by default — [plugin page](https://community.obsidian.md/plugins/tagged).
- [Vendor claim, author's forum post] Vault Audit AI (posted 2026-08-08) flags orphan notes, tagging problems and overlapping topics. No reactions visible — [forum](https://forum.obsidian.md/t/vault-audit-ai-audit-and-organize-your-obsidian-vault-with-ai/117080).

**Native AI and official posture**
- [Official] The pricing page does not mention AI. Sync costs $4 per user per month billed annually, and the app is free — [pricing](https://obsidian.md/pricing).
- [Third party, 2026-05-26] "Obsidian still doesn't include any native artificial intelligence: everything is through community plugins" — [Anthem Creation](https://anthemcreation.com/en/artificial-intelligence/ai-plugins-obsidian-2026-comparison/).
- [Official] Obsidian 1.12.7+ has a CLI with `move` (can update internal links), `rename`, `tags` and `property:set`. The app must be running. The page does not present it as an AI feature; it only says developer commands let agentic coding tools test and debug — [CLI help](https://obsidian.md/help/cli).
- [Official repo] kepano/obsidian-skills has 51,215 stars, last push 2026-09-15 — [repo](https://github.com/kepano/obsidian-skills). [Third party, search snippet only] It is described as built by Obsidian CEO Steph Ango — [overview](https://claudeskills.info/blog/obsidian-claude-skills-guide/). I did not confirm this on a primary page.

### Inferences
- The most relevant Obsidian competitors for the team are Note Companion (direct) and Copilot plus generic coding agents (substitutes). Smart Connections matters as adjacent discovery, not organizing.
- 51k stars on the agent skills repo, against 874 on Note Companion, suggests technical users may lean toward generic agents over dedicated organizers. Stars and downloads measure different audiences, so this is only a signal.
- Downloads are cumulative and are not active users. They should be quoted only as relative reach.
- PARA-specific plugins found are command helpers with no AI in their descriptions. I found no plugin that combines AI with PARA as its stated purpose, though I did not review all 10,161 listings.

### Gaps
- No official Obsidian statement on native AI found. The absence is inferred from a third-party article and the pricing page. A [Remio post](https://www.remio.ai/post/obsidian-power-users-push-back-as-ai-note-apps-get-simpler) mentions native local embedding support, but [Rival vendor] and not confirmed anywhere.
- No active-user data exists for any plugin.
- Prices for Copilot paid plans, Note Companion Cloud and Smart Connections Pro are unverified. A January 2026 discussion quotes Smart Connections Pro at $10 per month or $99 per year, which may be out of date ([mirror of discussion #1294](https://github-users.yhajoa.workers.dev/brianpetro/obsidian-smart-connections/discussions/1294)).
- Text Generator's organizing role and Periodic PARA (now "LifeOS", 54,135 downloads) were not examined beyond registry data.

## Structured PKM apps: what AI organization features exist today, what do they cost, and how much traction do they have?

### Takeaway
None of the apps reviewed documents an assistant for reorganizing an existing base. Capacities comes closest (property autofill and reviewable AI edits). Tana has moved toward meetings, and Heptabase, Logseq and Anytype lean on external AI through MCP or remain experimental.

### Cited Findings

| App | Priced from (read 2026-11-09) | AI organization today | Traction found | Relevance |
|---|---|---|---|---|
| Capacities | Free without AI; Pro $9.99/mo | Property autofill, assistant edits | No figures | Medium, closest |
| Tana | Free; Pro $15/member/mo yearly | AI builds structure, now for meetings | $25M raised (2025) | Medium, drifting away |
| Heptabase | Pro $8.99/mo | Chat, actions, MCP write access | No figures | Low |
| Logseq | Pricing not checked | No built-in AI found | 45,530 GitHub stars | Marginal |
| Anytype | Pricing not checked | Experimental local agent | 9,064 GitHub stars (desktop repo) | Marginal |

**Capacities**
- [Official] Basic is free with no AI. Pro is $9.99/mo, Believer from $12.49/mo, and the Plus add-on $8.33/mo billed annually adds AI budget. The page's structured data shows different figures (Pro $11.99/mo, Believer $14.99/mo) — [pricing](https://capacities.io/pricing).
- [Official] AI fills properties such as author, genre and year. Image, PDF and weblink analysis add metadata such as category or keywords. Each note shows its five closest notes. Connectors let ChatGPT or Claude create objects and change properties — [Pro page](https://capacities.io/pro).
- [Official] Assistant edits can be reviewed one by one or auto-approved, and version history can undo them — [Pro page](https://capacities.io/pro).
- Conflict: a search summary said the Pro page describes AI suggesting tags and collections with user approval, but my direct read of [the same page](https://capacities.io/pro) found no such text. Treat tag suggestion as unverified.
- [Official, 2026-05-19] Release 65 says the assistant can better break down complex tasks, but does not mention reorganizing — [release](https://capacities.io/whats-new/release-65).

**Tana**
- [Official] Free at $0 with about 50 AI queries. Pro $15 per member per month billed yearly, with about 20x the queries. Business from $35 per member per month. The plans are framed around meetings and teams — [pricing](https://tana.inc/pricing).
- [Official, May 2026] Tana split into a new meetings-focused product at tana.inc and a separate Tana Outliner with its own team and roadmap (split decided 2026-03-16). In the new product, AI builds structure from a described workflow and changes pass through proposal and approval — [Tana Current](https://outliner.tana.inc/blog/tana-current-may-2026).
- [Third party, February 2025, older data] $25M total funding and a 160k waitlist, the latter a company claim — [TechCrunch](https://techcrunch.com/2025/02/03/tana-snaps-up-25m-with-its-ai-powered-knowledge-graph-for-work-racking-up-a-160k-waitlist).

**Heptabase**
- [Official] Pro $8.99/mo with a Gemini-only agent and 100 credits. Premium $17.99/mo with 1,800 credits. Premium+ $53.99/mo with 8,100 credits. Yearly billing saves 25% — [pricing](https://heptabase.com/pricing).
- [Official, undated] AI uses cards and whiteboards as context and offers AI actions on cards. MCP lets external AI read, search and write. No tagging, moving or reorganizing by AI is described — [Work with AI](https://wiki.heptabase.com/work-with-ai).

**Logseq**
- [Official repo] 45,530 stars, active on 2026-11-09 — [repo](https://github.com/logseq/logseq).
- [Third party] Logseq 2.0 Beta (DB version) reportedly dates from 2026-07-13, with a data loss warning — [Kompozy](https://kompozy.io/news/logseq-2-0-db-version-beta). The DB version reportedly has no built-in AI model but offers an optional MCP server — [PromptQuorum](https://www.promptquorum.com/power-local-llm/logseq-review). Not confirmed against Logseq's release notes.

**Anytype**
- [Official, February 2026, older] Prototyping a local agent with the user's own API key, described as "early and experimental". The stated goal is a choice of no AI, local, cloud or hybrid — [community update](https://blog.anytype.io/february-community-update-2026/).
- [Official] An MCP server exists — [repo](https://github.com/anyproto/anytype-mcp). Activity on the desktop client is current — [repo](https://github.com/anyproto/anytype-ts).
- Conflict: [one directory](https://devtoollab.com/ai-tools/anytype) lists auto-tagging, while other comparisons say Anytype has no assistant. The official update supports "not shipped as a core feature as of February 2026".

### Inferences
- Capacities is the app to watch. Its review-and-undo flow is close to what Oracle proposes, but the documented AI fills properties rather than recategorizing a base.
- Tana's pivot means it is less of a direct competitor for individual second brain users than its reputation suggests. Its proposal-and-approval pattern is still a useful reference.
- Logseq and Anytype are marginal for this comparison. Heptabase is marginal for organizing, although MCP means an external agent could in principle act on it.
- MCP access shifts part of the competition to general assistants (Claude, ChatGPT) connected to these apps, not only to the apps' own AI.

### Gaps
- No reliable user or revenue figures found for Capacities, Heptabase, Anytype or Logseq, and none after early 2025 for Tana.
- Tana Outliner's current pricing and AI features were not verified. Access status is also in conflict: a [DEV review](https://dev.to/pickuma/tana-review-an-outliner-based-pkm-tool-that-thinks-in-graphs-8l8) reports a waitlist in mid-2026, while the [May 2026 post](https://outliner.tana.inc/blog/tana-current-may-2026) says the new product is with community members.
- Logseq and Anytype pricing not checked, given their marginal relevance.
- Heptabase's [wiki page](https://wiki.heptabase.com/work-with-ai) is undated and I could not read its roadmap.
- Saner.AI, Mem and Reflect were outside the products I examined. Saner.AI is pitched as replacing manual organizing ([Saner.AI's own blog](https://www.saner.ai/blogs/logseq-review), [Rival vendor]) and may deserve its own check.

## For each tool: does it reorganize existing notes or only classify new ones, does it require migration, and does it support human review?

### Takeaway
No tool reviewed documents the full pattern of a dedicated, reviewable reorganization of an existing base that also asks clarifying questions. Plugins and agents avoid migration but only for Obsidian users, and PKM apps need the notes to live inside them. Review is now common, so it does not differentiate on its own.

### Cited Findings

Verdicts come from the sources cited in the sections above and below. "Not documented" means I found no statement either way, not that the feature is absent.

| Tool | Existing notes? | Migration? | Human review? |
|---|---|---|---|
| Note Companion | Mainly inbox items; bulk existing not documented | No, if already on Obsidian | Suggestions or auto-apply; review flow not documented |
| Copilot / agents | Yes in practice, by prompt; no organizer workflow | No, if on Obsidian | Yes: permission modes and diff, with gaps |
| Smart Connections | Reads all notes, changes nothing | No, if on Obsidian | Not applicable |
| AI Tagger Universe | Tags only; scope not verified | No, if on Obsidian | Yes, per suggestion (third party) |
| Vaultend | Yes, by folder (tags and links) | No, if on Obsidian | Yes, per note |
| AI Organizer | Batch and inbox | No, if on Obsidian | Advised on its page; flow not documented |
| Capacities | Fills properties; recategorizing not documented | Yes | Yes for assistant edits |
| Tana (new) | Not stated | Yes | Yes, for structure proposals |
| Heptabase | Not documented in-app; MCP writes possible | Yes | Not documented |
| Logseq / Anytype | Not documented | Yes | Not documented |

- [Official] Note Companion's page does not mention batch processing of existing notes — [plugin page](https://community.obsidian.md/plugins/fileorganizer2000).
- [User report, 2026-06-25] A feature request says all Inbox pipeline steps "run unconditionally", with no per-step toggles. The issue is now closed; I did not verify what shipped — [issue #468](https://github.com/Nexus-JPF/note-companion/issues/468).
- [Official] Copilot's change card is "a review aid rather than a complete audit", and changes made through shell commands are not listed — [agent docs](https://docs.obsidiancopilot.com/agent-mode-and-tools/).
- [Official] Capacities offers per-change review or auto-approve — [Pro page](https://capacities.io/pro).
- [Official] Tana's structure changes go through proposal and approval — [Tana Current](https://outliner.tana.inc/blog/tana-current-may-2026).

### Inferences
- The open space is narrower than "AI that organizes notes". It is a guided, whole-base reorganization, with PARA as a framework, clarifying questions and batch review. I found this combination documented nowhere in this segment.
- Oracle starting on Notion avoids direct overlap with Obsidian plugins, but also means this group does not serve Oracle's first users. The Notion AI comparison, covered separately, matters more for the MVP.
- Vaultend is a useful product reference despite low reach, because it validates folder-level proposals with per-note review.

### Gaps
- I did not install or test any tool, so all verdicts come from documentation and reports. Real behavior on a messy base is unverified.
- I found no tool that documents asking clarifying questions when unsure about a category, but I did not search for this exhaustively and generic agents can do it when prompted.

## What documented limitations and user complaints exist about organizing notes with these tools?

### Takeaway
Complaint evidence is thin and I retrieved no Reddit threads. What exists points to three themes: unmet demand for approve-each-move filing, trust and pricing friction in plugins, and risk from agents acting on a vault without rollback.

### Cited Findings

**Unmet need and workarounds**
- [User report, 2026-05-12] A user with "catch all" notes holding hundreds of pasted URLs wants an LLM to route each item to its proper note, ideally locally, approving each move. The only reply suggests Codex in a terminal — [Obsidian forum](https://forum.obsidian.md/t/help-finding-a-workflow-for-organizeing-notes-using-a-llm/114174).
- [User report, October-November 2024, older] A user wanting automatic filing could not find a plugin. After being pointed to Smart Connections, File Organizer, Copilot and Khoj, they said these were "not well enough suited" — [Obsidian forum](https://forum.obsidian.md/t/my-dream-ai-to-auto-categorize-and-sort-new-notes/90188).

**Agent risk**
- [User report, 2026-05-12] Codex makes "a big mess" unless told to ignore `.obsidian`, and sometimes makes changes unless told to wait for confirmation — [Obsidian forum](https://forum.obsidian.md/t/help-finding-a-workflow-for-organizeing-notes-using-a-llm/114174).
- [Third party, 2026-05-26] Recommends versioning the vault with Obsidian Git before an agent rewrites many notes, because otherwise there is no reliable rollback — [Anthem Creation](https://anthemcreation.com/en/artificial-intelligence/ai-plugins-obsidian-2026-comparison/).
- [Official] Copilot says the vault is "the agent's working directory, not a security sandbox" — [agent docs](https://docs.obsidiancopilot.com/agent-mode-and-tools/).

**Trust, pricing and access**
- [User report, 2026-06-08] A user called Note Companion's bring-your-own-key advertising "scam behavior" because the shipped plugin offered no such setup. The maintainer accepted the complaint, corrected the docs and closed the issue. BYOK still needs a self-hosted backend — [issue #464](https://github.com/Nexus-JPF/note-companion/issues/464).
- [User report, 2026-01-29] A user objected to Smart Connections' unannounced move from GPL to a modified license and to Pro pricing. The maintainer conceded the change should have been better flagged and defended the price. Read through a mirror, not on GitHub itself — [discussion #1294 mirror](https://github-users.yhajoa.workers.dev/brianpetro/obsidian-smart-connections/discussions/1294).
- [Official] Note Companion is not available on iOS or Android — [README](https://github.com/Nexus-JPF/note-companion).
- [Third party, 2026-05-26] Local indexing is heavy on mobile — [Anthem Creation](https://anthemcreation.com/en/artificial-intelligence/ai-plugins-obsidian-2026-comparison/).

**AI-first apps (low trust)**
- [Rival vendor, June 18, year not stated, probably 2026] Claims apps that auto-organize notes cost users folder control, broke links and lost metadata in migration. No app, person or forum is named, so this should not be cited as evidence — [Remio](https://www.remio.ai/post/obsidian-power-users-push-back-as-ai-note-apps-get-simpler).

**PKM apps**
- [Third party] Logseq's DB beta carries a data loss warning — [Kompozy](https://kompozy.io/news/logseq-2-0-db-version-beta).

### Inferences
- The May 2026 forum post is the closest match to Oracle's concept found here: item-level routing with approval. It is one person, so it illustrates the need rather than sizing it.
- Safety features (preview, approval, undo, ignoring system folders) look like table stakes for any tool that writes to a user's notes.
- Clear pricing and data flow may be a cheap differentiator, given the friction reported in both leading plugins.

### Gaps
- No Reddit evidence. Searches aimed at r/ObsidianMD, r/PKMS and r/secondbrain returned no threads, so user sentiment there is unverified and should not be assumed either way.
- I found no reports of wrong categorization accuracy. A search of Note Companion's issues for "wrong folder" returned nothing. That does not show accuracy is good, since few users may report it there.
- No independent benchmark or comparative test of AI organizing quality was found. Most 2026 comparison articles found were SEO-style or vendor-written, so I used them sparingly.
- Complaint evidence for Capacities, Tana and Heptabase's AI organizing was not found in the sources I read.
