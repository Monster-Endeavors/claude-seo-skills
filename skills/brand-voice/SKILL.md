---
name: brand-voice
description: Reads pages the user says sound like their brand and writes a voice and tone guide with plain rules, each backed by a quote from their pages, plus words to use and avoid and before-and-after examples. On a MetaMonster plan, it can save the guide to the site's Context Library through the MetaMonster connector. Use when someone asks for a brand voice guide, a tone of voice guide, a style guide, or rules for an AI writer.
---

# Brand voice

You write a voice guide from what the user's own pages do, not from adjectives. Every rule must point to a line from their pages.

## 1. Get the pages

Ask for 3 to 5 URLs that sound the way the user wants, and optionally 1 or 2 that don't. Ask who the audience is.

## 2. Read them

Fetch and read each page. Note sentence length, how formal it is, whether it uses "you" and "we", how much jargon there is, humor, formatting habits such as headings, lists and sentence case, and words that come up again and again. Copy out short lines that show each habit.

## 3. Add what MetaMonster knows, on a plan

If the user has a MetaMonster plan and the site is in MetaMonster, call `get_site_guidance` to read the current brand voice. If they've added call transcripts, call `search_context` (for example, with "how customers describe the problem") to find the words customers use. Never present customer words as the brand's own claims.

## 4. Write the guide

- A short paragraph that sums up the voice.
- 5 to 8 rules. For each one, give a line from their pages that shows it, and a short do and don't.
- Words and phrases to use, and ones to avoid.
- Formatting habits.
- 2 before-and-after rewrites of a generic sentence in their voice.

Don't invent quotes, customers or claims.

## 5. Save it, if they ask

On a MetaMonster plan, offer to save the guide as the site's brand voice with `update_site_guidance` (`voice_tone`). This replaces the current brand voice, so show the user the current one first and save only when they say so.
