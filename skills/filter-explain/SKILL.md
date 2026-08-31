---
name: filter-explain
description: >-
  Explain an existing CDP filter in plain words: what selection it describes, which conditions it
  holds, and what about it cannot be read. Takes the filter as the project stores it — the JSON.
  Triggers: "explain this filter", "what does this filter do", "what does this segment select",
  "who does this selection pick".
  NOT for: building a new filter or changing one (/maestra:filter-build); datamart
  analytics — "count", "how many", a report, a metric (the `analytics_*` tools of the same
  MCP server).
argument-hint: "the filter JSON as the project stores it — paste it whole"
author: Maestra.io
---

# Filter explain

Say what an existing filter selects. The filter reaches you as machine payload — a JSON object
full of internal ids, which says nothing to a person. The project's MCP server turns it into an
intermediate, SQL-shaped query and puts the project's own names where the ids were; you turn that
into sentences.

**This skill deliberately holds no domain knowledge.** No entity or field names, no grammar, no
operator list — all of that is in `wiki`, generated outside this plugin and changing
without any edit here. What lives here is the route, the boundaries, and what may
and may not be claimed about somebody's filter.

## Three rules

1. **Nothing is invented about somebody else's project.** An internal id is not a name, an
   unfamiliar field is not a guess. What you cannot read, you say you cannot read.
2. **Tool answers document themselves.** The answer states what the result means and what to do
   next: why something was refused, whether a retry is worth it, which parts could not be read.
   Read it and do what it says — do not override it with this instruction and do not paraphrase it
   from memory.
3. **Nothing is changed.** Every tool here is read-only. Explaining a filter neither saves nor
   edits it, and the person's filter is exactly as it was before you looked at it.

## 0. Choose the project — before anything else

Names come out of **that project's** catalogues. The same id means a different brand, segment or
custom field in another project, and reading a filter against the wrong project does not fail
with an error — it produces a confident, wrong explanation.

Find the tools in your list that belong to filters (names shaped like
`mcp__<server>__filter_*`) — one set per connected project.

**None.** Say that the MCP server for the project is not connected, naming the environment and
project if the request mentioned them. Go no further: the JSON alone cannot be read into names.

**Exactly one, and the request names no other project** — name the chosen project out loud and
work with it. **In every other case ask first**, listing the connected servers and which project
and environment each stands for. Once chosen, call only that server's tools.

## 1. Get the filter itself

The tool reads **the JSON the project stores**, copied whole.

- **The person pasted JSON** — use it as it stands. Do not reformat it, do not retype it, do not
  trim it to what looks relevant: a filter reassembled by hand looks plausible and is not the
  same filter.
- **The person pasted a link to a list with a filter applied** — that link carries the platform's
  own compact form, and nothing here converts it back into the filter JSON. Say that plainly and
  ask for the JSON. Do not attempt to decode the link, and do not explain the filter from its
  URL: a guess about somebody's audience is worse than a question.
- **The filter was just built in this conversation** — use what the build returned, unedited.
- **The person refers to a filter you have never seen** ("the segment in the admin site") — ask
  for the JSON. There is no tool that lists or fetches a project's saved filters.

If the JSON is broken, the tool refuses it with wording that says what is wrong with it. Pass the
substance on and ask for a clean copy rather than repairing it yourself.

## 2. Read it back into a query

One call turns the filter into a readable query with the project's names in it. The answer is not
just the text: it says, before the query, **what about this filter could not be read**. Both
caveats change what you are allowed to say, so read them first.

- **Values that stayed internal ids.** The catalogue has no entry for them — deleted since the
  filter was saved, or below what one page of the catalogue reaches. Name them as unidentified.
  Never guess what an id meant, never present an id as a name, and never quietly drop the
  condition it belongs to: a condition on an unknown value is still a condition, and the audience
  depends on it.
- **Parts the query cannot express.** They appear as explicit markers. Their meaning is not in the
  text at all, so no reading of the text can recover it. Explain the rest, and say plainly that
  the filter also holds conditions you cannot describe. Summarising as if they were absent
  produces an explanation of a filter that does not exist.

If the tool refuses the call, its answer says whether a retry is worth it and what to tell the
person. Follow it rather than trying another route.

## 3. Understand what the conditions mean

The query is in a language with its own fields and functions, and their meaning is in `wiki` —
the same reference the building side uses. **Do not explain a field from its name.** A plausible
reading of an unfamiliar field is the one mistake in this skill nobody can catch: the sentence
sounds right and describes a different audience.

Look up what you are not sure of: the root entity — what one row of the selection *is* — and the
fields, relations and functions the query actually uses. Navigate by the ids inside documents you
have already read; there is no full-text search and ids are not to be guessed.

What the reference does not cover, you do not either. Say that a condition is there and that you
cannot describe what it checks — the honest gap in an explanation costs far less than a confident
invention in it.

## The shape of the answer

The plain-words reading comes first, because it is the whole point and the only part the person
can check. Then this order, so the report does not change from run to run.

The labels below say what each section is for; they are not text to copy. Write the whole answer —
labels included — in the language the person asked in. Half-translated headings over a translated
body read as a machine's form, and this answer is the one thing they came for.

```markdown
**Selects:** what one row of this selection is, then every condition in the person's own
  words. No syntax, no field names unless the person's own vocabulary has them.

**Could not be read** — leave the section out entirely if there is nothing in it:
  — values that stayed internal ids: which condition each sits in, and that it cannot be
    identified. Never a guess at what it meant;
  — conditions that could not be read at all: that they are there and that their meaning is
    not recoverable.

**Project:** the project and environment it was read on — the choice from step 0.
**Status:** nothing was changed; the filter is exactly as it was.
```

**The query text stays out of the answer** unless it is asked for by name — and so does the name
of the language it is written in. It is working material: its syntax is the reference's business,
not the person's, and putting either the text or its language in the answer invites them to review
something they did not ask to learn. When it is asked for, hand it over exactly as the tool
returned it.

## What not to do

- Do not present an internal id as a name, and do not guess what one referred to.
- Do not drop a condition you could not fully read — say it is there and unread.
- Do not explain a filter from a link, a screenshot or a description of it.
- Do not explain a field, function or entity from its name instead of the reference.
- Do not edit, reformat or retype what the person or the tool gave you.
- Do not say a filter is "empty" or "selects everyone" because you could not read it.
- Do not offer to fix, improve or rebuild the filter unless asked — this skill reads.
- Do not start work with the project unsettled, and do not choose it silently.
