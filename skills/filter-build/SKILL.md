---
name: filter-build
description: >-
  Build a CDP filter (a selection of customers, products or actions; the basis of a segment)
  from a natural-language request: the filters-domain reference → draft → validation →
  resolving the project's catalogue wording → a link to the list in the project, and the filter
  itself on request.
  Triggers: "build a filter", "make a segment", "select customers who",
  "who bought X in the last N days", "filter by products",
  "starter filters".
  NOT for: datamart analytics — "count", "how many", a report, a metric, ClickHouse SQL
  (the `analytics_*` tools of the same MCP server); explaining a filter that already exists
  (/maestra:filter-explain).
argument-hint: "who to select — e.g. customers with a confirmed email who bought Nike in the last 90 days"
author: Maestra.io
---

# Filter build

Build a CDP filter from a natural-language request. The domain lives in the project's MCP
server: the `wiki` tool holds the filter language and the entity catalogue, the `filter_*`
tools do validation, catalogue lookups and building.

**This skill deliberately holds no domain knowledge.** No entity or field names, no grammar,
no operator list — all of that is in `wiki`, generated outside this plugin and
changing without any edit here. A copy would inevitably drift from its
source and silently teach outdated syntax. What lives here is the route, the boundaries and the
shape of the answer.

## Three rules

1. **Knowledge comes from `wiki`, not from memory.** Fields, relations, operators, document
   ids, catalogue names. What is not in a document you have read does not exist — do not
   extrapolate by analogy.
2. **Tool answers document themselves.** The answer already states what the result means and
   what to do next: why something was refused, whether a retry is worth it, what to ask the
   person, why there is no link. Read the tool's answer and do what it says — do not override it
   with this instruction and do not paraphrase it from memory.
3. **The filter is not saved.** The domain's tools are read-only: building returns the finished
   filter but creates and changes nothing in the project. Never report "the filter is ready",
   "the segment was created", or "saved".

## Checklist

Keep a checklist of steps 0–3 and tick off what is done. Keep the count of rebuild rounds in the
checklist rather than in your head: the rule "after this, ask the person" depends on it.

## 0. Choose the project — before anything else

**The skill's first action.** Do not read the reference, do not write a draft and do not call a
single tool until it is settled which project you are building on.

Almost everything depends on the project: its own catalogues (brands, categories, segments,
custom fields), its own set of available filters, its own data and its own link. The same name
exists in one project and not in another, and a filter built on the wrong project does not fail
with an error — it silently describes a different audience. So the project is **never chosen by
default and never guessed**.

Find the tools in your list that belong to filter building (names shaped like
`mcp__<server>__filter_*`) — one set per connected project.

**None.** Say that the MCP server for the project is not connected, naming the environment and
project if the request mentioned them. The user knows how MCP is connected — do not invent a
command or an address. Go no further: without a server there is nothing to build with.

The server needs network access and rights to the project — it authorises the user, not the
skill. So "the server is connected but no tools appeared" is nearly always access
rather than the request: have the user check their rights on the project. If the tools are there
but answer with a refusal, that is the **refusal** branch below, where the tool itself says
whether it is access or the service.

**The project is unambiguous** — exactly one server is connected and the request names no other
project or environment. Name the chosen project out loud in your first answer and work with it.

**In every other case, ask — and it is the first question, before any other work.** It is
ambiguous when:

- more than one server is connected, whether those are different projects or one project across
  environments;
- the request names a project or environment and the connected server is not it, or it is
  unclear whether it is;
- the server's name does not clearly say which project it stands for.

When asking, list the connected servers and which project and environment each one stands for.
Once chosen, call **only that server's** tools — never mix answers from different servers into
one filter. Keep the chosen project in the checklist and name it in the final report.

## 1. Take the building instructions

Start from the `filters` domain reference — the `wiki` tool. Its index lists what is there.

You need at least two kinds of material, both before writing a draft: the **step-by-step
building procedure** and the **grammar** of the language. The procedure is the source of truth
for step 2 — what to take as the root, how to split the request into predicates, how to group
conditions. The grammar is what that split is written in. If the index holds anything else
relevant to the task, take that too.

