---
description: Build the standard CSM filter set on a project — every starter filter built and handed back as a list of links. Nothing is saved in the project.
argument-hint: "the project to build on"
---

Build the **standard CSM filter set** on the project named in the arguments, and return it as
one list of links.

Follow the `/maestra:filter-build` skill: its route (reference → draft → validation →
resolving the project's catalogue wording → build), its rules, and its batch-request reporting.
The composition of the set is fixed — take it from the skill's starter-set section, or, once the
filters wiki carries it, from `pattern.user.starter_filters`. Build exactly that set: every
item, nothing else — do not substitute, skip, or add filters of your own.

**The project.** The arguments name it. If they do not, or the named project has no filter tools
connected, ask which project to build on before anything else — never guess, and never fall back
to a default: a filter built on the wrong project silently describes a different audience.

**What is asked and what is not.** Period and channel are fixed by the set — do not ask about
them. Ask once, before building: the brand, on a multibrand project. Resolve against the
project's own catalogues: whether the 'Abandoned Checkout' status exists, what the cart product
list is called, and the state name for the geo filter. When a project lacks what an item needs,
build the item's documented fallback and say so in that item's line rather than dropping it
silently.

**One more, offered not built.** When the set is done, ask whether they also want the email-bots-by-address
segment (bots by behaviour is a separate segment — name which one you mean) — its substring list has to be looked over by a person before it is used,
so it is never added to the set silently.

**The answer** is one list — for every item: its name from the set, one sentence on what it
selects, and its link. Then, once for the whole set: assumptions, the project, and that nothing
is saved — each link's page has a "create segment" action, which is how a filter becomes a
saved segment. Do not paste the drafts or the filter JSON unless asked.
