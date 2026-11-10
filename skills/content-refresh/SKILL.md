---
name: content-refresh
description: Finds the pages on a site that are losing Google clicks, works out why from Search Console, and writes a refresh plan for each one. Uses the MetaMonster connector's Search Console and quick page check tools. Use when someone asks which content to update, why traffic dropped, how to refresh old posts, or what to fix first.
---

# Content refresh

You find the pages losing the most search traffic and tell the user what changed and what to edit. Every recommendation should point back to a Search Console number or a check that failed.

## Before you start

- This skill needs the MetaMonster connector. If its tools aren't available, tell the user to add MetaMonster from Claude's connector directory, or offer to work from Search Console data they paste in.
- Call `list_search_console_properties`. If there's more than one property, ask which site. If none is connected, give the user the link the tool returns.
- Without a MetaMonster plan, Search Console queries are capped at 100 a day. This skill uses two queries to find pages and about two more per page (its lost searches and its baseline), so work on 3 pages at a time unless the user asks for more.
- Pages that already rank in the top 3 for a search have the most to lose, since a change can cost them rankings and clicks. The first time one comes up, ask the user how to handle them: leave them alone, ask before each change (the default if they don't say), or treat them like any other page. Follow their answer for the rest of the session. If the site is in MetaMonster on a plan, check `get_site_guidance` for a saved answer first, and offer to save a new one as a preference with `update_site_guidance`.

## 1. Find the pages losing clicks

If the user named a page, skip to step 2.

Call `query_search_console` with the property, `dimensions: ["page"]`, `days: 28`, `compare_to: "previous_period"`, `sort: "clicks_change"`, `direction: "asc"` and `limit: 25`. These are the pages that lost the most clicks against the 28 days before.

Run the same call with `compare_to: "previous_year"`. If a page lost about the same at this time last year, the drop is probably seasonal: tell the user and leave it out.

Show the user the biggest drops that aren't seasonal and ask which to work on. Default to the top 3.

## 2. Work out what kind of drop it is

For each page, call `query_search_console` with `dimensions: ["query"]`, a page filter (`operator: "equals"` and the exact URL), `days: 28`, `compare_to: "previous_period"`, `sort: "clicks_change"`, `direction: "asc"` and `limit: 25`.

Sort each lost query into one of these:

- Fewer impressions at the same position: fewer people are searching. That isn't a content problem, so don't rewrite for it.
- A worse position: other pages overtook this one. This is the case a refresh fixes best.
- The same position and impressions with a lower CTR: something on the results page changed, such as an AI Overview, more ads or a competitor's better title. Look at the title and meta description first.
- Gone entirely: the page may no longer look relevant, or another page on the same site took over. Run a query-filtered search with the page dimension to see whether another URL on the site now ranks for it.

## 3. Read the page

Fetch the page and read it. Then call `quick_check_page` with its `url`, using the query with the most impressions as `primary_keyword`, and note every check that fails.

Compare the page with the queries it lost. Which questions doesn't it answer? Which facts, prices, screenshots or dates look out of date? Does the opening answer the main search quickly?

## 4. Write the refresh plan

For each page, write:

- What happened, in a sentence or two with the numbers: clicks, impressions and position, this period against the last.
- The edits, most important first: sections to add for the lost queries, facts to update, sections to merge or cut, quick check failures to fix, and a new title and meta description if CTR fell.
- What to leave alone: the URL, and sections that still pull clicks for queries that held or grew. If the page is still in the top 3 for its main search, handle it the way the user chose (see Before you start).

Rules:

- Never invent statistics, quotes or examples. Mark the spots where the user needs to supply updated numbers or new examples.
- Only suggest changing the published date if the content changes in a meaningful way.
- Don't suggest adding words just to raise the word count.
- Cover the basics first: the lost queries, and what the top results for the main search all cover. The serp-topic-gaps skill makes that comparison if it's installed.
- Then add something the other results don't have, such as the user's own data, examples, screenshots or steps. New material helps most on a page that already covers the basics, so don't trade the basics for a unique angle.

## 5. Go deeper on a MetaMonster plan

If the user has a plan, offer to run `analyze_page` for the full analysis, which checks 40+ factors including information gain, E-E-A-T and answer-engine readiness. If the analysis has no fixes yet, run `write_fixes`. Once the user picks fixes, `generate_content_draft` rewrites the body and saves it as a draft in MetaMonster. Nothing is published.

Without a plan, hand over the refresh plan as a checklist the user can work through.

## 6. Show the results

Start with a summary table: page, clicks then and now, type of drop, and the top 3 edits. Then give each page's full plan.

Before the edits go live, call `query_search_console` with `dimensions: ["date"]`, the page filter and `days: 90`, and add the days up into weekly clicks. That's the page's normal range. Tell the user to count it as a recovery only if weekly clicks move outside that range and stay there for 2 to 3 weeks, and not to credit the refresh for it, since rankings move for other reasons too.
