---
name: metadata-rewrite
description: Finds pages that get Google impressions but few clicks and rewrites their title tags, meta descriptions, H1s and Open Graph tags from the searches behind them. Uses the MetaMonster connector's Search Console and quick page check tools. Use when someone wants more clicks from Google, new titles or meta descriptions, a better CTR, or asks why a page gets impressions but no clicks.
---

# Metadata rewrite

You rewrite title tags and meta descriptions for pages that Google already shows but people don't click. Base every rewrite on the searches in the site's Search Console data, not on guesses.

## Before you start

- This skill needs the MetaMonster connector. If its tools aren't available, tell the user to add MetaMonster from Claude's connector directory, or offer to work from data they paste in: the URL, the current title and description, and the top queries with clicks, impressions and position.
- Call `list_search_console_properties`. If there's more than one property, ask which site. If none is connected, give the user the link the tool returns.
- Without a MetaMonster plan, Search Console queries are capped at 100 a day. This skill uses one query to find pages and about two more per page (its searches and its baseline), so work on 5 pages at a time unless the user asks for more.

## 1. Find the pages

If the user named a page, skip to step 2.

Call `query_search_console` with the property, `dimensions: ["page"]`, `days: 28`, `sort: "impressions"` and `limit: 50`. Keep pages with an average position between 4 and 10 whose CTR is well below the median CTR of the site's other pages in the same position range. Those pages rank but don't get picked. Leave out pages in the top 3 unless the user asks for them, because they already get most of the clicks on offer and a new title can lose some. If the user does want one, tell them the risk is higher and keep the change small. Show the user the top 5 with clicks, impressions, CTR and position, and ask which to work on. Default to all 5.

## 2. Read the searches behind each page

For each page, call `query_search_console` with `dimensions: ["query"]`, a page filter (`operator: "equals"` and the exact URL), `days: 28`, `sort: "impressions"` and `limit: 25`.

Note three things:

- the query with the most impressions, which becomes the working primary keyword
- what the top queries have in common: are people looking for a definition, a tool, a comparison, a price or a how-to?
- queries where the page ranks well but gets no clicks, because those are the ones the current title is losing

If the top queries don't match what the page is about, say so. A new title won't fix a page that ranks for the wrong thing.

## 3. Check the current page

Call `quick_check_page` with the page's `url` and the working primary keyword as `primary_keyword`. Record the current title, meta description and H1, and every check that fails. If the fetch comes back thin because the page builds its content with JavaScript, ask the user for the page's HTML or its current title and description.

## 4. Write the new copy

For each page, write:

- 2 title options
- 2 meta description options
- an H1, only if the quick check flagged it or it doesn't match the top searches
- an Open Graph title and description, if the user wants social copy or the page has none

Rules:

- Match what the top searches want. If people want a tool, say it's a tool. If they want a price or a number, put it in.
- Put the primary keyword near the start of the title when it reads naturally, and don't stuff in secondary keywords.
- Only promise what the page delivers. Read the page before you mention a feature, number, price or date, and never make one up.
- If the site ends its titles with the brand name, keep doing that.
- Write like a person, not an ad. Skip words like "ultimate", "comprehensive" and "unlock".

## 5. Check the new copy

Call `quick_check_page` again with the `url`, the `primary_keyword`, and your proposed `title` and `meta_description`, which override what's on the page. Fix anything that fails and check again. Only show the user versions that pass the length and keyword checks.

## 6. Show the results

For each page, show a table with the current and proposed title, meta description and H1 (if it changed), plus one line on why, citing the searches and numbers behind the change. Put the option you'd pick first.

Nothing is published. If the user has a MetaMonster plan and wants to keep going, offer to save the copy they pick as drafts on the page in MetaMonster with `set_field_draft`, where they can review it and publish it. Without a plan, they copy the new tags into their CMS themselves.

## 7. Set up a fair before and after

CTR moves from week to week on its own, so one period against the next won't show whether the new copy worked. Before the copy goes live, call `query_search_console` for each page with `dimensions: ["date"]`, the page filter and `days: 90`, and add the days up into weekly clicks and CTR. That's the page's normal range. Tell the user to count it as a real result only if CTR moves outside that range and stays there for 2 to 3 weeks, and even then not to credit the new title for it, since rankings and the results page change too.
