# 🚀 News & Event Heat 🔥 Credit Spread Screener

Work in Progress... The script is pulling live market data from tastytrade server. GPT 5 and GROK 4 handle news and events.  Need a tool or automation for your project or idea? Hit me up, and I’ll build it from scratch!  

---

# 🛠 Set Tastytrade Credentials

**`config.py`** Stores API URL and login credentials, imported and used by other scripts.

---

# 🪐 Define ETF Universe

## ▪️ Attach Trading Universe

`XLK` https://www.sectorspdrs.com/mainfund/XLK

`XLC` https://www.sectorspdrs.com/mainfund/XLC

`XLY` https://www.sectorspdrs.com/mainfund/XLY

`XLP` https://www.sectorspdrs.com/mainfund/XLP

`XLV` https://www.sectorspdrs.com/mainfund/XLV

`XLF` https://www.sectorspdrs.com/mainfund/XLF

`XLI` https://www.sectorspdrs.com/mainfund/XLI

`XLE` https://www.sectorspdrs.com/mainfund/XLE

`XLU` https://www.sectorspdrs.com/mainfund/XLU

---

# 🏆 Screen Tickers for Catalysts

## ▪️ Prompt for 3 tickers per sector using news/events.


### ◽️ GROK 4 (input)
```python
# Prompt
## Foundation
1. Lock universe: Sector CSV tickers only; uppercase, dedupe; common stock; prioritize large-cap/index for liquidity/tight spreads (OI >400, volume >100, ATM spread ≤5%, per TradeStation/AlphaArchitect).
2. Fresh news: ≤7d credible coverage required; prioritize PR/EDGAR/IR/Govt > Tier-1 (Reuters/Bloomberg/WSJ); economic > social; multi-source confirmation +10% edge (MDPI). Skip without.
3. Prime window: ≤7d with multi-day follow-through preferred; backtests show 15-20% win boost for confirmed trends (arXiv/TradeStation).
4. Tradable heat: Steady reaction > gaps/halts; avoid ±10% gaps (83% 0DTE loss, TradeStation). Require durable move potential.
5. Source tiers: PR/EDGAR/IR/Govt > Tier-1; use X semantic/LLM for sentiment verification (positive/negative scale 0-100); multi-source boosts ROC 6% (arXiv).
6. Earnings guard: Exclude ≤33d; 94% win drop post-vol (TradeStation).
7. Binaries: FDA/votes/courts/product dates ≤33d → exclude; 70% short DTE failure; use alt-data (e.g., satellite for retail) if available (Berkeley Haas).
8. Imminent events: ≤24h scheduled → skip; gamma 2x spike (arXiv).
9. Sector balance: ≤3/sector; high IVR (50%+) for premium; balance bull/bear with macro (e.g., CPI/yields impact financials/energy); don't force.

## Edge Engine

1. Catalyst hunt: ≤7d; prioritize M&A/guidance/analyst upgrades/FDA/deals/product launches (durable > recency, 6% ROC boost, arXiv); confirm multi-source.
2. Rank: Durability (multi-day reaction) > Recency > Quality; boost S/R breakouts via X semantic/LLM sentiment (FinBERT-style scoring).
3. Bias: Bullish (positive sentiment >70) → bull put; Bearish (<30) → bear call; unclear → pass; align with 83-95% wins (arXiv). Use LLM for tone analysis.
4. Tone: Orderly > hot; theta in 7-33 DTE (85% QQQ 0DTE wins, TradeStation).
5. Score: High/Med/Low + why/citation; tiebreak: IV tailwind (>50%) or alt-data. Check "priced-in" (e.g., overbought sentiment).
6. Quant filter: Large-cap/index; 91% win vs 74% (AlphaArchitect); contrarian: Skip if news overbought (e.g., gap without volume).

## Execution

1. Pick: Top ≤3/sector clearing guards; focus low delta (5-10) for credits; AI as assistant (AlphaArchitect).
2. Flip: Open spread; +10% TP; headline stop; EOD time stop; verify sim.
3. Table: Sector | Ticker | Bias | Catalyst | Flip Plan | Edge | Sentiment Score (0-100) | Est. ROI | Risks |

---------

#Instructions

## Foundation

1. **Free data:** CSV tickers; Google/EDGAR/IR; no APIs/paywalls; X semantic for verification (mdpi.com).
2. **Confirmation:** Multi-source > solo; X as alert, confirm Tier-1; economic > social (mdpi.com).
3. **Liquidity:** Large-cap/index; proxy <1% ATM spread (tradestation.com).
4. **Themes:** Catalyst + sector tailwind/macro; e.g., XLE deals + oil rally (durability +15% ROC, arxiv.org).
5. **PR:** Guidance/buybacks/contracts > rumors; +15% ROC (alphaarchitect.com).
6. **Reaction:** Follow-through > pop; S/R wins via article/X context.
7. **Guards:** Earnings/binaries → drop; scheduled ≤24h → skip.
8. **Miss:** Uncertain → exclude; public only; add alt-data hints (satellite, haas.berkeley.edu).
9. **Advisory:** Sizing/fills managed; delta 5-10 edge (83-95% wins, arxiv.org); AI assistant (alphaarchitect.com).

## Edge Engine

1. **Recency:** ≤72h > old; +20% conviction (mdpi.com).
2. **Themes:** Backtested wins e.g., 94% SPX 0DTE (tradestation.com).
3. **IV:** High relative >20%; premium edge.
4. **Heat:** Tradable > chaos; gamma <7 DTE.
5. **Bias:** Match spread; bull put +ve news; sentiment via X semantic.
6. **Score:** Transparent; win rate data; what-if risks (arxiv.org).

Execution

1. **Output:** Table; sort score.
2. **Plan:** +10% TP; headline/time stops.
3. **Limit:** 3/sector; data exclusions; contrarian filters.
```


