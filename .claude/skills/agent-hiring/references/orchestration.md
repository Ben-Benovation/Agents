# Orchestration — From Employee to Department

## When to split

Split a role when any of these are true:

- The mandate needs the word "and" to be complete
- Two SOPs have fundamentally different trigger types (event-driven vs. scheduled)
- Two parts of the job need different permission tiers (one reads, one writes)
- Two parts need different failure tolerances (drafting an email vs. updating a deal value)
- The SOP list is longer than ~5 procedures

**Do not split** just because the job feels big. Split because the jobs are *different*. Three SOPs that all serve one outcome is one agent. Two SOPs serving two outcomes is two agents.

## The department pattern

```
[Manager / Orchestrator]
├── Worker A — narrow job, own dossier
├── Worker B — narrow job, own dossier
└── Worker C — narrow job, own dossier
```

**The orchestrator owns:**
- Routing: which worker handles this input
- Escalation: it is the single point of contact with the human
- Shared context: it holds the business context so workers don't each need it
- Sequencing: when Worker A's output feeds Worker B

**The orchestrator does NOT:**
- Do the work itself. If it's executing SOPs, it's a worker with delusions of management.
- Hold write permissions. Workers act; the manager decides who acts.

**Each worker still gets a full Role Dossier.** No shortcuts. A worker without guardrails is a worker that will eventually do something expensive.

## Worked example — Sales department

```
Sales Manager (orchestrator)
│  Context: BenoVation ICP, rate card, current campaigns
│  Routes on: event type
│
├── Lead Intake Agent
│     Trigger: new row on monday Leads board
│     Job: classify (Hot/Warm/Cold) + enrich (company, size, industry)
│     Tier: monday W (classification columns only)
│
├── Follow-up Agent
│     Trigger: scheduled — daily 07:00
│     Job: identify leads untouched >72h, draft outreach
│     Tier: Gmail D, WhatsApp D — draft only, never send
│
└── Quote Agent
      Trigger: manual — Ben requests a quote
      Job: assemble quote from rate card + scope notes
      Tier: Drive R, no write anywhere
      Escalates: any scope not in the rate card
```

Note the tiers differ per worker. That's the point — this is exactly what a single "sales assistant" agent could not do safely.

## Implementation in Claude Code

Map this to Subagents:
- Orchestrator = the main agent, holding the shared context
- Workers = subagents, each with its own system prompt derived from its dossier
- Episodic log = shared, written by all, read by the review process

**Watch out:** subagents cost tokens. Parallel fan-out on every input is expensive. Route to *one* worker per input unless the job genuinely requires parallel work.

## Anti-patterns

| Anti-pattern | Why it fails |
|---|---|
| Orchestrator that also executes | Nobody's watching the watchman. It'll skip its own guardrails. |
| Workers that talk to each other directly | Untraceable. When it breaks, you can't tell who decided what. |
| One shared permission set for all workers | Defeats the entire purpose of splitting. |
| A "general assistant" worker | That's the jack-of-all-trades you split to avoid. It'll grow to eat the others. |