If the reference does not have what the work relies on, stop and say that the reference and the
skill have diverged. Improvising here is not allowed: the route rests on it.

There is no full-text search: you navigate only by the id links inside documents you have
already read, and the tool prints the canonical id of whatever it found. **Do not guess ids** —
follow the links until you reach the fields, relations and worked recipes you need.

You read a lot and out of order, so **write a short summary immediately after reading**: what
you took as the root, the canonical ids you read, the available fields and relations, the recipe
that fits. You will need it for the report. But the source is the documents, not the summary: if
you are unsure of a name or an operator, re-read the document instead of extrapolating from your
own notes.

## 2. Work the procedure through to a valid result

From here follow **the procedure from the reference**, not the steps of this instruction. It
names the tools and the order itself — including checking the draft and turning catalogue values
into the project's own wording. Take exact tool names, arguments and permitted values from the
tool schemas; they are deliberately absent here so that this file cannot drift from the server.

The skill adds only what the procedure does not carry — the boundaries:

- **the draft does not pass the check** — go back to the reference for the right field, operator
  or construct instead of patching blindly. And do not weaken a condition to make a draft pass:
  the audience changes. If it cannot be expressed, say so plainly rather than substituting
  something similar.
- **catalogue values did not match** — the answer lists them with a reason and hands back
  ready-made lines for asking again. Work through its text and retry, **two rounds at most**.
  After that ask the person instead of cycling through wordings.
- **a refusal or a service failure** — the answer states whether retrying is worth it and what
  to tell the person. Follow it.

## 3. Return the link

**By default hand over the link alone.** It is the artefact a person can act on: it opens the
selection in the project, shows who fell into it, and is where the filter becomes a saved
segment. The filter itself is machine payload — long, unreadable, and useless to somebody who
only wanted the audience.

**The draft never goes in the answer.** The query you wrote is working material: its syntax is
the reference's business, not the person's, and pasting it invites them to review a language
they did not ask to learn. Say what the filter selects in their own words instead — that
sentence is what they check, and it is the only place they can catch a misread request. Show
the draft only if it is asked for by name.

Hand the filter itself over in two cases only:

- **it was asked for** — either in so many words, or by what they said they would do with it:
  pass it on, store it, feed it to something else;
- **there is no link** — then it is all there is, and the answer's reason for the missing link
  goes with it.

Whatever you hand over, take it **from the tool's answer as it stands**: do not edit or reformat
it and do not retype it from memory; do not construct a link yourself. There may be no link — the
answer then says why, and that reason is to be quoted, not filled in by guesswork. If the answer
notes that the filter can be saved as a segment from that page, pass that on: otherwise the
person is left one click short of what they asked for.

**An answer with no filter in it has no filter to hand over.** The build can end without one even
though the draft was fine — the platform has to confirm the assembled filter, and when it cannot
be reached nothing has validated it. The answer says so, and says whether to retry. There is
nothing to substitute in that case: not the draft, not a filter from an earlier build, not one
written out by hand. Report what the answer says and stop — a filter no backend agreed to, handed
over as the result, is the one failure here nobody downstream can detect.

## When to ask the person

`wiki` describes a procedure for an autonomous service that has nobody to talk to. You do have
somebody — so ask, but **only at forks where different readings produce different audiences**.

Choosing the project does not fall under this rule: it is not a fork but the mandatory gate of
step 0, and ambiguity there always stops the work.

The forks worth asking about:

