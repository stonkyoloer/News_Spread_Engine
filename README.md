# 🚀 GPT5 vs Grok4 | Credit Spread Screener 🔥

Work in Progress...  

1. Start with 9 sectors and scan for catalysts across earnings, filings, flows, sentiment, ratings, volatility, support/resistance, and relative strength. GPT-5 and Grok select the top 3 tickers per sector, 27 tickers total. 

2. Scripts pulls live market data from the tastytrade server, and uses Black-Scholes to get PoP and ROI. 

3. GPT-5 and Grok link news and events to each spread, producing entry and exit plans.


**Need a tool or automation for your project? Hit me up, and I’ll build it: stuart.alexander.phi@icloud.com**

---

# 🪐 Define Universe | Screen Tickers 🏆

## ▪️ Prompt for top 3 tickers/sector.

### ◽️ GROK 4 & ChatGPT 5
```python
You are a financial markets research assistant.

### Task:
Search for recent market events, verify data points, and generate a Python script that defines a 45-ticker credit spread universe.

### Search & Verification Criteria:
1. **Earnings Movers (past 30 days)**  
   - Identify companies whose stock price moved by **more than 15%** on earnings.  
   - For each: report the **exact move percentage and date**.  
   - Verify that **options are tradeable**, specifically that weekly expirations exist.

2. **High Implied Volatility Events (current)**  
   - Look for biotech/pharma **FDA decisions**, **major litigation outcomes**, **regulatory investigations**, **M&A rumors**, or **activist investor campaigns**.  
   - For each: describe the **specific catalyst** and **expected timeline**.

3. **Technical / Momentum Signals**  
   - Stocks breaking **52-week highs or lows** this week.  
   - Stocks with **>30% move in the past 3 months**.  
   - Any **support/resistance breaks** highlighted in financial media.

4. **Unusual Options Flow**  
   - Verified unusual options activity (volume >3× normal).  
   - Large sweep orders from sources like FlowAlgo, Unusual Whales, etc.  
   - Include **source** and **report date**.

5. **Sector Rotation Candidates**  
   - ETFs or stocks mentioned in **institutional sector-rotation reports**.  
   - Companies recently added to **S&P 500** or **Nasdaq 100**.  
   - Recent **upgrades/downgrades** by major banks that triggered volatility.

6. **Liquidity & Eligibility Checks**  
   - Every ticker must have **weekly options**.  
   - Must not be under $5.  
   - No pending **delisting** or **bankruptcy**.

### Output Format:
```python
# Monthly refresh script – Generated YYYY-MM-DD
# Search conducted for events from YYYY-MM-DD to YYYY-MM-DD

OPTIMAL_45 = [
    # Tier 1: Always liquid (15) – Core positions, never remove
    "SPY", "QQQ", "IWM", "AAPL", "MSFT", "NVDA", "AMZN", "META", 
    "GOOGL", "TSLA", "AMD", "NFLX", "JPM", "BAC", "XOM",
    
    # Tier 2: High IV reliables (15) – Replace bottom 3 monthly
    ...
    
    # Tier 3: Sector anchors (15) – Replace on M&A or delisting
    ...
]

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
