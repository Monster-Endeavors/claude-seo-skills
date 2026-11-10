# Claude SEO skills

Nine skills that teach Claude to do real SEO work on your site: rewrite titles people scroll past, find pages losing traffic, suggest internal links, check drafts before they go live, and answer questions about your Google Search Console data. They run on the [MetaMonster](https://metamonster.ai) connector, so Claude works from your own search data instead of guessing.

You can start for free with the MetaMonster MCP. Search Console questions and the quick page check work without a MetaMonster plan (up to 100 Search Console queries a day), and the table below shows which parts of each skill need one.

<!-- TODO: link the skills hub at metamonster.ai/skills/ once it's live. -->

## The skills

| Skill | What it does | Without a MetaMonster plan? | Download |
| --- | --- | --- | --- |
| [MetaMonster](skills/metamonster/SKILL.md) | Runs your content through MetaMonster from chat: plans from your Playbook, takes each page through keyword, brief, draft, analysis and fixes, and stops wherever your automation settings say | Mostly needs a plan, since it works on a site in MetaMonster | [metamonster.zip](https://github.com/Monster-Endeavors/claude-seo-skills/raw/main/dist/metamonster.zip) |
| [Search Console](skills/search-console/SKILL.md) | Answers Search Console questions in plain words, builds performance reports, and finds striking-distance keywords, cannibalization and rising searches | Yes, up to 100 queries a day | [search-console.zip](https://github.com/Monster-Endeavors/claude-seo-skills/raw/main/dist/search-console.zip) |
| [Metadata rewrite](skills/metadata-rewrite/SKILL.md) | Finds pages with lots of impressions and few clicks, then rewrites their titles, meta descriptions and H1s from the searches behind them | Yes. Saving drafts in MetaMonster needs a plan | [metadata-rewrite.zip](https://github.com/Monster-Endeavors/claude-seo-skills/raw/main/dist/metadata-rewrite.zip) |
| [Content refresh](skills/content-refresh/SKILL.md) | Finds the pages losing clicks, works out why, and writes a refresh plan for each | Yes. The full page analysis needs a plan | [content-refresh.zip](https://github.com/Monster-Endeavors/claude-seo-skills/raw/main/dist/content-refresh.zip) |
| [Internal links](skills/internal-links/SKILL.md) | Suggests internal links for pages close to page one, down to the sentence and anchor text | Yes. Finding more link sources in MetaMonster needs a plan | [internal-links.zip](https://github.com/Monster-Endeavors/claude-seo-skills/raw/main/dist/internal-links.zip) |
| [Query fan-out](skills/query-fan-out/SKILL.md) | Maps the related searches behind a topic and checks which ones your site already covers | Partly. Keyword volumes need a plan | [query-fan-out.zip](https://github.com/Monster-Endeavors/claude-seo-skills/raw/main/dist/query-fan-out.zip) |
| [SERP and topic gaps](skills/serp-topic-gaps/SKILL.md) | Reads what ranks for a keyword and lists what your page is missing | Yes, with web search on in Claude. Content briefs need a plan | [serp-topic-gaps.zip](https://github.com/Monster-Endeavors/claude-seo-skills/raw/main/dist/serp-topic-gaps.zip) |
| [Content QA](skills/content-qa/SKILL.md) | Checks a draft before it's published, from on-page basics to typos, unsourced claims and AI-sounding wording | Partly. The AI-judged checks need a plan | [content-qa.zip](https://github.com/Monster-Endeavors/claude-seo-skills/raw/main/dist/content-qa.zip) |
| [Brand voice](skills/brand-voice/SKILL.md) | Writes a voice and tone guide from the pages that sound like your brand, with every rule backed by a line from them | Partly. Writing the guide works anywhere, and saving it to MetaMonster needs a plan | [brand-voice.zip](https://github.com/Monster-Endeavors/claude-seo-skills/raw/main/dist/brand-voice.zip) |

<!-- TODO (Austin): confirm the plan rows the tool descriptions don't settle: site settings and usage, work items, content edits and fixes, the Context Library, publishing hand-off and Drift. -->

## Install in Claude

In Claude on the web or desktop:

1. Download the skill's zip from the table above and keep it zipped.
2. Skills need file creation turned on. In Settings > Capabilities, turn on Create and edit files. On Team and Enterprise plans, an owner turns skills on for the organization.
3. Go to Customize > Skills, click +, then Create skill > Upload a skill, and pick the zip.
4. Turn the skill on.
5. Add MetaMonster from Claude's connector directory if you haven't yet. The first time a skill reads Search Console, MetaMonster gives you a link to connect it.
6. Ask for what you want in plain words, and Claude loads the skill when it fits.

In Claude Code, skills you've uploaded in Claude load automatically when you sign in with the same account (v2.1.273 or later; run `/skills` to see them). You can also copy a skill's folder from `skills/` into `~/.claude/skills/`.

Using ChatGPT? Each skill's page on the MetaMonster site has a plain prompt you can paste instead.

## Start for free

Start for free with the MetaMonster MCP: TODO signup link, with utm_source=metamonster-skills and a utm_campaign per skill.

## How the zips stay current

Each zip in `dist/` holds its skill's folder, ready to upload. They're rebuilt automatically from `skills/` on every push to `main`, and a pull request fails its check if a zip doesn't match its folder. To rebuild them yourself, run:

```
python3 scripts/build_zips.py
```

## Contributing

Edit the skill in `skills/<name>/SKILL.md`, run the build script, and open a pull request with the folder and its zip. Skills only describe what MetaMonster's tools do today, and they never invent facts, numbers or quotes for a site.

## Still to do

- [ ] Add the signup link, with UTMs.
- [ ] Link the skills hub at metamonster.ai/skills/ once it's live.
- [ ] Confirm the "To confirm" plan rows with Austin.
- [ ] Confirm whether CMS publishing will come to the connector, since the MetaMonster skill hands drafts off through the site's code for now.
- [ ] Add a license.
