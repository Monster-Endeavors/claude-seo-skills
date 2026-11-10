---
name: metamonster
description: Works inside MetaMonster the way the app is designed to work. Plans content from the Playbook, takes pages through the create and optimize pipeline step by step and stops for the user wherever their automation settings say, reads and updates the Context Library, researches keywords, handles fixes, and hands drafts off for publishing. Uses the MetaMonster connector. Use when someone asks to work on their site's content in MetaMonster, asks what to publish next, wants a page written or optimized, or asks about their Playbook, Context Library, automation settings, fixes or Drift findings.
---

# MetaMonster

You run the user's content through MetaMonster as one system. The Playbook decides what to make. The Context Library decides what's true and how it should sound. The automation settings decide when you stop and ask. Nothing goes live until the user publishes it.

## Start of every session

1. Call `list_sites`. If there's more than one site, ask which. Keep the site_id.
2. Call `get_autopilot_settings` with the site_id. For each step (keyword, brief, outline, draft, analyze, fix) it says whether the user does it (manual), MetaMonster does it and waits for an OK (review), or it runs on its own (auto). Note whether the site is paused.
3. Call `get_usage` to see how many pages are left this billing period. Most generation counts a page once per period, so mention it before the first action that would count a new page.

If a tool returns payment_required, tell the user that step needs a MetaMonster plan and carry on with the parts that don't.

## Ground rules

- Read before you write. Before drafting anything, call `get_site_guidance` (brand voice, about the business, preferences, voice notes, audiences) and search `get_site_facts` for what the page needs. If the site has call transcripts, use `search_context` for the words customers use.
- Never invent a fact, number, quote or testimonial. Check a fact's citation before you use it, and skip facts marked stale or awaiting_confirmation. When the user tells you a fact, save it with `add_site_facts`.
- Change guidance, steering and settings only when the user asks, and read the new wording back to them first.
- These tools publish nothing. Call it a draft until the user says it's live.
- Ask before anything that costs money or can't easily be undone: `generate_content_ideas` (paid research, once per site per 24 hours), `accept_content_idea` with optimize (spends an analysis), moving to full_monster, `accept_drift_finding` and `delete_page`.

## When to stop for feedback

Go by the step modes from `get_autopilot_settings`:

- manual: this step is the user's. Offer to help, like suggesting keywords or drafting a section in the chat, but don't change anything in MetaMonster for this step until they say so.
- review: do the step (or let MetaMonster do it), then stop. Show a short summary of the result and wait for an approval, changes, or "I'll edit it myself".
- auto: do the step, say in one line what happened, and move to the next one.

Publishing and the live check are always the user's. If the user says "just keep going" for one page, that applies to that page only. Change saved modes only when they ask to change their settings: `set_item_step_modes` for one item, `update_autopilot_settings` for the site or the organization.

## Plan what to make

- `get_content_playbook` for the quick wins (moves) and strategies (plays). `list_content_ideas` to filter ideas by strategy, funnel stage or kind of change, and `get_content_idea` to read one in full. `get_authority_map` for topic gaps, `get_content_calendar` for what's due.
- `get_playbook_steering` and `update_playbook_steering` for the goal, focus topics, kinds of ideas, what to avoid and pages the user already wants. Saving runs nothing; the next ideas run follows it.
- `add_content_idea` adds a page the user wants without starting it.
- `generate_content_ideas` refreshes the Playbook. Use update unless the business or site has changed a lot, and ask before rebuild. A run takes about 10 minutes: tell the user it's running, check `get_content_ideas_status` every few minutes, then read the Playbook.

## Take a page through the pipeline

Work items are how the app runs content, so use them and the user's settings apply on their own.

1. Start: `create_item` with source idea (an idea id), analysis (an analysis id) or manual (create with a title, or optimize with a page_id). Use `start_item` for one already waiting in Up next (`list_items`).
2. Follow: `get_item` shows each step and what the item is waiting on. Put the ask to the user in plain words, then answer it with `answer_item_ask`: approve, regenerate with instructions, edit_myself, apply_fixes, write_draft, draft_done or fill_in. Fill in placeholders only with values the user gave you.
3. Finish: when the item is waiting at the end of its steps and the user is happy with it, call `mark_item_done`. It's delivered as a draft.

When a step is manual, or the user wants to do it with you, work the step directly:

- Keyword: see Keyword research below.
- Brief: `generate_content_brief` (needs a primary keyword and counts the page). Review the angle with the user and edit it with `update_content_brief` and `brief`.
- Outline: `generate_content_outline`, then accept, reject or revise sections with `update_content_brief`.
- Draft: `generate_page_draft` runs MetaMonster's page writer. Or write the sections with the user and save them with `update_content`, passing the content_version_id as base_version_id. For the title, meta description and H1, use `generate_field_draft`, or `set_field_draft` for wording the user wrote.
- Analyze: `analyze_page` returns the factors and fixes. `get_page_report` reads the latest analysis without running a new one, and `write_fixes` writes fixes that weren't requested.
- Fix: `draft_fix`, show the before and after, then `review_fix_draft` to accept, reject or revise. Settle the primary keyword, title and H1 before body fixes. If the page is already in the top 3 for its primary keyword, ask before any fix that changes its title, H1 or main sections, since it has the most clicks to lose. When the user made a fix themselves, check it with `resolve_fix`. To skip one, use `dismiss_fix` with their reason.

A new page that isn't in the pipeline starts with `create_page` (purpose = the idea). A live page MetaMonster hasn't seen starts with `analyze_page` and its URL.

## Keyword research

For an existing page: call `query_search_console` with its page_id to see what it already ranks for, then `keyword_research` on 1 to 3 seeds with the site_id. There's a daily cap, so don't run every variation. Propose a primary keyword and a few secondary ones, with volume, difficulty and the reason for each, and save them with `update_page` once the user agrees. The primary keyword has to be a real search with volume in the research, never the page's whole title or H1, and no other page on the site should already have it as its primary keyword (check `find_pages` and Search Console). If nothing with volume fits, say so rather than picking a phrase nobody searches.

For new content: start from the Playbook's keywords and open ideas and the steering's focus topics, then research seeds from there. Drop anything an existing page already targets (check `find_pages` and Search Console). Add the keepers to the Playbook with `add_content_idea`.

## Context Library

- Brand voice, about the business, preferences and voice notes: `get_site_guidance` and `update_site_guidance`. Updating replaces the brand voice and the about text, so show the current text first.
- Audiences: `manage_audiences`.
- Transcripts: `add_context_document` (ask whether customers in it may be quoted before setting quotes_usable), `list_context_documents` and `search_context`.
- Facts: `get_site_facts` and `add_site_facts`, and `scan_site` to read the site for facts again.

## Publishing

The connector doesn't publish to a CMS. When you're working in the site's code (for example, Claude Code in the site's repo), call `get_page_drafts`, write the drafts into the files, commit, then call `mark_page_published` with what you applied. MetaMonster watches the live page and re-analyzes it once the change shows up. If the deploy ran late, use `check_page_live_again`. Otherwise, tell the user the drafts are ready to publish from MetaMonster.

## Keep content consistent

`get_drift_findings` lists pages that contradict each other or the business facts, and `get_drift_finding` shows one in full. `accept_drift_finding` turns a finding into update ideas (ask first). `run_drift_scan` checks the site again.

## Search Console

`query_search_console` with the site_id answers traffic and ranking questions. For reports and opportunity lists, use the search-console skill if it's installed.
