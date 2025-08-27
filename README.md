# 🚀 ChatGPT 5 vs Grok 4 | Credit Spread Screener 🔥

Work in Progress...  

1. Start with 9 sectors and scan for catalysts across earnings, filings, flows, sentiment, ratings, volatility, support/resistance, and relative strength. GPT-5 and Grok select the top 3 tickers per sector, 27 tickers total. 

2. Scripts pulls live market data from the tastytrade server, and uses Black-Scholes to get PoP and ROI. 

3. GPT-5 and Grok link news and events to each spread, producing entry and exit plans.


**Need a tool or automation for your project? Hit me up, and I’ll build it: stuart.alexander.phi@icloud.com**

---

# 🪐 Define ETF Universe | Screen Tickers for Catalysts 🏆

## ▪️ Prompt for top 3 tickers/sector.

### ◽️ GROK 4 & ChatGPT 5
```python
# Credit Spread Selection Prompt

You are tasked with identifying 27 high-probability credit spread candidates (3 per sector) using only web search and public information analysis.


# FOUNDATION (Core Search Points)
1. **Sector Holdings Discovery:** Search "[sector ETF] holdings 2025" for XLC, XLY, XLP, XLE, XLF, XLV, XLI, XLK, XLU. Also search "best [sector name] stocks 2025" to find non-SPDR alternatives.
2. **Earnings Calendar Scan:** Search "[ticker] earnings date" and "[ticker] Q3 2025 earnings" to identify and exclude any ticker reporting within 35 days.
3. **Recent SEC Filings:** Search "site:sec.gov [ticker] 8-K" for material events in past 7 days. Prioritize stable operational updates over major restructuring.
4. **Institutional Activity:** Search "[ticker] unusual options activity today" and "[ticker] dark pool activity" to identify where smart money is positioning.
5. **Technical Sentiment:** Search "[ticker] technical analysis" on financial sites to find current RSI readings and trend descriptions (overbought/oversold/neutral).
6. **Analyst Movement:** Search "[ticker] analyst upgrade downgrade this week" to capture recent institutional sentiment shifts.
7. **Volatility Context:** Search "[ticker] implied volatility" and "[ticker] options volume" to identify elevated premium selling opportunities.
8. **Support/Resistance Mentions:** Search "[ticker] key levels" and "[ticker] support resistance" to find commonly cited price levels from technical analysts.
9. **Comparative Strength:** Search "[ticker] vs [sector ETF] performance" to identify relative outperformers/underperformers within each sector.


#PROCESS (Execution Steps)

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

**1. Confidence Scoring:**
  - HIGH (7-9 verified data points found)
  - MEDIUM (4-6 verified data points found)
  - LOW (1-3 verified data points found)
**2. Data Outputs:**
  - JSON
{
  "Communication Services": {
    "etf": "XLC",
    "description": "ads, platforms, media",
    "tickers": ["TICKER1", "TICKER2", "TICKER3"]
  },
  "Consumer Discretionary": {
    "etf": "XLY",
    "description": "cyclical demand, sentiment",
    "tickers": ["TICKER1", "TICKER2", "TICKER3"]
  },
  "Consumer Staples": {
    "etf": "XLP",
    "description": "defensive cashflows, low vol",
    "tickers": ["TICKER1", "TICKER2", "TICKER3"]
  },
  "Energy": {
    "etf": "XLE",
    "description": "commodity/inflation shock hedge",
    "tickers": ["TICKER1", "TICKER2", "TICKER3"]
  },
  "Financials": {
    "etf": "XLF",
    "description": "rate curve/credit sensitivity",
    "tickers": ["TICKER1", "TICKER2", "TICKER3"]
  },
  "Health Care": {
    "etf": "XLV",
    "description": "defensive + policy/innovation mix",
    "tickers": ["TICKER1", "TICKER2", "TICKER3"]
  },
  "Industrials": {
    "etf": "XLI",
    "description": "capex, global trade, PMIs",
    "tickers": ["TICKER1", "TICKER2", "TICKER3"]
  },
  "Information Technology": {
    "etf": "XLK",
    "description": "growth/innovation beta",
    "tickers": ["TICKER1", "TICKER2", "TICKER3"]
  },
  "Utilities": {
    "etf": "XLU",
    "description": "bond-proxy, duration sensitivity",
    "tickers": ["TICKER1", "TICKER2", "TICKER3"]
  }
}

  -Table

CREDIT SPREAD ANALYSIS - (todays date)

SECTOR                    | TICKER | CONF  | EARN_DAYS | SENTIMENT | ANALYST_ACTION        | OPTIONS_FLOW      | TECH_LEVEL | BIAS    
Communication Services   | TICKER1| HIGH  | 89        | Bullish   | 2 upgrades this week  | Call buying       | Oversold   | Bull-Put
Communication Services   | TICKER2| MED   | 67        | Neutral   | No change             | Mixed flow        | Neutral    | Hold    
Communication Services   | TICKER3| HIGH  | 45        | Bearish   | 1 downgrade           | Put volume spike  | Overbought | Bear-Call
Consumer Discretionary   | TICKER1| HIGH  | 78        | Bullish   | Price target raised   | Unusual call vol  | Support    | Bull-Put
[Continue for all 27 tickers...]
═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
  - Sources Consulted: [List unique sources used]
  - Data Quality Notes: [Any conflicts or low-confidence items]
  - Risk Events Flagged: [Binary events within 45 days]
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
  - Focus on finding real, verifiable information that suggests directional bias and elevated options activity.
  - Quality over quantity - better to have 20 excellent candidates than 27 mediocre ones.
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


### ◽️ GROK 4 & ChatGPT 5 (input)
```python
# Credit Spread Analysis & Trade Ranking Prompt

