# 🚀 News & Event Heat 🔥 Credit Spread Screener

Work in Progress... The script is pulling live market data from tastytrade server. GPT 5 and GROK 4 handle news and events.  Need a tool or automation for your project or idea? Hit me up, and I’ll build it from scratch!  

---

# 🪐 Define ETF Universe & Screen Tickers for Catalysts 🏆

## ▪️ Prompt for top 3 tickers/sector.

### ◽️ GROK 4 & GPT 5 (input)
```python
# Credit Spread Selection Prompt

You are tasked with identifying 27 high-probability credit spread candidates (3 per sector) using only web search and public information analysis.


# FOUNDATION (9 Core Search Points)

1. **Sector Holdings Discovery:** Search "[sector ETF] holdings 2025" for XLC, XLY, XLP, XLE, XLF, XLV, XLI, XLK, XLU. Also search "best [sector name] stocks 2025" to find non-SPDR alternatives.

2. **Earnings Calendar Scan:** Search "[ticker] earnings date" and "[ticker] Q3 2025 earnings" to identify and exclude any ticker reporting within 35 days.

3. **Recent SEC Filings:** Search "site:sec.gov [ticker] 8-K" for material events in past 7 days. Prioritize stable operational updates over major restructuring.

4. **Institutional Activity:** Search "[ticker] unusual options activity today" and "[ticker] dark pool activity" to identify where smart money is positioning.

5. **Technical Sentiment:** Search "[ticker] technical analysis" on financial sites to find current RSI readings and trend descriptions (overbought/oversold/neutral).

6. **Analyst Movement:** Search "[ticker] analyst upgrade downgrade this week" to capture recent institutional sentiment shifts.

7. **Volatility Context:** Search "[ticker] implied volatility" and "[ticker] options volume" to identify elevated premium selling opportunities.

8. **Support/Resistance Mentions:** Search "[ticker] key levels" and "[ticker] support resistance" to find commonly cited price levels from technical analysts.

9. **Comparative Strength:** Search "[ticker] vs [sector ETF] performance" to identify relative outperformers/underperformers within each sector.


#PROCESS (6 Execution Steps)

**1. Triple Source Verification:** For each data point, find 3 different sources mentioning similar information. If only 1 source exists, mark as "unverified" in output.

**2. News Recency Scoring:**
  - Last 24 hours = 3 points
  - Last 3 days = 2 points
  - Last 7 days = 1 point
  - Older = 0 points
  - Prioritize tickers with score ≥4 from multiple news items

**3. Sentiment Aggregation:** Count bullish vs bearish mentions across all search results:
  - Strong directional bias (>70% one direction)** = ideal for credit spreads
  - Mixed sentiment (40-60%)** = avoid
  - Search terms:** "bullish on [ticker]", "bearish on [ticker]", "[ticker] price target"

**4. Options Activity Validation:** Search "[ticker] put call ratio" and "[ticker] options flow". High put/call ratio (>1.5) suggests bear call setup; low (<0.7) suggests bull put.

**5. Volatility Rank Approximation:** Search "[ticker] IV rank" or "[ticker] implied volatility historical". If current IV mentioned as "elevated" or "above average" in multiple sources, mark as favorable.

**6. Risk Event Scanning:** Search "[ticker] FDA approval", "[ticker] lawsuit", "[ticker] merger", "[ticker] regulatory". Exclude any ticker with binary events within 45 days.

# OUTPUT (3 Requirements)

**1. Confidence Scoring:

- HIGH (7-9 verified data points found)
- MEDIUM (4-6 verified data points found)
- LOW (1-3 verified data points found)

##2. JSON Structure with verifiable data only:

json{
  "scan_timestamp": "2025-08-25T10:00:00Z",
  "total_tickers_analyzed": 120,
  "final_selections": 27,
  "sectors": {
    "Communication Services": {
      "etf": "XLC",
      "alternatives_checked": ["FCOM", "VOX"],
      "tickers": [
        {
          "symbol": "META",
          "confidence": "HIGH",
          "data_points_found": 8,
          "earnings_days_away": 89,
          "recent_news_sentiment": "bullish",
          "analyst_actions": "2 upgrades this week",
          "options_activity": "unusual call buying detected",
          "technical_mention": "oversold per 3 sources",
          "suggested_bias": "bull-put",
          "sources": ["reuters.com", "benzinga.com", "optionshawk.com"]
        }
      ]
    }
  }
}

**3. Fallback Protocol:** If cannot find 3 HIGH/MEDIUM confidence tickers in a sector:
  - First expand to top 10 holdings of sector ETF
  - Then check competing sector ETFs (iShares, Vanguard)
  - Finally include best available with "LOW" confidence flag
  - Never fabricate data - mark as "insufficient_data" if needed



# SEARCH EXECUTION PATTERNS

**1. For each ticker, execute in this order:**
  - "[ticker] stock price today" - Verify it's trading
  - "[ticker] earnings date 2025" - Event avoidance
  - "[ticker] news this week" - Catalyst check
  - "[ticker] unusual options activity" - Smart money
  - "[ticker] analyst rating change" - Institutional view
  - "[ticker] technical analysis oversold overbought" - Entry timing
  - "[ticker] implied volatility" - Premium check

# CRITICAL RULES

  - Never invent data - use "not_found" for missing information
  - Each ticker must have at least 3 verified data points
  - Prioritize liquid names mentioned across multiple sources
  - If conflicting information found, note it explicitly
  - Timestamp all searches to acknowledge data delay

Focus on finding real, verifiable information that suggests directional bias and elevated options activity.
Quality over quantity - better to have 20 excellent candidates than 27 mediocre ones.
```
---

# 🛠 Set Tastytrade Credentials

**`config.py`** Stores API URL and login credentials, imported and used by other scripts.

---

# 🤖 Analyze Credit Spreads via Pipeline

## ▪️ How to Execute 

Run `individual steps` or use the `master pipeline`

```python
# Individual steps:

# `sectors.py` Sets tickers for querying.
python3 sectors.py

# `build_universe.py` Tests tickers for options chains.
python3 build_universe.py

# `spot.py` Fetches current stock prices for strikes.
python3 spot.py

# `ticker_ranker.py` Ranks stocks by options liquidity.
python3 ticker_ranker.py

# `options_chains.py` Downloads option contracts for spreads.
python3 options_chains.py

# `greeks.py` Gets option prices and Greeks for PoP/ROI.
python3 greeks.py

# `spread_analyzer.py` Builds spreads, calculates PoP/ROI, picks best.
python3 spread_analyzer.py


# OR run everything at once:

python3 master.py
```

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
