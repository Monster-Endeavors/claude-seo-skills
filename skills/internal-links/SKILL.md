---
name: internal-links
description: "Suggests internal links for pages that are close to page one of Google, using Search Console to pick target pages, anchor text and source pages, then names the exact sentence to link from. Uses the MetaMonster connector's Search Console and quick page check tools. Use when someone asks for internal link suggestions, an internal linking plan, or how to help a page rank higher."
---

# Internal links

You suggest internal links that help specific pages rank. Every suggestion names the source page, the sentence to link from, the anchor text and the target, and points back to the Search Console data behind it.

## Before you start

- This skill needs the MetaMonster connector. If its tools aren't available, tell the user to add MetaMonster from Claude's connector directory, or offer to work from a list of URLs and Search Console data they paste in.
- Call `list_search_console_properties`. If there's more than one property, ask which site. If none is connected, give the user the link the tool returns.
- Without a MetaMonster plan, Search Console queries are capped at 100 a day. This skill uses about 3 queries per target page (its searches, its sources and its baseline) plus 1 to find targets, so work on 3 targets at a time unless the user asks for more.

## 1. Pick the target pages

If the user named the pages to help, use those.

Otherwise call `query_search_console` with the property, `dimensions: ["page"]`, `days: 28`, `sort: "impressions"` and `limit: 100`. Keep pages with an average position between 8 and 20 and a meaningful number of impressions for this site. They're close enough to page one that links can move them. Show the user the top 3 and ask which to work on.

## 2. Learn what each target ranks for

For each target, call `query_search_console` with `dimensions: ["query"]`, a page filter (`operator: "equals"` and the exact URL), `days: 90`, `sort: "impressions"` and `limit: 25`. Its top queries are the anchor text ideas. Call `quick_check_page` with the target's `url` to see its current links.

## 3. Find source pages

Take the 2 or 3 most distinctive words from the target's top queries. Call `query_search_console` with `dimensions: ["page"]`, a query filter (`operator: "includingRegex"` with those words joined by `|`), `days: 90` and `limit: 50`. Leave out the target itself. These are other pages on the site that already rank for related searches, which makes them relevant sources.

If the user has a MetaMonster plan and the site is in MetaMonster, you can also use `find_pages` with a `search` term to find more pages. If not, and you need more candidates, fetch the site's sitemap.

## 4. Read the sources

Fetch and read up to 10 source pages. Look for sentences in the main content that already mention the target's topic. Skip navigation, footers and sidebars, and skip pages that already link to the target.

## 5. Suggest the links

For each target, suggest 1 to 3 links from different source pages. Rules:

- Prefer sources that rank well and get clicks, and pages the site links to often, such as its main guides. They pass more weight.
- If the site has a main guide for the target's topic (a pillar page) that doesn't link to the target yet, make it one of the sources. If the target doesn't link back to that guide, suggest that link too.
- Use a natural phrase from the sentence as the anchor, close to one of the target's top queries. Vary the anchors across links and never force an exact-match phrase into a sentence.
- If no sentence fits, you can suggest one short new sentence. Mark it clearly as new copy.
- One link to the same target per source page is enough.
- Check each anchor against the links on the source pages you read. If the same anchor text already points to a different page, pick another anchor and tell the user, because the same words linking to two pages muddle which one is about that topic.

## 6. Show the results

Show a table with the source page, the sentence (with the anchor in bold), the target, and one line on why, citing the target's position and the queries the anchor matches. Nothing on the site changes.

Before the links go live, call `query_search_console` for each target with `dimensions: ["date"]`, the page filter and `days: 90`, and average the position by week. That's the target's normal range. Tell the user to count it as a move only if the weekly position leaves that range and stays out for 2 to 3 weeks, and not to credit the links for it, since rankings move for other reasons too.
