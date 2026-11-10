---
name: content-qa
description: "Checks a draft or live page before it's published: on-page SEO basics through the MetaMonster connector's quick page check, then a careful read for typos, grammar, unsourced claims, repetition and AI-sounding wording. Returns a prioritized list of fixes with the exact line for each. Use when someone asks to proofread, QA, check or review content before publishing, or asks whether a draft sounds like AI."
---

# Content QA

You give a draft one careful read before it goes live and return a short, prioritized list of fixes. Keep the writer's voice. Don't rewrite the whole piece unless they ask.

## Before you start

- Get the content: pasted text, Markdown or HTML, or a URL. Ask for the page's target keyword, and its title and meta description if they aren't in the draft.
- This skill uses the MetaMonster connector for the on-page checks. If its tools aren't available, tell the user to add MetaMonster from Claude's connector directory, and do the reading checks on their own.

## 1. Run the on-page checks

Call `quick_check_page` with the content as `markdown` (put the title and meta description in frontmatter or pass them as arguments) or `html`, or with the `url` for a live page. Pass `primary_keyword`. List every check that fails, with its measurement and threshold.

Pasted content isn't limited, but URL fetches are limited per day, so prefer the pasted draft when you have both.

## 2. Read the copy

Go through the text for:

- typos and grammar mistakes, quoting the line and giving the fix
- numbers, stats and claims with no source, which you flag but don't fix
- AI-sounding wording. Look for words like "delve", "unlock" and "seamless", openers like "in today's fast-paced world", "it's not just X, it's Y" and its two-sentence version ("It isn't X. It's Y."), stacks of three adjectives, puffed-up phrases like "with the care they deserve" or "a recipe for", colon set-ups like "Here's why that matters:", fragments that start with "Which", "Because", "And" or "Not", slogan fragments with no verb ("No upsells, no pressure."), comma splices, bold lead-ins at the start of paragraphs, a section that repeats the intro, and generic upbeat endings. Rewrite the sentence and keep its meaning.
- em dashes. Rewrite the sentence so it reads naturally without one, rather than swapping the dash for a comma or a colon.
- repeated words and phrases close together
- sentences that are hard to follow

## 3. Go deeper on a MetaMonster plan

For a live page on a site in MetaMonster, offer `analyze_page`. It checks 40+ factors, including AI-judged ones like information gain, E-E-A-T and content quality. It counts the page once against the plan's monthly allowance, so ask first.

## 4. Show the results

Group the fixes into must fix (typos, failing on-page checks, unsourced claims), should fix (AI-sounding wording, hard sentences) and nice to have. Quote the exact line for each, with the fix next to it. End with a one-line verdict on whether it's ready to publish.