### ◽️ ChatGPT 5 (input)

```python

# Master Prompt: News_Spread_Engine (Universe → Catalyst Screen)

You are an eliet AI analyst. Follow every rule exactly. Only use tasks GPT can execute: reading lists, scanning public news/filings, classifying sentiment, and formatting JSON. Do not invent data or use paywalled APIs.

Foundation Rules:
1. Universe lock: Use only the attached sector CSV tickers. If none are attached, pull constituents from free ETF issuer sites (SPDR/iShares/Vanguard). Deduplicate. Exclude ETFs/indices.
2. Recency discipline: Only consider catalysts ≤7 days old; prioritize ≤72h.
3. Source tiers:
  First: company PR, SEC/EDGAR, IR/government filings.
  Then: Tier-1 outlets (Reuters, Bloomberg, WSJ, CNBC, Yahoo Finance).
  Social/X only as alerts; must confirm with ≥1 credible source.
4. Event guard: Exclude tickers with credible news showing earnings, FDA/court/vote/product binaries within 33 days, or scheduled in next 24h.
5. Liquidity proxy: Favor large-cap names; tag smaller/illiquid ones as "filler".
6. Tone filter: Skip halted/gapped/whipsaw narratives. Favor “orderly drift / follow-through.”
7. Sector balance: Always return 3 per sector (27 total). If fewer pass, backfill from universe as "filler".

Edge Engine:
1. Sentiment classify: Bullish → "put-credit"; Bearish → "call-credit"; Unclear → "filler".
2. Confirm: Require ≥2 credible sources per ticker. If only one, mark "Low".
3. Durability: Rank guidance raises, contracts, buybacks, regulatory approvals > one-off PR/hype.
4. Thematic tailwind: Add bonus if aligned with sector/macro flow (oil↑ → Energy; yields↓ → Tech; consumer demand↑ → Discretionary).
5. Score: "High", "Medium", "Low", or "Filler". Tie-break: Durability > Recency > Source quality.
6. Thesis: Write ≤30 words linking catalyst → bias. Always include 2–3 source links.

Execution
1. Selection: Always exactly 27 tickers (3 per sector). Strongest first, filler last.
2. Flip plan (standardized): "Open aligned credit spread; +10% TP; headline stop; time stop (EOD/next)."
3. Output format: JSON only. Schema:
---
{
  "Communication Services": {
    "ETF": "XLC",
    "Description": "Media, ads, platforms",
    "Tickers": [
      {
        "ticker": "DIS",
        "bias": "put-credit",
        "catalyst": "Streaming subscriber growth beat; bullish sentiment",
        "strength": "High",
        "sources": ["https://...", "https://..."]
      },
      {
        "ticker": "NFLX",
        "bias": "call-credit",
        "catalyst": "Mixed reviews on new pricing; cautious tone",
        "strength": "Medium",
        "sources": ["https://...", "https://..."]
      },
      {
        "ticker": "T",
        "bias": "filler",
        "catalyst": "No strong catalyst; backfill",
        "strength": "Filler",
        "sources": []
      }
    ]
  },
  "Consumer Discretionary": {
    "ETF": "XLY",
    "Description": "Cyclical demand, sentiment",
    "Tickers": [...]
  }
  // ... repeat for all 9 sectors, 3 tickers each
}
---
```



# 🤖 Analyze Credit Spreads via Pipeline

## ▪️ How to Execute 

