# General-purpose AI assistants and DIY setups as alternatives to an AI note organization assistant (state as of 2026-11-09)

Evidence labels used in these notes: **[Official]** = vendor documentation or vendor help page. **[Vendor marketing]** = vendor blog or customer story, or a third party selling something adjacent. **[User report]** = first-person account or GitHub issue. **[Secondary]** = third-party guide or aggregator. All pages were consulted on 2026-11-09. Many pages were read through a summarizing fetch tool or search excerpts, so quotes marked [search excerpt] should be rechecked before they are presented publicly. Dates are the source's own, where it shows one.

## Can Claude, ChatGPT, Gemini and Microsoft Copilot read AND write a Notion workspace today, and reorganize notes at scale? At what cost and with what limits?

### Takeaway
Read and write access to Notion is now mostly a commodity, because Notion publishes a remote MCP server with page, move and database tools that any MCP client can use. Claude is the most clearly documented and cheapest route for an individual. ChatGPT's access depends on the plan and is partly unclear. Gemini and Copilot are documented mainly as enterprise routes. I found no vendor that documents or guarantees reorganization "at scale". API rate limits are not the main barrier for a personal workspace. The harder limits are approval steps, reliability and the lack of a review or undo workflow.

### Cited Findings

**Summary table (detail and sources below)**

| Assistant | Read Notion | Write Notion | Move pages documented? | Entry price found | Confidence |
| --- | --- | --- | --- | --- | --- |
| Claude | Yes | Yes | Yes, through Notion MCP tool | $0 is possible for a connector; Claude Code from Pro at $20/mo | High for capability; medium for the Free plan |
| ChatGPT | Yes | Yes "where supported", plan terms unclear | Not confirmed for the ChatGPT app | Not verified | Medium to low |
| Gemini | Enterprise: yes. Consumer: no native connector (vendor blog) | Enterprise: create/update page and database | Not listed among the actions | Not verified | Medium for Enterprise; low for consumer |
| Microsoft Copilot | Yes, Notion is in the gallery | General write support since Oct 2026; Notion-specific tools not confirmed | Not confirmed | Requires a Microsoft 365 Copilot license; price not verified | Medium to low |

