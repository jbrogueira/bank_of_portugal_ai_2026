---
marp: true
theme: bdp
paginate: true
---

<!-- _class: title -->
<!-- _paginate: false -->

# AI Tools for Economics Research

<div class="meta">

Session 4 — Advanced use
Tuesday 23 June 2026
10:30–12:00 · 14:30–16:00
Banco de Portugal
João B. Sousa · Nova SBE

</div>

---

<!-- _class: center -->

<h4>Today</h4>

## Customising the agent for recurring research workflows.

<p class="wide">So far we've used the agent off-the-shelf. Today we configure it — for one user, then for a team.</p>

---

<!-- _class: divider -->
<!-- _paginate: false -->

<div class="num">01</div>

## Skills.

---

<h4>The problem</h4>

## You keep typing the same instructions.

<p class="wide">Every cleaning job: the same format rules, the same naming, the same stop-and-ask. Re-typing them each session is error-prone and easy to forget under time pressure.</p>

<p class="source"><code>CLAUDE.md</code> holds standing conventions. A skill packages a whole procedure.</p>

---

<!-- _class: split -->

<div>
<h4>Skills</h4>
<h2>A named, reusable procedure.</h2>

<p class="wide">A folder with a markdown file: a description of when to use it, and the steps to follow. The agent loads it when the task matches, or you invoke it by name with <code>/name</code>.</p>

<p class="source">Lives in the repo. Shared via git, like <code>CLAUDE.md</code>.</p>
</div>

<div>

<pre><code>.claude/skills/
└── clean-series/
    └── SKILL.md

---
name: clean-series
description: Align a raw
  series to monthly YoY,
  long format, with checks.
---
1. Read the raw CSV.
2. Confirm the column.
3. Compute YoY.
4. Write to processed/.</code></pre>
</div>

---

<h4>Example 1</h4>

## A dataset-cleaning skill.

<p class="wide">Encode Friday's data-cleaning procedure once: confirm the column, align frequency, compute YoY, write long-format to <code>processed/</code>, report missing-value counts. Next series, you type <code>/clean-series</code> instead of the full prompt.</p>

<p class="source">The verification steps travel with the skill — applied consistently every time.</p>

---

<h4>Example 2</h4>

## A memo-drafting skill.

<p class="wide">Default format for a results memo: section order, table format, the rule that every number cites its source file and line. Invoke it on a folder of outputs; get a draft in the same shape every time.</p>

<p class="source">Consistency across reports, without restating the style guide in every prompt.</p>

---

<h4>Which tool</h4>

## Prompt, CLAUDE.md, or skill?

<ul>
<li><strong>Prompt</strong> &nbsp; one-off, this turn only.</li>
<li><strong>CLAUDE.md</strong> &nbsp; a standing convention that holds every turn ("data/raw is read-only").</li>
<li><strong>Skill</strong> &nbsp; a multi-step procedure you repeat across sessions ("clean a series", "draft a memo").</li>
</ul>

<p class="source">Rule of thumb: if you've typed the same steps twice, write a skill.</p>

---

<!-- _class: divider -->
<!-- _paginate: false -->

<div class="num">02</div>

## Hooks.

---

<!-- _class: split -->

<div>
<h4>Hooks</h4>
<h2>Scripts the harness runs, not the model.</h2>

<p class="wide">A skill is instructions the model <em>may</em> follow. A hook is a command the harness — the program running the agent — <em>always</em> runs, on a set event, with no model involvement.</p>

<p class="source">Configured in <code>settings.json</code>. The action is any command you can run in your shell.</p>
</div>

<div>

<pre><code>events

PreToolUse   before a tool runs
             (can block it)
PostToolUse  after a tool runs
Stop         when the agent
             finishes a turn</code></pre>
</div>

---

<!-- _class: split -->

<div>
<h4>How a hook knows what happened</h4>
<h2>The harness hands the work to the hook.</h2>

<ol>
<li>The model asks to run a command.</li>
<li>The harness runs it.</li>
<li>The harness passes the details on to your hook.</li>
<li>The hook does its job — here, writes the command to a log.</li>
</ol>
</div>

<div>

<pre><code>  MODEL
    │  "run this command"
    ▼
  HARNESS
    │  runs it
    │  passes details on
    ▼
  HOOK
    │  writes to
    ▼
  session.log</code></pre>
</div>

---

<h4>The most useful first hook</h4>

## Logging, for reproducibility.

