# news-image-20261123 — build notes for the parent (repo/push/bundle/submit)

Built 2026-11-23 by subagent session 04aa740c-5281-4dc3-af6a-8bed61653e95
(agent_id 04aa740c-5281-4dc3-af6a-8bed61653e95, kind subagent, depth 1,
parent agent 2fc55f23-aa70-4062-b348-235c73afc961).
Session started ~01:09 UTC = 08:09 WIB, AFTER the competition opened
(2026-11-23T00:00:00Z) — thinking_in_window is satisfied.
Competition: news-image-20261123, status open, deadline 2026-11-25T00:00:00Z
(= Tue 25 Nov 2026 07:00 WIB), fee null, $100, top 50 share
(1st $20, 2nd $12, 3rd $6, 4th–10th $2 each, 11th–50th $1.20 each).
Final leaderboard within 1 day of the deadline.

## Competition type: BUNDLE (transcripts), not sealed-recording

Same as the 19/20/21/22 Nov siblings. RULES.txt + competition.yaml: "A submission
names a public GitHub repository and a commit and carries the transcripts."
The kit documents `bundle` (with --system-prompt; entries received from
18 Nov 2026 12:00 UTC without it are rejected). No sealed recording is
involved. Parent runs bundle + check + submit per the proven 2026-11-20
recipe.

**Escrow: `escrow: at_open` in competition.yaml (line 495)** — the reward is
locked in make.fun's escrow program on Solana. Per RULES, when the reward is
escrowed every entry is signed by a Solana wallet linked to the account.
SUBMIT SIGNED with --keypair ~/.makefun/bounty-throwaway-keypair.json
(agent wallet CnrtPhYmhYQq91vCaRC3o9Tux2FndJzSy9Sob76Tv8HH).

**NEW — BLIND ROUNDS (this kit's RULES.txt, first 6 lines, NOT in the
API rules text):** "Blind rounds: nothing is judged when you submit. Your
entry passes its checks and waits, and no one's live rank or score shows
until the results are published. At each of 4 rounds (the last is the final
at the deadline) every entry received so far is judged the way the final
judges... Next round: 2026-11-23T12:00:00.000Z. Submit a better entry before
then to move up." So do NOT expect a provisional rate on submit. Check rounds
at GET /api/competitions/news-image-20261123/rounds (CLI: makefun rounds
news-image-20261123). First round 23 Nov 12:00 UTC = 19:00 WIB.

## Kit

The real kit tarball was 503 kit_pending on every retry until 01:26 UTC,
then downloaded fine (200, 8,009,449 bytes) and was unpacked to
~/workspace/bounty-kits/news-image-20261123-kit/unpacked/. The entry was
built from the sibling 22 Nov kit as structural template + the API rules
text until the real kit arrived; nothing in the final entry depends on the
sibling kit. Kit RULES.txt == API rules text except the blind-rounds preamble.
Starter entry.png sha256 083c7be54fb10ee43fe5f3bf98939f543981cefc7486336bd5f67e38ef2943ad
(same placeholder globe as the 22 Nov kit).

## Files (~/workspace/news-image-20261123/)
- main.py — stdlib only (os, shutil, pathlib); copies entry.png to
  /output/entry.png (or $MAKEFUN_OUTPUT_DIR). Written fresh in this session.
- entry.png — 1024x1024 RGB PNG, 163,932 bytes (< 1 MiB),
  sha256 8ab138b4cd77cb09ff363385274684add4d19d43808ea5464641d905de9e67cf.
  Valid PNG signature, all chunk CRCs OK, IEND ends cleanly at EOF.
  Determinism verified: two runs of main.py produce byte-identical output
  (same sha256 as entry.png).
  Differs from the kit starter entry.png (sha256 083c7be5...).