Run `individual steps` or use the `master pipeline`

```python
# Individual steps:

python3 sectors.py
python3 build_universe.py  
python3 spot.py
python3 ticker_ranker.py
python3 options_chains.py
python3 greeks.py
python3 spread_analyzer.py

# OR run everything at once:

python3 master.py
```
---

## ▪️ Definitions:


**`sectors.py`** Sets tickers for querying.

**`build_universe.py`** Tests tickers for options chains.

**`spot.py`** Fetches current stock prices for strikes.

**`ticker_ranker.py`** Ranks stocks by options liquidity.

**`options_chains.py`** Downloads option contracts for spreads.

**`greeks.py`** Gets option prices and Greeks for PoP/ROI.

**`spread_analyzer.py`** Builds spreads, calculates PoP/ROI, picks best.

---



# 💯 Generate Strategy and Game Plan

## ▪️ Prompt for Report with Catalyst Heat, Bias, and Trade Plan.


### ◽️ GROK 4 (input)

```python
# Prompt 

## Foundation

1. **Parse:** JSON fields; %/$ → floats; guard NaN/negatives.
2. **Derive:** Width = |long-short|; credit = Net_Credit; max_loss = width-credit; R:R = credit/max_loss >0.33.
3. **Sanity:** Order legs bull put/bear call; de-dupe Ticker+Type+Legs+DTE.
4. **Scope:** 0-33 DTE; tag 7-21 optimal (6% ROC, tradestation.com), 22-33 acceptable, <7 gamma-hot.
5. **Buffer:** Distance_From_Current; <0.5% thin; +8% edge ≥0.5% (tradestation.com).
6. **Catalyst:** ≤72h confirm; PR/8-K > media; multi-source via X semantic (mdpi.com).
7. **Direction:** Bullish → bull put; Bearish → bear call; mismatch → skip.
8. **Guards:** Earnings/binaries ≤33d → drop; ≤24h event → skip; chaos/gaps → too hot.
9. **Score:** ROI_cap=200, w_ROI=0.35, w_DIST=8; bonuses +6 (7-21), +3 (22-33), -5 (<7); POP ≥65%.

## Edge Engine

1. **Width:** -4 (<$1), +2 ($3-5), -4 (>$10); $3-5 sweet (tradestation.com).
2. **Formula:** Score = POP + 0.35ROI_cap + 8buffer% + DTE_bonus + Width_adj.
3. **Enter:** Bias match + high score + buffer ≥0.5% + not hot.
4. **Hold:** Aligned but thin/aging → watchlist.
5. **Skip:** Mismatch/binaries/chaos/no confirm.
6. **Quant:** Delta 5-10 equiv (83-95% wins, alphaarchitect.com); alt-data boost (satellite, haas.berkeley.edu); LLM predictive (arxiv.org).

## Execution

1. **Table:** AI Bot | Sector | Ticker | Type | Legs | DTE | PoP | ROI | R:R | Buffer% | Score | Bias | Catalyst | Action | Flip Plan | Citation(s).
2. **Sort:** Score ↓; top 1/ticker post de-dupe.
3. **Plan:** Open spread; +10% TP; headline stop; time stop (EOD/next).

---------

# Instructions 

## Foundation

1. **JSON:** Math/filters/score from fields; no live IV/Greeks.
2. **News:** PR/EDGAR/IR/Tier-1; earnings via IR/web; economic > social (mdpi.com).
3. **No chains:** Algo strikes/premiums.
4. **Outlook:** Match spread to catalyst; ≤72h recency.
5. **Heat:** Follow-through > halts; theta 7-21 DTE (94% wins, tradestation.com).
6. **IV:** Proxy high via news; drop <20%.
7. **Guards:** Binaries/earnings → drop; mismatch → skip.
8. **Width:** $3-5 practical; avoid extremes.
9. **Score:** Transparent; ROI cap >120% diminishing; macro/alt context (haas.berkeley.edu).

# Edge Engine

1. **POP:** Base 70-95% (backtests SPY/QQQ, arxiv.org).
2. **ROI:** Payout/risk; +theta short DTE.
3. **Buffer:** ≥0.5% safety; gamma <7 DTE.
4. **DTE:** 7-21 sweet (94% wins); 22-33 ok.
5. **Catalyst:** Multi-source > stale; tailwind durability; X sentiment.
6. **Action:** Enter high + aligned; watch thin; what-if risks (alphaarchitect.com).

## Execution

1. **Table:** Specified columns; dedupe.
2. **Plan:** +10% TP; headline/time stops.
3. **Output:** Markdown; 1/ticker; AI as assistant (alphaarchitect.com).
```