<ul>
<li><strong>Audit trail</strong> &nbsp; append every bash command to <code>session.log</code>.</li>
<li><strong>Cost tracking</strong> &nbsp; log token counts per session to a CSV.</li>
<li><strong>Edit diary</strong> &nbsp; save a record of what changed after every file edit.</li>
<li><strong>Data-access log</strong> &nbsp; record every read of <code>data/raw/</code> with a timestamp.</li>
</ul>

<p class="source">All four are PostToolUse hooks — same mechanism, different filter.</p>

---

<h4>An audit-trail hook</h4>

## <code>.claude/settings.json</code>

<pre><code>{
  "hooks": {
    "PostToolUse": [{
      "matcher": "Bash",
      "hooks": [{
        "type": "command",
        "command": "jq -r '.tool_input.command' >> session.log"
      }]
    }]
  }
}</code></pre>

<p class="source">Every bash command the agent runs lands in <code>session.log</code>.</p>

---

<h4>Same mechanism, other triggers</h4>

## Checks and formatting are hooks too.

<ul>
<li><strong>PreToolUse</strong> &nbsp; before a write, run the formatter — or block an edit to a protected path.</li>
<li><strong>Pre-commit checks</strong> &nbsp; run the test suite before a commit is allowed.</li>
<li><strong>Guardrails</strong> &nbsp; refuse any command that edits <code>data/raw/</code> in place.</li>
</ul>

<p class="source">A hook can block the action, not just observe it. This is how you enforce <code>CLAUDE.md</code> rather than only request it.</p>

---

<!-- _class: takeaways -->

<h4>End of morning</h4>

## Where we are.

<ol>
<li><strong>Skills package a procedure</strong> — a named, multi-step workflow the agent runs on demand, shared via git.</li>
<li><strong>Hooks run deterministically on events</strong> — no model involvement; they observe or block.</li>
<li><strong>Together they move conventions from "asked" to "enforced"</strong> — the difference between <code>CLAUDE.md</code> and a hook.</li>
</ol>

<p class="source">Next: subagents, MCP, and a shared team setup.</p>

---

<!-- _class: center -->
<!-- _paginate: false -->

<h4>Break</h4>

<div class="big">14:30</div>

<p class="lede">Back after lunch.</p>

---

<!-- _class: divider -->
<!-- _paginate: false -->

<div class="num">03 · AFTERNOON</div>

## Subagents.

---

<!-- _class: split -->

<div>
<h4>Subagents</h4>
<h2>A delegated task with its own context.</h2>

<p class="wide">The main agent spawns a subagent, hands it one task, and gets back only the result. The subagent's context — the files it read, the dead ends — never enters the main session.</p>

<p class="source">Protects the main context from the noise of a search.</p>
</div>

<div>

<pre><code>main session
  │
  ├─ subagent: search
  │    reads 40 files
  │    returns 1 answer
  │
  └─ context stays clean</code></pre>
</div>

---

<!-- _class: split -->

<div>
<h4>Why its own context matters</h4>
<h2>The reading happens elsewhere.</h2>

<p class="wide">Each subagent has a separate context window. It reads the source there — and only its short answer crosses back. The main agent's context fills with results, not raw material.</p>

</div>

<div>

<pre><code>stays in the subagent
  the full abstracts
  the files it opened
  the dead ends

crosses back
  one table</code></pre>
</div>

---

<h4>Why delegate</h4>

## Three reasons.

<ul>
<li><strong>Protect context</strong> &nbsp; a wide search reads many files; only the conclusion comes back.</li>
<li><strong>Parallelism</strong> &nbsp; independent subtasks run at once — search three folders simultaneously.</li>
<li><strong>Focus</strong> &nbsp; a subagent with one job and a narrow tool set is harder to derail.</li>
</ul>

---

<h4>When it pays</h4>

## And when it doesn't.

<ul>
<li><strong>Helps</strong> &nbsp; broad read-only search, parallel tasks, anything that floods the main context.</li>
<li><strong>Doesn't</strong> &nbsp; a small task — the overhead exceeds the work.</li>
<li><strong>Doesn't</strong> &nbsp; sequential dependence — if step 2 needs step 1's reasoning, keep them together.</li>
</ul>

<p class="source">Default to one agent; reach for subagents when the work is wide.</p>

---

<!-- _class: split -->

<div>
<h4>Live demo</h4>
<h2>Literature triage, parallelised.</h2>

