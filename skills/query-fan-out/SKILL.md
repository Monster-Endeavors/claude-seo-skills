---
name: query-fan-out
description: Writes out the related searches behind a topic (a query fan-out), checks which ones the site already shows up for in Search Console, and turns the gaps into questions to answer or a section plan. Uses the MetaMonster connector's Search Console tool, plus keyword research on a MetaMonster plan. Use when someone asks for a query fan-out, related questions, AI search coverage, what a page is missing, or how to plan a new piece of content.
---

# Query fan-out

You map the related searches someone is likely to need around a topic, then measure which ones the site already covers. Be clear about which part is prediction and which is data: the fan-out is your prediction, and coverage comes from Search Console.

## Before you start

- This skill needs the MetaMonster connector. If its tools aren't available, tell the user to add MetaMonster from Claude's connector directory. You can still write the fan-out without it, but say that coverage can't be checked.
- Call `list_search_console_properties`. If there's more than one property, ask which site. If none is connected, give the user the link the tool returns.
- Without a MetaMonster plan, Search Console queries are capped at 100 a day. This skill uses 2 or 3.

## 1. Get the topic

If the user gave a topic, use it. If they gave a page, call `query_search_console` with `dimensions: ["query"]`, a page filter (`operator: "equals"` and the exact URL), `days: 90`, `sort: "impressions"` and `limit: 25`, and use the page's main search as the topic. Ask whether this is for a new piece of content or an existing page.

## 2. Write the fan-out

Write 15 to 30 searches, phrased the way people type or ask them, in these groups:

- definitions and basics
- how-to and steps
- comparisons and alternatives
- costs and pricing
- problems and mistakes
- examples and templates
- what to do next

Skip a group if it doesn't fit the topic.

## 3. Check coverage

Pick the 3 to 5 most distinctive words across the fan-out. Call `query_search_console` with `dimensions: ["query", "page"]`, a query filter (`operator: "includingRegex"` with those words joined by `|`), `days: 90`, `sort: "impressions"` and `limit: 200`.

Match each fan-out search to the closest real query in the results. Mark it covered (with the page and position), weak (the site shows up, but below position 20), or a gap (nothing close).

## 4. Add demand on a MetaMonster plan

If the user has a plan, call `keyword_research` once with the topic as the seed and `limit: 50`. Add volume and difficulty to the fan-out searches that match a related keyword. Keyword research has a daily cap, so don't run it for every search.

## 5. Show the results

Show a table with each search, its group, its coverage (page and position, or gap) and, on a plan, volume and difficulty.

Then, for new content, give a section plan with one heading per group that has gaps, and the searches each section should answer. For an existing page, list the 5 gaps it should answer first and where on the page each one fits. If another page on the site already covers a search, suggest linking to it rather than repeating it.