### ◽️ ChatGPT 5 (input)
```python
# Prompt

## Foundation

1. **Parse:** JSON fields only; convert %/$ → floats; guard NaN/negatives.
2. **Derive:** Width=|short−long|; Credit=Net_Credit; Max_Loss=Width−Credit; **R:R=Credit/Max_Loss > 0.33**.
3. **Sanity:** Validate leg order for bull put / bear call; de-dupe Ticker+Type+Legs+DTE.
4. **Scope:** Keep **0–33 DTE**; tag **7–21 optimal**, **22–33 acceptable**, **<7 gamma-hot** (tradestation.com).
5. **Buffer:** Use Distance_From_Current as **Buffer%**; **<0.5% thin**; ≥0.5% provides better protection (tradestation.com).
6. **Catalyst link:** Require **≤72h** confirm; **PR/8-K/IR/Govt > media**; allow X semantic as lead but verify (mdpi.com).
7. **Direction map:** **Bullish → bull put; Bearish → bear call;** mismatch → **skip**; LLM news labels can set bias (arxiv.org).
8. **Guards:** **Drop** earnings/binaries within DTE; **skip** if scheduled **≤24h**; exclude “too hot” chaos/gaps.
9. **Score scaffold:** `ROI_cap=200`, `w_ROI=0.35`, `w_DIST=8`; DTE bonus **(+6:7–21, +3:22–33, −5:<7)**; **PoP ≥ 65%** baseline.

## Edge Engine

1. **Width adj:** **−4** (<$1), **+2** ($3–$5), **−4** (>$10); $3–$5 sweet spot (tradestation.com).
2. **Score formula:** `Score = PoP + 0.35·min(ROI,200) + 8·Buffer% + DTE_bonus + Width_adj`.
3. **Enter:** Bias match + high Score + Buffer ≥0.5% + not hot → **Enter**.
4. **Watch:** Aligned but thin buffer or aging news (>72h) → **Watchlist**.
5. **Skip:** Mismatch / binaries / chaos / no confirmation → **Skip**.
6. **Quant adds:** Favor conservative deltas (small-delta bias improves success; alphaarchitect.com); allow alt-data boost (satellite/foot-traffic, haas.berkeley.edu); LLM predictive support (arxiv.org).

## Execution

1. **Table:** AI Bot | Sector | Ticker | Type | Legs | DTE | PoP | ROI | R:R | Buffer% | Score | Bias | Catalyst | Action | Flip Plan | Citation(s).
2. **Sort:** Score ↓; 1 entry per ticker after de-dupe.
3. **Plan:** “Open credit spread; +10% TP; headline stop; time stop (EOD/next).”

---------

# Instructions

## Foundation

1. **JSON only:** Compute all metrics from JSON; no live IV/Greeks/quotes.
2. **News rules:** PR/EDGAR/IR/Tier-1 only; earnings/binary checks via IR/calendars; **economic > social** signal (mdpi.com).
3. **No chains:** Strikes/premiums handled by your engine; this prompt aligns/filters/scores.
4. **Outlook fit:** Spread direction must match catalyst; prefer ≤72h news; multi-confirm.
5. **Heat discipline:** Favor follow-through language; prefer 7–21 DTE theta capture (tradestation.com).
6. **IV proxy:** Use news context to infer regime; deprioritize clearly low-IV unless buffer/PoP strong.
7. **Guardrails:** Drop binaries/earnings within DTE; skip mismatch or “too hot” tapes.
8. **Width practicality:** $3–$5 preferred; avoid <$1 or >$10 for fill/ROC quality.
9. **Transparent scoring:** Cap ROI to avoid outliers; allow macro/alt-context as a nudge (haas.berkeley.edu).

## Edge Engine

1. **PoP sanity:** 65–90% typical for conservative spreads; beware tail risk even at high PoP (arxiv.org).
2. **ROI vs risk:** Favor stable R:R with sufficient credit; avoid “juicy” but thin-buffer setups.
3. **Buffer rule:** ≥0.5% required; below this needs exceptional Score.
4. **DTE sweet spot:** 7–21 preferred; 22–33 okay; <7 only with strong timeboxed catalyst plan.
5. **Catalyst quality:** Multi-source and sector tailwind; include X only when verified.
6. **Action map:** Enter (high+aligned), Watch (thin/aging), Skip (any guard). Add 1-line “what-if” risk.

## Execution

1. **Table:** Use specified columns; de-dupe.
2. **Plan:** +10% TP; headline/time stops.
3. **Output:** Markdown; 1/ticker; AI acts as assistant (alphaarchitect.com).
```