- two plausible roots with different meanings for the selection (entity pages carry "use when /
  do not use when" sections — read those first and ask only if they do not settle it);
- a catalogue value is ambiguous — the project holds several entries under that name and the
  draft does not say which;
- a second rebuild round still did not match;
- the request sets no boundary that the selection depends on, and there is no sensible default.

Decide the rest yourself and record it as an assumption: an unstated but obvious period, a
choice between equivalent phrasings of a predicate.

If part of the request cannot be expressed as a filter, name which part, and hand over the
subset you did build, saying honestly how it is broader or narrower than what was asked. Whether
such a selection will do is the person's call. Dropping an inexpressible condition silently is
not allowed: the filter would look right and select the wrong audience. Nor is substituting
something else for it — people come for a filter in order to act on the selection.

## The shape of the answer

The link comes first. Then this order and content, so that the report does not change from run
to run.

The labels below say what each section is for; they are not text to copy. Write the whole answer —
labels included — in the language the person asked in. Half-translated headings over a translated
body read as a machine's form, and this answer is the one thing they came for.

```markdown
**Filter:** what falls into the selection, in the person's own words — every condition
  that made it in, none of the syntax. This is the only thing they can check, so it
  carries the whole burden of catching a misread request.

**Link** — exactly as the tool returned it.
  — if the answer explains why there is no link, quote the reason; do not invent a link;
  — if it notes that the filter can be saved as a segment, say so.

**The filter itself** — only if it was asked for, or if there is no link.
  Exactly as the tool returned it. Otherwise leave the section out and say nothing
  about it; mention it is available on request only if they seem to want it.

**Assumptions:** what you decided yourself instead of asking; "none" if there were no forks.
**Project:** the project and environment it was built on — the choice from step 0.
**Status:** not saved — the result still has to be applied by whatever saves filters.
```

## Batch requests

A request may name a set of filters rather than one. Each item of the set walks the full
route on its own — draft, check, resolve, build — but the report is one list, not a stack of
full reports: for every item its name, the one-sentence description of what it selects, and
the link. Assumptions, the project and the not-saved status are stated once for the whole set.

<!-- ========================= TEMPORARY BLOCK =========================
     Remove everything between these markers once the filters wiki ships
     `pattern.user.starter_filters` — the wiki then carries this set and
     the skill must not duplicate it. The "Batch requests" section above
     and the starter-filter trigger phrases in the description STAY.
-->

## TEMP: the starter set — "main filters"

Until the wiki documents the starter set, its composition lives here. When asked for the
"main / popular / key filters", "standard segments", or "starter filters" — build the
standard CSM set.

**The set is thirteen filters, and all thirteen get built.** By name, in order:

```
Engaged 30D Email · Engaged 90D Email · Engaged 180D Email
Engaged 30D SMS · Engaged 180D SMS
Abandoned Carts 30D · Recent Purchasers 30D
Inactives · Email Bounces
Subscribed to Email · Subscribed to SMS
In-Stock Products · Texas Customers
```

Build exactly these — do not substitute, skip, or add filters of your own. Each is its own
filter with its own link, named exactly as above: those names are what the segments get saved
under. **A filter you cannot build gets a line saying so and why — never silent omission.**
Two of them are the ones most easily dropped, so they are stated outright:

- **In-Stock Products** is a PRODUCT filter — its root is the product, not the customer, and
  its link opens the product list. A different root is not a reason to leave it out of a
  "customer segments" answer: it is part of the set on every project.
- **Texas Customers** is part of the set too. Being geo-specific is not a reason to skip it,
  and neither is the link-length caveat below — build it, hand over what the tools returned,
  and add the caveat to its line.

**Before answering, count.** Go through the thirteen names above against the answer you are
about to send; if a name has no line, go back and build it. An answer that quietly holds
eleven filters is the failure this section exists to prevent.

The composition of each:

1. **Engaged 30D Email**, **Engaged 90D Email**, **Engaged 180D Email** — activity OR-block
   over the window (site visit, message open, message click, order, registration), AND the
   email hygiene block: valid email; no hard bounces (Mailbox full / Address does not exist)
   ever; no email bounces in the last 14 days. Do NOT add an email subscription condition —
   email subscriptions differ per brand (topics etc.) and are filtered at send time.
2. **Engaged 30D SMS**, **Engaged 180D SMS** — the same activity OR-block, AND the SMS
   hygiene block: valid mobile phone; an ACTIVE subscription to the SMS channel (mandatory —
   SMS subscription is global, per channel); no SMS bounces in the last 14 days.
3. **Abandoned Carts 30D** — (an order whose line status is 'Abandoned Checkout' — the
   standard Shopify-integration status, CANCELLED category — OR added to the cart product
   list in the window and the product is still in the list) AND no order with line status
   category placed/paid/delivered in the same window.
4. **Recent Purchasers 30D** — an order in the last 30 days whose first action falls in
   the window AND at least one order line with status category placed/paid/delivered, both
   inside ONE order scope (the status condition is what keeps abandoned checkouts out).
5. **Inactives** — more than 12 emails received and zero opens, AND no orders in the last
   180 days, AND no site visits in the last 30 days.
6. **Email Bounces** — hard bounces (Mailbox full / Address does not exist) ever, OR any
   email bounces in the last 14 days, OR email present but invalid.
7. **Subscribed to Email** — an ACTIVE subscription to the Email channel AND a valid email
   AND no hard bounces (Mailbox full / Address does not exist) ever AND no email bounces in
   the last 14 days.
8. **Subscribed to SMS** — an ACTIVE subscription to the SMS channel AND a valid mobile
   phone AND no SMS bounces in the last 14 days.
9. **In-Stock Products** — the standard PRODUCT filter, needed on every project: not an
   unknown product AND available (in stock) AND price above 1 AND has an image. Its root is
   the product, not the customer, so it is built and linked as a product selection.
10. **Texas Customers** — the customer's Area name equals 'Texas' OR the mobile phone starts
   with any of the Texas area codes (see the geo section below for the full list, which must
   be used whole). Mind the link-length caveat below.

After the set is built, OFFER one more segment rather than building it unasked: **Email Bots
by Address** — an OR block of `user.email CONTAINS` over suspicious substrings, AND no
order with line-status category placed/paid/delivered ever. Starting substring list: botmail,
+, test, johnsmith, xyz, junk, spam, mail.codisto.com, bounce-, tiktok, amazon.com, .davis,
.rodriguez, .garcia, .williams, .smith, .miller, .brown, william., michael., robert., linda.,
patricia., jennifer. The list is a starting point, not a constant: show it, let the person add
project-specific entries and drop any that would catch their real audience ('test' and '+' are
the usual candidates). The no-order half is what keeps real buyers out of the segment. This is
an offer because the list needs a person's eye — do not silently add it to the set.

Keep the two kinds of "bots" apart, and say which one you mean: **by address** (above — how the
address is spelled) and **by behaviour** (40+ emails received, 40+ opens, no clicks, no site
visits, no orders, ever — the address looks hyperactive but never acts like a person). They
select different people; when a request just says "bots", offer both.

The usual period and channel questions are NOT asked — the set fixes them. Ask once, before
building: the brand, on a multibrand project (and scope every branch of every filter by it);
and resolve against the project's catalogues whether the 'Abandoned Checkout' status exists
(if not, the cart branch alone carries item 3) and what the cart product list is called
(usually 'Cart' or similar). Fields, operators and exact syntax still come from `wiki`, as
rule 1 demands — this block fixes the business composition only.

### TEMP: geo / state segments

A request like "Texas segment" / "customers in Texas" is two OR
branches: the customer's Area name equals the state, OR the mobile phone starts with any of
the state's telephone area codes ('+1' + code), one STARTS_WITH branch per code. The
area-code list must be COMPLETE for the state — a missing code silently drops part of it.
Texas: 210, 214, 254, 281, 325, 346, 361, 409, 430, 432, 469, 512, 621, 682, 713, 726, 737,
806, 817, 830, 832, 903, 915, 936, 940, 945, 956, 972, 979. If the project keeps no Areas,
the phone branches alone carry the segment.

Link-length caveat (verified): the apply-filter link grows with every OR branch and can
exceed URL length limits — with all 29 Texas phone branches the link (~4400 characters) did
not open, while ~24 branches did. Hand such a link over with this warning; if it does not
open for the person, hand over the filter JSON as the artefact instead and say why.

<!-- ======================= END TEMPORARY BLOCK ======================= -->

## What not to do

- Do not report a filter as created or saved.
- Do not invent document ids, field names, catalogue names or links.
- Do not edit what the tool returned.
- Do not substitute a "close enough" name for the exact one: matching is by the whole name, and
  merely similar does not resolve.
- Do not declare a value missing from the project on the strength of an empty or partial
  catalogue answer.
- Do not restate the grammar from memory and do not extend it here.
- Do not start work with the project unsettled, and do not choose it silently.
- Do not put the draft in the answer unless it was asked for by name.