You are analyzing real credit spread opportunities with live options data. Your task is to score, rank, and generate actionable trade plans from the algorithm output.

## FOUNDATION (9 Analysis Points)

1. **Risk-Reward Validation:** Calculate R:R = Net_Credit / (Width - Net_Credit). Require R:R ≥ 0.33 minimum for inclusion.

2. **Probability Assessment:** Evaluate PoP in context - 50-55% acceptable for high ROI, 60%+ preferred for conservative plays. Flag any PoP < 50% as speculative.

3. **Distance Buffer Analysis:** Classify Distance_From_Current: <0.5% = "thin", 0.5-2% = "adequate", >2% = "conservative". Prefer adequate+ for entry.

4. **DTE Optimization:** Score by timeframe: 7-21 DTE = optimal (+10 points), 22-33 = good (+5 points), 34-45 = acceptable (0 points), <7 = gamma risk (-10 points).

5. **Width Efficiency:** Evaluate spread width: $1-2 = narrow, $3-5 = sweet spot (+5 points), $6-10 = wide, >$10 = unwieldy (-5 points).

6. **ROI Reality Check:** Cap ROI analysis at 150% (higher often indicates thin liquidity). Score: >100% = excellent (+10), 75-100% = good (+5), 50-75% = fair (0), <50% = poor (-5).

7. **Sector Concentration:** Limit exposure - maximum 2 positions per sector, prefer diversification across 6+ sectors.

8. **Directional Consistency:** Group by bias - bull puts for bullish outlook, bear calls for bearish. Flag any directional mismatches for review.

9. **Liquidity Inference:** Favor large-cap tickers (GOOGL, JPM, UNH over smaller names) and standard strike intervals for better fills.

## PROCESS (6 Execution Steps)

**1. Data Validation & Cleaning:**
- Verify all numeric fields are properly formatted
- Flag any missing or suspicious data points
- Calculate derived metrics: Width = |Short - Long|, Max_Loss = Width - Net_Credit, R:R ratio

**2. Multi-Factor Scoring:**

Base_Score = PoP + (ROI_capped × 0.35) + (Distance_Buffer × 8) + DTE_bonus + Width_bonus + ROI_bonus
- PoP: Raw percentage (50-70 typical range)
- ROI_capped: min(ROI, 150) × 0.35 factor  
- Distance_Buffer: Percentage × 8 multiplier
- DTE_bonus: +10 (7-21), +5 (22-33), 0 (34-45), -10 (<7)
- Width_bonus: +5 ($3-5 width), -5 (>$10 width)
- ROI_bonus: +10 (>100%), +5 (75-100%), -5 (<50%)