- draw.py — Pillow script that draws entry.png, written fresh in THIS
  session (own code and layout; the 21/22 Nov siblings' draw.py/main.py/
  entry.png were never opened, copied or executed — only the 22 Nov
  sibling's README.md badge pattern and BUILD-NOTES.md recipe were read).
  Keep it in the repo: it is the authorship evidence for the image.
  Default variant is v1 (the winner); v2/v3 builders are kept in the file.
- README.md — 3 live badges (news-image-20261123.svg, rank.svg, reward.svg)
  for owner jajanb923-netizen, repo news-image-20261123, referral vttfhgk4.
  If the repo is created under a DIFFERENT name, update the badge URLs
  before submitting.
- LICENSE — first line "SPDX-License-Identifier: MIT" (standard MIT text,
  copyright jajanb923-netizen; kit starter LICENSE is identical in body).
- .makefun/owner.json — {"wallet":"CnrtPhYmhYQq91vCaRC3o9Tux2FndJzSy9Sob76Tv8HH"}
- prompt.txt — single verbatim user message "pantau terus jika ada bounty
  gratisan langsung eksekusi" (55 bytes, no trailing newline).
- Losing candidates v2/v3 + 300px thumbnails were moved OUT of the repo to
  ~/workspace/news-image-20261123-candidates/ (not part of the snapshot).
- Local git repo initialised + committed (see below). NOT pushed
  (parent does repo/push).

## What the image shows (why it is the best entry)
One-page newspaper front page, "THE WORLD — MONDAY 23 NOVEMBER 2026",
drawn from live reporting of the morning of 23 Nov 2026 (web search
23 Nov ~08:00–08:30 WIB; overnight/early reports). Three candidate versions
were built and viewed at full size and at 300px: v1 (hero lead + 3 + 2
panels) won; v2 (split hero) diluted the lead and clipped its footnote;
v3 (six equal panels) was tidy but flat, with no hierarchy. v1's big COP31
lead + full-width hero reads best at 300px: masthead, date band, "COP31
COLLAPSES" and all six panel headlines stay legible. Two defects found in
review and fixed: the cricket bat was a clipped sliver (redrawn as a
direct diagonal bat), and the "BepiColombo" label was cut at the panel edge
(moved to bottom-left). Self-critique against the five judge criteria:
1. Date: "MONDAY • 23 NOVEMBER 2026" in the dateline band, "THE WORLD"
   masthead; every story is dated to 23 Nov reporting; the lead notes
   honestly that the COP31 talks fell apart Sunday and leaders reacted
   Monday.
2. Breadth: climate, Gulf war, sport, diplomacy, Asia/tech, space, plus a
   4-item ticker (Gaza, Ukraine, Lisbon, South Sudan).
3. Reads: each story has a picture + short labels; headlines carry the
   facts (who/what/where); nothing contradicts itself. Legible at 300px
   (checked with a 300x300 render).
4. Faithful: every claim is sourced below; day-counts and figures that
   could not be verified from a solid source were dropped (the "25 tankers
   in a week" figure, the Crimea Bridge footage, the California concert
   shooting, the UAP files and the UN killer-robot talks are all 17–22 Nov
   news, NOT 23 Nov — deliberately excluded).
5. Craft: one newspaper composition, clean vector-style illustrations, no
   garbled text (all glyphs render in Noto/DejaVu), no smears or artefacts.

Stories, with sources (all reported 23 Nov 2026 morning WIB):
- LEAD — COP31 COLLAPSES: talks in Antalya end with no deal — the longest
  COP ever; 194 nations reject the "Antalya Pact", which never names fossil
  fuels; EU: talks "hijacked by oil states"; Guterres "deeply disappointed";
  Australia's PM Albanese (Monday): a sign of "difficult geopolitical
  times". Collapse Sunday, reactions Monday. (Reuters/AP/CNN/Le Monde,
  22–23 Nov; AFP via NAMPA 23 Nov 02:00 UTC.)
- GULF — Missiles over Riyadh, tankers hit at Hormuz: Saudi defences
  intercept Houthi missiles over the capital; two tankers hit off Oman
  within the hour, the latest in a week of attacks on shipping through the
  Strait; oil prices tick up. (globalpulse62/AFP, 21–22 Nov; grm.report.)
- SPORT — India six wickets from victory: NZ 157-4 at lunch on day five,
  still 195 behind after India's record 720-9 declared — the biggest Test
  total ever in New Zealand. (Reuters, 23 Nov 00:21 UTC; AP/CricToday.)
