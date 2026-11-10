---
name: serp-topic-gaps
description: Reads the top Google results for a keyword, works out what they all cover and where they differ, and compares them with the user's page to list missing topics, untapped angles and unanswered searches from Search Console. Uses web search plus the MetaMonster connector's Search Console and quick page check tools, and content briefs on a MetaMonster plan. Use when someone asks for a SERP analysis, a topic gap analysis, competitor content research, or what a page is missing.
---

# SERP and topic gaps

You compare a page with what currently ranks for its keyword and tell the user what to add. Only describe competitor pages you actually opened and read.

## Before you start

- You need web search to read the results. If it isn't available, ask the user to paste the URLs of the top results.
- This skill uses the MetaMonster connector for the Search Console and page check steps. If its tools aren't available, tell the user to add MetaMonster from Claude's connector directory, and do the SERP part on its own.
- Call `list_search_console_properties` and ask which site if there's more than one. Without a MetaMonster plan, Search Console queries are capped at 100 a day. This skill uses 1 or 2.

## 1. Get the keyword and the page

Ask for the keyword and the page (or say it's a new page). If the user only gave a page, call `query_search_console` with `dimensions: ["query"]`, a page filter (`operator: "equals"` and the exact URL), `days: 90`, `sort: "impressions"` and `limit: 25`, and use the query with the most impressions. Keep the rest of the list for step 4.

## 2. Read the results

Search the keyword and open the top 5 to 8 organic results. Skip ads. If forums or videos fill the top spots, note that, because it says something about what searchers want.

For each result, note the type of page, its angle, its main sections, anything only it offers (data, a tool, a template, real examples), and when it was last updated.

## 3. Sum up the results

- Table stakes: what nearly every result covers.
- Differences: what only some cover.
- Open angles: facts, data or examples searchers likely need that nobody covers well.
- Format: the kind of page that wins, such as a guide, list, tool or comparison, and its rough length.

## 4. Compare with the user's page

Fetch and read the page. Call `quick_check_page` with its `url` and the keyword as `primary_keyword`, and note what fails. Then go through the Search Console queries from step 1 and find the ones the page doesn't answer.

## 5. Show the results

Give four short lists: table stakes the page is missing, open angles worth taking, Search Console questions to answer, and any mismatch in format. Put the most important item first in each, and put the missing table stakes ahead of the open angles. New angles help a page that already covers the basics, but a page that's mostly new angles and skips the basics can do worse. Don't promise that new material will move a page up once it's already on page one. Don't copy any competitor's wording.

## 6. Build a brief on a MetaMonster plan

If the user has a plan and the page is in MetaMonster, offer `generate_content_brief`. It reads the top results for the page's primary keyword and writes an angle and a section outline the user can edit. It counts the page once against the plan's monthly allowance, so ask first.
