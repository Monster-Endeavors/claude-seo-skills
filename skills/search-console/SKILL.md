---
name: search-console
description: Answers questions about a site's Google Search Console data and turns it into reports and opportunity lists, including performance reports with period comparisons, striking-distance keywords, cannibalization, new and rising searches, question searches, brand versus non-brand traffic, and device or country splits. Uses the MetaMonster connector's Search Console tools, which work without a MetaMonster plan (up to 100 queries a day). Use when someone asks about their search traffic, rankings, clicks, impressions, Google Search Console, an SEO report, or where their SEO opportunities are.
---

# Search Console

You answer Search Console questions with real data, and you say which dates every number covers.

## Before you start

- This skill needs the MetaMonster connector. If its tools aren't available, tell the user to add MetaMonster from Claude's connector directory, or work from a Search Console export they paste in.
- Call `list_search_console_properties`. If there's more than one property, ask which site, and prefer the domain property (sc-domain:) when both exist. If none is connected, give the user the link the tool returns.
- Pass `property` to `query_search_console`. Without a MetaMonster plan that's capped at 100 queries a day. On a plan, with the site in MetaMonster, you can pass `site_id` instead, and page rows come with a page_id for MetaMonster's page tools.
- Plan the queries before you run them. Most recipes below take 1 to 5. If a request would need more than about 20, say so and suggest a smaller version.
- Pages that already rank in the top 3 for a search have the most to lose, since a change can cost them rankings and clicks. The first time one comes up, ask the user how to handle them: leave them alone, ask before each change (the default if they don't say), or treat them like any other page. Follow their answer for the rest of the session. If the site is in MetaMonster on a plan, check `get_site_guidance` for a saved answer first, and offer to save a new one as a preference with `update_site_guidance`.

## Rules for the numbers

- Data ends 2 days ago. Default to 28 days, and use 90 days when volumes are small.
- Use the same date range for every number in one answer, and state the dates.
- Rows leave out searches Google anonymizes, so query rows add up to less than the totals. Take headline numbers from a query with no dimensions.
- Position is an average, and lower is better. A negative position_change is an improvement.
- When seasonality could explain a change, compare with `previous_year` as well as `previous_period`.
- Say what the data shows. Don't present a guess about the cause as fact; name what you'd check next.
- One period against another doesn't prove that a change worked. To judge one, take the weekly numbers for 8 to 12 weeks before it as the normal range (`dimensions: ["date"]`, added up by week), and count it only if the numbers leave that range and stay out for 2 to 3 weeks. Even then, say what moved, not that the change caused it.

## Answer a question

Turn the question into a query: dimensions, filters, date range and sort. For "how are we doing" questions, start with totals and no dimensions. Show a short table, then two or three sentences on what it means.

## Performance report

1. Totals with `compare_to: "previous_period"` (and `"previous_year"` if asked).
2. Top 10 pages: `dimensions: ["page"]` with the same comparison.
3. Top 10 queries: `dimensions: ["query"]` with the same comparison.
4. Biggest movers: `dimensions: ["page"]`, compared with the previous period, sorted by `clicks_change` ascending for the losers and descending for the winners.
5. If asked: a device or country split.

Lay it out as headline numbers with their change, then the tables, then the 3 things most worth acting on. About 5 or 6 queries.

## Find opportunities

Pick the recipe that fits the ask. For "where are my opportunities", run striking distance, cannibalization, rising searches and question searches together, which is about 5 queries. Handle searches where a page already ranks in the top 3 the way the user chose (see Before you start).

Striking distance: `dimensions: ["query", "page"]`, `days: 90`, `sort: "impressions"`, `limit: 200`. Keep rows with an average position from 8 to 20 and rank them by impressions. For the top 5, name the page and the search and what would move it: a section that answers the search, the search in the title or H1, or internal links from related pages (the internal-links skill does this).

Low click-through on page one: use the metadata-rewrite skill if it's installed. Otherwise, take pages at position 10 or better whose CTR is below the median for their position range.

Pages losing traffic: use the content-refresh skill if it's installed. Otherwise, `dimensions: ["page"]` with `compare_to: "previous_period"`, sorted by `clicks_change` ascending.

Cannibalization: `dimensions: ["query", "page"]`, `days: 90`, `sort: "impressions"`, `limit: 200`. Group the rows by search. Flag searches where two or more pages each get at least 20% of the impressions. For each, say which page should own the search (usually the one with more clicks and the closer match) and what to do with the other: merge it, refocus it on a different search, or link it to the owner. Check the other page's own searches before suggesting a redirect.

New and rising searches: `dimensions: ["query"]`, `compare_to: "previous_period"`, `sort: "impressions_change"`, `limit: 100`. Searches with no impressions in the previous period are new. They show topics Google has started testing the site for.

Question searches: `dimensions: ["query", "page"]`, `days: 90`, and a query filter with `operator: "includingRegex"` and `^(how|what|why|when|where|which|who|can|does|do|is|are|should)\b`. Group them by page. Questions with impressions and a weak position are content to add, as a section, an FAQ or a new page.

Brand versus non-brand: ask for the brand terms. Run two totals queries with the same comparison, one with `includingRegex` and the brand terms joined by `|`, and one with `excludingRegex`.

Device or country: `dimensions: ["device"]` or `["country"]` with a comparison.

## Finish

End with the 3 to 5 most worthwhile actions, most important first, each tied to the rows behind it. On a MetaMonster plan, offer the next step there: `analyze_page` for a page an opportunity points to, or `add_content_idea` for a new page. Change nothing unless the user asks.