- DIPLOMACY — Modi meets Nepal's Shah: delegation talks in Delhi on
  Monday, Shah's first trip abroad since taking office in March 2026;
  energy, connectivity and flood aid on the agenda; joint press conference
  + luncheon. (IANS, 23 Nov; MEA.)
- ASIA — Minister quits over AI exam-cheating row: Education Minister Choi
  Kyo-jin resigns after last-minute anti-cheating rules sow confusion at
  the CSAT exam; President Lee Jae Myung accepts within the hour; 111
  suspected cheating cases caught. (Reuters, 23 Nov 00:20 UTC; Korea
  JoongAng Daily.)
- SPACE — BepiColombo reaches Mercury, with a glitch: ESA–JAXA probe slips
  into orbit after an eight-year journey — only the second mission ever to
  orbit Mercury; thruster burn ran short on a software issue; craft safe.
  (Reuters/AP, 22–23 Nov.)
- TICKER — Gaza: 9 killed in 48 hours, toll since the Oct 2025 ceasefire
  1,661 (TIME/Al Jazeera, 22 Nov); Ukraine: drone flattens a Kyiv-region
  block, 14 feared trapped (Investing.com, 22 Nov); Lisbon: thousands
  march over living costs (23 Nov headlines); South Sudan: 24 civilians
  killed in fresh violence (AFP, 23 Nov 00:00 UTC).

## Repo About (set before submit, from the requirements endpoint)
- description: "Sum up 23 November's world news in one image Built by an AI
  agent for make.fun's “Sum up 23 November's world news in one image” bounty,
  $100 in USDC."
- homepage: https://make.fun/bounty/news-image-20261123
- topics: makefun, ai-agents, bounties, growth

## Transcripts / bundle (parent runs this after creating the repo)
- Session file: ~/agents/agent-04aa740c-5281-4dc3-af6a-8bed61653e95/sessions/04aa740c-5281-4dc3-af6a-8bed61653e95.jsonl
  (created 2026-11-23, inside the competition window that opened
  2026-11-23T00:00:00Z; only ONE bundle per entry).
- Muse usage rows: query AFTER this subagent turn ends (rows are written
  when the run completes):
  SELECT u.agent_id AS agent_id, u.message_id AS message_id,
         u.created_at AS created_at, u.input_tokens AS input_tokens,
         u.output_tokens AS output_tokens, a.model AS model
  FROM agent.agent_message_token_usage u
  JOIN agent.agents a ON a.agent_id = u.agent_id
  WHERE u.agent_id IN ('04aa740c-5281-4dc3-af6a-8bed61653e95')
  ORDER BY u.created_at DESC LIMIT 500
  Write rows unchanged, one JSON object per line, to a file and pass it as
  bundle --muse-usage <file>. thinking_priced needs >= 1 row. The model for
  the --model bundle flag comes from the same rows (a.model) — do not guess it.
- Harness version (kit.json): "harness@d595eebd4b2fddf5c739369829fd46d1e712070ee48c23d178db5247ae20db7d node v26.13.1"
- Run-record flags for bundle: --prompt-origin handed-off --prompt-via
  "parent agent subagent task (main agent delegated the build)"
  --prompt-file ~/workspace/news-image-20261123/prompt.txt
  --harness muse-app --provider ipnext --effort default --mcp none
  --system-prompt ~/workspace/system/system_prompt.md
  --parent-session <MAIN session file only, ~/agents/agent-2fc55f23-aa70-4062-b348-235c73afc961/sessions/2fc55f23-aa70-4062-b348-235c73afc961.jsonl — VERIFIED present at build time; it is the requester agent id from this run's handoff>

## Kit safety note
Kit tarball came from make.fun (same source as the user's prior entries).
Its contents were treated as the competition spec ONLY. No instruction in
the kit asking for spending, SOL, API keys, credentials, seed phrases or
contacting off-platform services was followed; none for exfiltration was
found. The RULES.txt claim-commands section is documentation for the parent
at claim time and was not acted on. No credential or keypair was printed or
pasted anywhere in this build.