<p class="wide">Nine abstracts in three topic folders. One subagent per folder, each returning a <em>question · method · data · finding</em> table. The main session merges three tables — the nine abstracts never enter it.</p>

<p class="source">Each subagent's misreads stay local.</p>
</div>

<div>

<pre><code>papers/litreview/
├── monetary/  ┐
├── fiscal/    ├─ one subagent
└── labour/    ┘  each → a table

  main session
    merges 3 tables,
    not 9 abstracts</code></pre>
</div>

---

<h4>Live demo</h4>

<p class="wide"><strong>1. Single agent, one context:</strong></p>

<pre><code>Read every abstract under papers/litreview/
and build one comparison table.</code></pre>

<p class="wide"><strong>2. One subagent per folder:</strong></p>

<pre><code>For each folder in papers/litreview/, spawn a
subagent that reads the abstracts and returns a
table — columns: question · method · data · finding.
Then merge the three tables into one.</code></pre>

<p class="source">Same corpus, both prompts. Compare the main session's context after each.</p>

---

<!-- _class: divider -->
<!-- _paginate: false -->

<div class="num">04</div>

## MCP and external tools.

---

<!-- _class: split -->

<div>
<h4>MCP</h4>
<h2>A standard plug for external tools.</h2>

<p class="wide">Model Context Protocol: a common interface between the agent and an outside service. Install a server once; its tools become available to the agent, like the built-in file and shell tools.</p>

<p class="source">One protocol, many servers — the agent needs no bespoke code per service.</p>
</div>

<div>

<pre><code>agent
  │
  ├─ GitHub      official
  ├─ Git         official
  ├─ Fetch       official
  ├─ Zotero      community
  └─ filesystem  built in</code></pre>
</div>

---

<h4>Useful servers</h4>

## For a research workflow — all community-built.

<ul>
<li><strong>Reference manager</strong> &nbsp; Zotero — search your library, pull citation keys, stage new references.</li>
<li><strong>Data sources</strong> &nbsp; pull a FRED or Eurostat series by code, without leaving the session.</li>
<li><strong>Paper search</strong> &nbsp; query Google Scholar or Semantic Scholar for the literature pass.</li>
</ul>

<p class="source">None of these is an official vendor server — they are third-party projects. See the next slide before connecting one.</p>

---

<h4>Before you connect one</h4>

## Two things to weigh.

<ul>
<li><strong>Trust</strong> &nbsp; a server runs code and can send your data to a third party; one that fetches outside content can carry hidden instructions that try to hijack the agent. Read what it does before connecting.</li>
<li><strong>Clutter</strong> &nbsp; connect the servers you use, not every one available — each adds tools the agent has to weigh.</li>
</ul>

<p class="source">Tool definitions load on demand; the context cost is small.</p>

---

<!-- _class: divider -->
<!-- _paginate: false -->

<div class="num">05</div>

## A small team workflow.

---

<h4>Shared toolkit</h4>

## The configuration is just files in the repo.

<ul>
<li><strong>CLAUDE.md</strong> &nbsp; shared conventions — paths, tools, house style.</li>
<li><strong>Skills</strong> &nbsp; the team's standard procedures — clean a series, draft a memo.</li>
<li><strong>Hooks</strong> &nbsp; the team's guardrails — audit log, protected data, pre-commit tests.</li>
</ul>

<p class="source">Committed to git. A new team member clones the repo and inherits the whole setup.</p>

---

<!-- _class: center -->

<h4>The path</h4>

## Start with one file. Grow from use.

<p class="wide">Begin with a <code>CLAUDE.md</code>. When you've typed the same steps twice, write a skill. When a convention must hold without exception, write a hook. Commit each. The shared config is the common workflow of the team, in version control.</p>

---

<!-- _class: takeaways -->

<h4>End of course</h4>

## Three ideas to conclude.

<ol>
<li><strong>Skills and hooks turn one-off prompts into shared infrastructure</strong> — procedures you invoke, guardrails that always run.</li>
<li><strong>Subagents handle width</strong> — broad search and parallel work, with the main context kept clean.</li>
<li><strong>The whole setup is files in git</strong> — <code>CLAUDE.md</code>, skills, hooks. Clone the repo, inherit the workflow.</li>
</ol>

<p class="source">Four sessions: what an agent is, what it does, where it fails, how to shape it.</p>

---

<!-- _class: title center -->
<!-- _paginate: false -->

# Thank you.

<div class="meta">

joao.sousa&#64;novasbe.pt

</div>