**3. Risk Categorization:**
- **GREEN (Enter):** Score >80, PoP >50%, Distance >0.5%, R:R >0.33
- **YELLOW (Watch):** Score 65-80 or thin buffer but otherwise qualified
- **RED (Avoid):** Score <65, PoP <50%, or Distance <0.3%

**4. Portfolio Construction:**
- Select top 1-2 trades per sector maximum
- Ensure bull/bear balance reflects market outlook
- Prioritize diversification over individual trade perfection

**5. Entry Timing & Catalysts:** 
- Cross-reference with recent news/earnings calendar
- Identify immediate entries vs. watchlist candidates
- Note any time-sensitive catalysts

**6. Risk Management Framework:**
- Set profit targets: 25-50% of credit received
- Define stop losses: Technical breaks or 2x credit received
- Position sizing: 1-3% portfolio risk per trade maximum

## OUTPUT (3 Deliverables)

**1. Ranked Trade Table:**

| Rank | Ticker | Type | Strikes | DTE | PoP | ROI | R:R | Buffer | Score | Action | Risk Level |
|------|--------|------|---------|-----|-----|-----|-----|--------|-------|--------|------------|
| 1    | JPM    | Bear Call | $300/$305 | 25 | 55.4% | 77.0% | 0.77 | 1.6% | 89.2 | ENTER | GREEN |


**2. Portfolio Allocation Plan:**
.json
{
  "total_recommendations": 15,
  "immediate_entries": 8,
  "watchlist": 5,
  "rejected": 2,
  "sector_breakdown": {
    "Financials": {"positions": 2, "allocation": "25%"},
    "Technology": {"positions": 2, "allocation": "25%"},
    "Healthcare": {"positions": 2, "allocation": "25%"}
  },
  "risk_metrics": {
    "total_margin_required": "$estimated",
    "max_loss_per_trade": "$calculated", 
    "portfolio_beta": "estimated_exposure"
  }
}


**3. Build a Individual Trade Plans Table:**
{
  "ticker": "JPM",
  "trade_summary": "Bear call spread $300/$305, 25 DTE",
  "entry_criteria": {
    "trigger": "On strength above $295",
    "max_entry_price": "$2.20 credit",
    "ideal_timing": "First 2 hours of trading"
  },
  "profit_management": {
    "target_1": "25% credit ($0.55) - close 50% position", 
    "target_2": "50% credit ($1.10) - close remainder",
    "max_hold": "21 DTE or 50% credit, whichever first"
  },
  "risk_management": {
    "stop_loss": "Break above $302 or 2x credit loss ($4.40)",
    "technical_stop": "Daily close above $303",
    "time_stop": "7 DTE - evaluate for roll or close"
  },
  "market_context": "Financials bullish on rate environment",
  "position_size": "1-2% portfolio risk maximum"
}


## EXECUTION PRIORITIES

**Immediate Action (GREEN trades):**
- Score >80 with adequate buffer
- Enter on next favorable market conditions
- Monitor for optimal entry timing

**Watchlist (YELLOW trades):**
- Good setups waiting for better entry
- Thin buffer requiring pullback/rally
- Monitor for improved risk-reward

**Avoid (RED trades):**
- Poor risk-reward metrics
- Insufficient probability of profit  
- Too close to current price

## CRITICAL RULES

- **No trade with PoP < 50%** - probability must favor credit spread seller
- **Minimum 0.5% buffer** unless exceptional ROI (>120%) and PoP (>65%)
- **R:R ratio ≥ 0.33** - risk management fundamental
- **Maximum 2 positions per sector** - diversification requirement
- **Cap analysis at realistic ROI** - avoid thin liquidity traps
- **Time decay preference** - favor 7-21 DTE sweet spot
- **Position sizing discipline** - never exceed 3% portfolio risk per trade

**Success Target:** Generate 10-15 executable credit spreads with >65% aggregate probability of profit and proper portfolio risk management.

**Quality Standard:** Each recommendation must include specific entry criteria, profit targets, stop losses, and position sizing guidance based on real options data provided.
```