**Notion MCP (the shared foundation)**
- [Official] Notion MCP lets assistants search a workspace, create and edit pages, manage databases, save memories and use reusable Notion Skills. Notion names Claude, ChatGPT and Gemini as examples and says any MCP client can connect. Admins can manage MCP clients. The page is undated. — [Notion MCP overview](https://developers.notion.com/docs/mcp)
- [Official] The tool list includes `notion-move-pages` ("Put pages in a different location"), `notion-update-page` ("Update a page's content and properties"), `notion-update-data-source` ("Update the fields and page layout of a data source"), `notion-search`, `notion-fetch`, `notion-delete-pages` and `notion-restore-pages`. — [Notion MCP FAQs and tool list](https://developers.notion.com/guides/mcp/tools-faqs)
- [Official] "Some tools and parameters also depend on the workspace plan or the connection's capabilities", but the page does not say which ones. `notion-get-tool-access` shows what a given connection can use. — [Notion MCP FAQs and tool list](https://developers.notion.com/guides/mcp/tools-faqs)
- [Official] Connection limit: 180 requests per minute (about 3 per second) in general and 600 per minute on Business and Enterprise. A separate workspace-wide limit also applies, and data source queries are limited to about 3 per second per connection. — [Notion request limits](https://developers.notion.com/reference/request-limits)
- [Official] Every MCP tool call counts toward the standard limits. MCP retries once if the wait is 2 seconds or less and otherwise returns a `rate_limited` error. Notion says the limits may change. — [Notion MCP rate limits](https://developers.notion.com/guides/mcp/rate-limits)
- [Official] The changelog contains both a statement that tool-specific MCP limits were removed and an older entry with a limit of 30 searches per minute. I treat the removal as current, but the order of the entries was not fully confirmed. — [Notion changelog](https://developers.notion.com/page/changelog)
- [Official, search excerpt] Page writes can return a 504 timeout, and "a 504 does not mean the write was undone", so a client must check whether the change was saved before retrying. The excerpt covers content updates, not moves. — [Notion changelog](https://developers.notion.com/page/changelog)
- [Secondary] `notion-delete-pages` moves at most 20 pages to Trash per call. I did not confirm this figure in official documentation. — [Creators Toolbox](https://creatorstoolbox.com/blog/notion-delete-pages-and-databases-in-notion-mcp)
- [User report, opened 2026-02-15] In Claude Desktop (Cowork mode) with the remote Notion connector, `notion-update-page`, `notion-create-pages` and `notion-move-pages` rejected object parameters with a validation error. The reporter's workaround was moving pages by hand in the Notion UI. The issue had 7 thumbs-up reactions and was still shown as open, with the last comment on 2026-03-17 and a proposed fix in PR #234. Whether it still reproduces in November 2026 is unverified, so this should not be presented as a current bug. — [GitHub issue #209](https://github.com/makenotion/notion-mcp-server/issues/209)

**Claude**
- [Official] The directory connector can search and read a workspace, create and update pages, add entries to databases and save chat output as pages. It connects to `https://mcp.notion.com/mcp`. The listing warns that Anthropic does not control or verify third-party connector tools. — [Claude Notion connector](https://claude.com/connectors/notion)
- [Official] Custom remote MCP connectors are available on Free, Pro, Max, Ultra, Team and Enterprise, across Claude, Cowork and Claude Desktop. Free users are limited to one custom connector. — [Anthropic custom connector help](https://support.claude.com/en/articles/11175166-get-started-with-custom-connectors-using-remote-mcp)
- [Official] Pricing: Free $0 (connectors yes, up to 5 Projects, no Claude Code). Pro $20/mo monthly or $17/mo billed annually. Max $100/mo. Ultra $200/mo. Team $20/seat billed annually or $25 monthly (standard). Connectors are shown on all of these plans. — [Claude pricing](https://claude.com/pricing)
- Conflict on Cowork plans: the fetched pricing summary listed Cowork only under Team, while the [Anthropic help article](https://support.claude.com/en/articles/11175166-get-started-with-custom-connectors-using-remote-mcp) mentions connectors in Cowork across plans and a [third-party page](https://claudecowork.com/connectors/notion) says Cowork comes with paid plans. Treat individual-plan Cowork availability as not fully verified.
- Conflict on Free: several [Secondary] guides say Notion is unavailable on Free, including [Skills Playground](https://skillsplayground.com/connectors/notion/). The official pages above show connectors on Free. No official page I found states directly whether adding Notion from the directory on Free counts against the one-connector limit.
- [Secondary] OAuth inherits access to all pages the connected user can reach, so scope should be restricted at connection time. — search result set including [Elite AI Advantage](https://eliteaiadvantage.com/how-to/claude-mcp-notion-workspace); the exact originating page was not pinned down.

**ChatGPT**
- [Official, 2026-03-29] Updated Notion app rolled out to ChatGPT, Business and Enterprise/Edu, adding actions "including write capabilities where supported". The post names no specific Notion actions and does not break down consumer tiers. — [OpenAI community announcement](https://community.openai.com/t/updated-box-notion-linear-and-dropbox-apps/1378101)
- [Official, older design] The legacy synced Notion connector lists no write actions and is superseded for new users by the app in the directory. — [OpenAI help: Notion synced connector](https://help.openai.com/en/articles/12532955-notion-synced-connector)
- [Official, search excerpt only; direct fetch returned 403] Full custom MCP including writes is limited to Business and Enterprise/Edu on web. Pro can connect custom MCP only for read/fetch. Free and Plus are not mentioned. Write actions may ask for confirmation, and some risky actions may be blocked. Deep research can use only read/fetch actions. — [OpenAI help: custom MCP in ChatGPT](https://help.openai.com/en/articles/12584461-developer-mode-and-mcp-apps-in-chatgpt)
- [Official, October 2025, older] Apps launched for Free, Go, Plus and Pro outside the EEA, Switzerland and the UK. This matters for a Spain-based team, but current EU availability was not verified. — [OpenAI apps announcement](https://openai.com/index/introducing-apps-in-chatgpt/)
- [User report] Developer community threads report custom MCP being removed or greyed out for Plus and write calls being blocked. — [Write actions blocked thread](https://community.openai.com/t/write-actions-blocked-on-custom-mcp-server-business-plan-workspace-developer-mode-unavailable-at-workspace-level/1384381)
- [Vendor marketing, 2026-11-03] Notion says a 16-person distributor had ChatGPT build a CRM in Notion from a photo of a contact sheet and generate an SOP library. This shows writes happening in practice, but it is new-content creation rather than reorganization, and the plan used is not stated. — [Notion blog](https://www.notion.com/blog/mcp-use-cases)

**Gemini**
- [Official] The Gemini Enterprise Notion data store supports federated search and "search and actions" modes, with actions to create comments, create and update databases, and create and update pages. It is available only in Global, US and EU locations. Status and licensing were not stated on the fetched page. — [Google Cloud docs](https://docs.cloud.google.com/gemini/enterprise/docs/connectors/notion)
- [Vendor marketing] The consumer Gemini app and Gemini Spark have no native Notion connector, Spark offers a custom MCP option, and writes require manual confirmation. Enterprise admin details are also given. I did not confirm these with Google. — [Carly blog](https://www.usecarly.com/blog/how-to-connect-multiple-notion-workspaces-to-gemini/)

**Microsoft Copilot**
- [Official, last updated 2026-10-28] Federated connectors can read and, "where a connector provides the tools", create, update or delete with user approval. Notion is listed in the gallery under Productivity. A user needs a Microsoft 365 Copilot license and admin enablement. The Researcher agent stays read-only. — [Microsoft Learn: federated connectors](https://learn.microsoft.com/en-us/microsoft-365/copilot/connectors/federated-connectors-overview)
- [Official] Write tools default to "Needs approval", with per-tool choices of Allow once, Allow for conversation or Always allow. — [Microsoft Learn: federated connectors](https://learn.microsoft.com/en-us/microsoft-365/copilot/connectors/federated-connectors-overview)
- [Official, 2026-09-21, now expired notice] Write, update and delete support rolled out worldwide from early to late October 2026. Notion is not named, and available actions depend on the publisher's tools. — [Message Center MC1476316](https://mc.merill.net/message/MC1476316)
- [Vendor marketing, 2026-07-16, likely outdated] A blog says Copilot cannot write to Notion. It predates the October rollout and quotes a Microsoft "read-only" line that the current Microsoft page no longer uses. — [Carly blog](https://www.usecarly.com/blog/microsoft-copilot-notion-integration/)

### Inferences
- **Rate limits are not the main barrier for an individual.** If each note took 3 calls (fetch, update, move), 1,000 notes would be 3,000 calls, or about 17 minutes at 180 requests per minute, and 5,000 notes would be about 83 minutes. This is a lower bound from my own arithmetic and ignores model latency, context size and errors. It was not measured.
- **The likely barriers are operational.** A batch of per-page writes runs into approvals (Copilot, ChatGPT), ambiguous partial failure (504 responses) and model context. Those are inferred from the documented behaviors above, not from a measured test.
- **"Do nothing new" is strongest for Claude users.** It offers documented read, write and move tools at low cost. A reusable Notion Skill could hold a PARA prompt, which further reduces the setup a dedicated product would save.
- **Consumer Copilot and Gemini users have a much weaker DIY path.** The documented routes need enterprise licensing or a custom MCP setup. This is an inference from the official pages describing enterprise products.

### Gaps
- No official statement was found on the maximum number of pages per `notion-move-pages` call, or on which tools depend on the Notion plan.
- Current ChatGPT prices and exact Notion app write actions per tier were not verified. Prices for Gemini Enterprise and Microsoft 365 Copilot were not verified either.
- Notion-specific write tools in Copilot could not be confirmed. Microsoft's page confirms the mechanism and that Notion is in the gallery, not that the Notion connector exposes them.
- Nobody on this research task ran a hands-on test. A short test (for example, 200 notes in a test workspace through Claude) would replace much of this inference with evidence.

## Do real examples exist of people reorganizing a Notion or Obsidian vault with Claude, Claude Code or ChatGPT? What worked and what failed?

### Takeaway
Yes, but the evidence is uneven. The most concrete personal example is on Obsidian (6,000+ notes in two sessions), where notes are local files. The strongest Notion example is a vendor customer story about migrating into Notion, and it took weeks of human review. I found no first-hand account of reorganizing an existing personal Notion workspace at scale, and written reports rarely describe failures, so success bias is likely.

### Cited Findings
- [User report, published 2026-03-07, updated 2026-03-25] Stefan Imhoff reorganized a vault of more than 6,000 notes with Claude Code into Zettelkasten and PARA folders, in two sessions of about 2 to 3 hours each. He also automated asset cleanup, link updates, metadata and new note types, and later created skills for maintenance. His `pages` folder remained unsorted and cleanup was ongoing. He reports no specific failures and does not describe git or backups for the vault or how metadata accuracy was checked. — [Stefan Imhoff](https://www.stefanimhoff.de/agentic-note-taking-obsidian-claude-code/)
- [User report, 2026-03-06] Kenneth Reitz runs Claude Code over 467 markdown files in numbered PARA-inspired folders, steered by a CLAUDE.md of about 200 lines that includes "Do not create new files unless explicitly asked". His use is mainly analysis and pattern-finding rather than restructuring. He has Obsidian Git installed and follows a rule that Claude suggests while he verifies. He reports no failures or measurements. — [Kenneth Reitz](https://kennethreitz.org/essays/2026-03-06-obsidian_vaults_and_claude_code)
- [Vendor marketing, 2026-11-03] Dance Academy of Virginia had Claude audit every Google Drive file and propose a location for it. The director reviewed the least critical files first and marked reviewed pages with an emoji. The migration covered hundreds of files and took about 2.5 weeks, against an estimated six months without Claude. The figures are self-reported in a Notion marketing post, and the case is a migration into Notion for an organization, not a personal note cleanup. — [Notion blog](https://www.notion.com/blog/mcp-use-cases)
- [Vendor marketing, 2026-11-03] Elevision consolidates scattered workflows into versioned "Agent SOP" pages through Notion MCP. — [Notion blog](https://www.notion.com/blog/mcp-use-cases)
- [User report, February 2026] On Notion, a Claude Desktop user could not use the move tool and moved pages by hand (status today unverified). — [GitHub issue #209](https://github.com/makenotion/notion-mcp-server/issues/209)
- [Secondary] A how-to warns that a query paginating through 500 pages at about 3 requests per second "will be slow and may fail", and recommends pre-filtering with database views. It reports no test data. — [Elite AI Advantage](https://eliteaiadvantage.com/how-to/claude-mcp-notion-workspace)
- [User report, search excerpt; page refused the connection on fetch] One author says repeated vault reorganizing meant "rearranging the same mess into a different shape". The excerpt is not about AI specifically. — [Organizing an Obsidian Vault](https://ibrah5em.duckdns.org/notes/deep-dives/organizing-obsidian-vault)
- [Secondary] An ecosystem of starter kits and skills exists for this DIY path, including [Claudesidian](https://cdn.jsdelivr.net/gh/heyitsnoah/claudesidian@main/README.md) and a listed [PARA skill](https://skillstore.io/skills/scifishelf-para-skill). Their quality and adoption were not assessed.

### Inferences
- **Recurring success pattern:** explicit instruction file (CLAUDE.md), staged human review, low-risk items first, and reusable skills or maintenance routines. Oracle would need to deliver these without asking users to build them.
- **Obsidian is the easier DIY target.** Local files allow scripts and direct edits, and optional git. Notion goes through API calls and rate limits, which fits Oracle's choice to start on Notion as the less served path. This is an inference from the sources, not a measured comparison.
- **The reports come from technical, motivated users.** Imhoff and Reitz both describe technical setups (CLI tools, plugins, instruction files). That is exactly who a product does not need to win first, and Roberto's contacts (English teachers on Notion, see [user_interviews.md](../../user_interviews.md)) are not that profile.
- **The speed claims need careful wording.** Dance Academy took 2.5 weeks, not one prompt, which suggests review is the real work and a better review experience could be the opening for a product.

### Gaps
- I found no first-hand Reddit or blog post describing reorganization of an existing personal Notion workspace with Claude or ChatGPT at scale, in success or failure. The search tool found no such thread, which does not prove none exist. Direct Reddit searching would be worthwhile.
- No error rates for AI classification of personal notes were found, and no follow-up reports on whether a reorganized structure lasted after several months.
- The title ["The AI Knowledge Graph That Killed PARA"](https://www.mejba.me/blog/infinite-brain-knowledge-graph-ai) suggests a move away from PARA, but the page was not read in full.

## How common are Zapier, Make and n8n templates that classify Notion entries with AI, and how difficult are they to set up?

### Takeaway
They are easy to find, especially on Zapier, where almost exactly the classification the Notion-using teachers asked for already exists as a template. However, they mostly act on new entries one at a time. They do not restructure a backlog or hold a clarifying conversation, and they require accounts, a prepared database and ongoing usage costs.

### Cited Findings
- **Zapier** [Official template pages] Listed templates include [categorize new Notion entries with ChatGPT and update database items](https://zapier.com/templates/details/9b6f4da8c1a9a8a27fa439491d417414e3a96258b0e4bae94f319a6f134a119e), [categorize and tag new Notion notes with AI analysis](https://zapier.com/templates/details/c044bc9ee21498b8cda78dcdaa4ae89485d256990d0ef54f38429a5bcd00c34b) and [categorize and update text data in Notion](https://zapier.com/templates/details/8ce285b3c769b73ba60a2cfcea293c841001199421d06783e213cb7dcd495f4b). The second needs Notion and AI by Zapier. Task usage, plan and install counts were not shown on the page.
- **n8n** [Community templates on the official site] [Notion AI summary & tags (4431)](https://n8n.io/workflows/4431-notion-ai-summary-and-tags/) adds a summary and tags to new rows, working from saved URLs, and needs prepared columns. [Slack to Notion auto-tagging (4502)](https://n8n.io/workflows/4502-starred-slack-messages-to-notion-database-with-ai-auto-tagging/) assigns only existing tags at 90% confidence or more [search excerpt]. [Feedback tagging (3689)](https://n8n.io/workflows/3689-analyze-and-tag-user-feedback-in-notion-with-gpt-4-sentiment-analysis/) needs a preconfigured Notion template.
- **n8n, human approval** A template title shows approval steps are buildable, in a lead-qualification use case. — [n8n 10025](https://n8n.io/workflows/10025-automate-interior-design-lead-qualification-with-ai-and-human-approval-to-notion/)
- **Make** [Secondary, independent site with affiliate links] A guide rated "Intermediate" requires Make, Notion, Airtable and an OpenAI API key, plus two related Notion databases and a Relation property. It uses JSON-mode output and a formula to write relation IDs. It says Make's starter plan is free with 1,000 operations per month, and each run uses operations and API credits. — [Make Notion AI classify guide](https://make-cfpage.pages.dev/en/workflows/make-notion-ai-classify)
- **Make** [Secondary] A third-party marketplace also lists a Notion to ChatGPT template that writes results back. — [GrowwStacks](https://growwstacks.com/workflows-make.com/11450-send-notion-items-to-chatgpt-and-update-your-database-with-the-results/)

### Inferences
- **Directly relevant competition for the teachers' request.** Roberto's contacts want tasks classified by topic (administrative, personal, work). A Zapier template can do roughly that for new database entries. Oracle's advantage is not classification itself.
- **Likely gaps in automations:** backlog cleanup across existing pages, moving pages across a hierarchy, clarifying questions and a single review queue. The templates I reviewed do not advertise these. A determined builder could add parts of them, as the approval template suggests.
- **Setup is moderate for builders and high for everyday users.** Database property preparation, API keys and JSON output are the sticking points. I did not time an install.

### Gaps
- No total count or install numbers were found for any of the three platforms, so "common" rests on what one search returned: several Zapier templates, several n8n templates and fewer Make resources.
- Current Zapier, Make and n8n pricing was not checked against official pricing pages. The Make figures come from an unaffiliated site.
- I found no first-hand reports on classification quality or on abandoning these automations.

## How well do non-AI alternatives work, such as PARA templates, weekly reviews, plain files and search, according to practitioners?

### Takeaway
They can work very well for disciplined users, and two people in the team's own evidence are satisfied or functional with simple routines. The recurring failure point is sustained maintenance (reviews get skipped, and people stall over which category fits), not the filing method itself. This evidence is largely opinion, and much of it comes from authors with something to sell.

### Cited Findings
- [Team interview, Oct–Nov 2026] vogelke uses Unix directories, keyword filenames and `locate`, reporting searches under four seconds over more than nine million files and no significant friction. mrz999 empties two inboxes daily into tasks, reminders, time blocks or deletion. e3e6 sometimes writes nothing because they do not know where to put it, and cannot find what they saved. — [user_interviews.md](../../user_interviews.md)
- [User report, article dated 2023-04-28 with examples from February 2020; older information] vogelke's shared article documents years of failed category schemes (ambiguous placement, a catch-all "Misc" folder, 658 email folders) before settling on a date-based notebook, automation with cron, and the principle "Search, don't categorize". This is the opposite of Oracle's premise. — [Organizing my Stuff](https://bezoar.org/posts/2020/0203/organizing-my-stuff/)
- [User report, May 27, year not shown, likely 2026] A PARA user reports running weekly notes for over a year, with a 10 to 15 minute Friday checklist. — [hackastak on DEV](https://dev.to/hackastak/weekly-notes-beat-daily-notes-the-sustainable-way-to-never-forget-anything-kj2)
- [Opinion, 2026-05-09, updated 2026-09-05] Antoine Buteau describes a "taxonomy trap" in which people spend more time deciding categories than working. He recommends placing a note where the next piece of work will need it, and keeping one copy. He says people abandon PARA after about six months, but gives no data. — [Antoine Buteau](https://www.antoinebuteau.com/personal-productivity-and-knowledge-management-series-4-para-taxonomy-and-the-myth-of-the-perfect-place-for-everything.md)
- [Opinion] Buteau also has a companion essay arguing that the weekly review is the system and is often skipped. — [Antoine Buteau](https://www.antoinebuteau.com/personal-productivity-and-knowledge-management-series-3-the-weekly-review-is-the-system-and-youre-probably-skipping-it.md)
- [User report, search excerpt] Past a threshold, the cost of a weekly review exceeds what a reasonable person will absorb, so this author moved to short daily reviews. — [Goryugo](https://goryugo.com/en/review/)
- [Vendor marketing; Fabric sells an AI second-brain product] Second-brain systems typically die when the weekly review is skipped, and PARA drifts as completed projects stay unarchived. — [Fabric: why second brains fail](https://developers.fabric.so/blog/why-second-brains-fail); [Fabric: PARA yearly review](https://fabric.so/learn/para-yearly-review)
- [Vendor marketing, 2026-04-11; sells StackMind] PARA sorts on only one axis, so bug fixes, AI conversations, snippets and decisions lack a natural home for developers. — [Stackbench](https://stackbench-web.pages.dev/writing/why-the-para-method-doesnt-work-for-developers/)

### Inferences
- **The problem Oracle targets is plausibly real but not universal,** matching the split in the team's interviews. Practitioner consensus points to upkeep and decision friction more than to lack of a framework.
- **PARA should not be imposed as the fixed structure.** Boundary ambiguity is the most common complaint. Asking when unsure and placing a note by its next use may fit better than choosing among four categories.
- **Oracle has to beat "simple system plus habit" on effort,** not on sophistication. A tool that adds review work could lose to vogelke's and mrz999's routines.

### Gaps
- No reliable data was found on PARA or weekly-review abandonment rates. The "six months" figure is unsupported opinion.
- The search tool surfaced no first-hand Reddit threads on abandoning PARA. A blog in the result set mentions Reddit complaints that PARA is incomplete in Notion, but I could not attribute this reliably, so it should not be used without checking.
- I did not evaluate individual PARA template products. No usage or retention data for them was found.

## What is Hippocampus, what similar open-source memory tools exist, and do they address organizing at all?

### Takeaway
Hippocampus is a very young, small project that gives coding agents long-term memory. It is not a tool for organizing a user's Notion or personal notes. Similar tools mostly serve agent memory and retrieval, which relates more to the postponed Express and assistant ideas than to the MVP. They only organize notes within their own stores.

### Cited Findings
- [Official repository, GitHub API on 2026-11-09] Hippocampus was created on 2026-09-27 and last pushed on 2026-11-03. It has 7 stars and 0 forks, and uses the MIT license. — [Hippocampus](https://github.com/marcelinollima/hippocampus)
- [Official repository] It stores memories as Markdown indexed in SQLite and offers hybrid search (BM25, local vectors, graph of `[[links]]`), recall hooks on each prompt, an optional end-of-session review hook, statuses (active, pending, resolved, superseded), MCP tools and a web UI. Setup is local with Python 3.10+ or on a small VPS with a domain and token. — [Hippocampus](https://github.com/marcelinollima/hippocampus)
- [Official repository] Organizing applies within its own store: a folder per project, plus a type and status per memory. The README does not mention Notion or Obsidian integration. It imports Claude Code memory folders. — [Hippocampus](https://github.com/marcelinollima/hippocampus)
- [Official repository, GitHub API on 2026-11-09] Basic Memory has 4,541 stars, was last pushed on 2026-11-08 and uses AGPL-3.0. — [Basic Memory on GitHub](https://github.com/basicmachines-co/basic-memory)
- [Official docs, search excerpt] Basic Memory keeps Markdown files locally, readable in Obsidian or any editor, and has a Claude Code plugin with session briefings and checkpoints. — [Basic Memory docs](https://docs.basicmemory.com/start-here/why-basic-memory); [README](https://cdn.jsdelivr.net/gh/basicmachines-co/basic-memory@main/README.md)
- [Secondary, comparison pages from vendors] Other options named include Mem0 (a memory layer for apps and agents, with a warning that its OpenMemory component is being sunset), Graphiti, MemCP and the reference MCP memory server. I did not verify these against their repositories. — [Hjarni comparison](https://hjarni.com/blog/best-mcp-memory-server.md); [Unabyss comparison](https://unabyss.com/blog/best-memory-mcp-servers-claude)
- [Official] Notion MCP itself saves private memories that can be recalled across connected clients, which reduces the need for a separate memory tool. — [Notion MCP overview](https://developers.notion.com/docs/mcp)

### Inferences
- **These tools are not direct competitors to an organization assistant.** They help an agent remember what it has done and retrieve Markdown. None of the sources I read describes categorizing or moving an existing Notion workspace.
- **They are relevant to Oracle's postponed features.** Claims that memory or RAG are differentiators remain weak, matching conclusion 5 in the team's interviews: this technology already exists.
- **Hippocampus is weak evidence of demand.** At 7 stars and about six weeks old, it shows that one person built it and one Reddit user recommended it. Basic Memory shows larger interest in agent memory, though stars do not measure use.

### Gaps
- I did not read each memory tool's documentation in depth, so a niche capability for reorganizing notes could have been missed.
- Actual usage of Hippocampus beyond its GitHub numbers is unknown.
