# Credit Spread Screener 

Work in Progress...  

1. Start with 9 sectors and scan for catalysts across earnings, filings, flows, sentiment, ratings, volatility, support/resistance, and relative strength. GPT-5 and Grok select the top 3 tickers per sector, 27 tickers total. 

2. Scripts pulls live market data from the tastytrade server, and uses Black-Scholes to get PoP and ROI. 

3. GPT-5 and Grok link news and events to each spread, producing entry and exit plans.


**Need a tool or automation for your project? Hit me up, and I’ll build it: stuart.alexander.phi@icloud.com**

---

# 🪐 FINANCIAL MARKETS RESEARCH ASSISTANT PROMPT

## ▪️  STEP 1

### ◽️ Define a 45 Ticker Trading Portfolio | Screen for News and Events 


```python
# FINANCIAL MARKETS RESEARCH ASSISTANT PROMPT
# Task: Generate 45-ticker credit spread universe with automatic sector allocation
# Focus: Publicly verifiable information only (SEC filings, earnings reports, company announcements)

# =============================================================================
# RESEARCH CRITERIA - HIGH CONFIDENCE TASKS ONLY
# =============================================================================

RESEARCH_CRITERIA = {
    "recent_earnings_analysis": {
        "timeframe": "past_30_days",
        "focus": [
            "companies_that_reported_earnings_last_30_days",
            "revenue_eps_beats_or_misses_from_earnings_releases", 
            "management_guidance_updates_or_outlook_changes",
            "quarterly_performance_vs_prior_periods"
        ],
        "sources": ["company_earnings_press_releases", "10Q_filings", "investor_presentations"],
        "verification_required": True
    },
    
    "corporate_development_events": {
        "focus": [
            "recent_ma_announcements_spinoffs_major_acquisitions",
            "new_product_launches_or_market_expansions", 
            "executive_leadership_changes_ceo_cfo_transitions",
            "strategic_partnerships_or_major_contract_wins"
        ],
        "sources": ["8K_filings", "company_press_releases", "investor_relations_pages"],
        "verification_required": True
    },
    
    "financial_health_indicators": {
        "focus": [
            "companies_with_strong_balance_sheets_low_debt_equity",
            "consistent_free_cash_flow_generation_past_4_quarters",
            "revenue_growth_trends_from_quarterly_reports",
            "market_capitalization_above_1B_for_liquidity"
        ],
        "sources": ["10K_filings", "10Q_filings", "financial_statements"],
        "verification_required": True
    },
    
    "index_changes_and_upgrades": {
        "focus": [
            "recent_additions_to_sp500_russell_indices_sector_etfs",
            "analyst_upgrades_downgrades_major_investment_banks",
            "credit_rating_changes_moodys_sp_fitch"
        ],
        "sources": ["index_provider_announcements", "analyst_research_summaries"],
        "verification_required": True
    },
    
    "sector_leadership_identification": {
        "focus": [
            "companies_with_dominant_market_positions",
            "high_institutional_ownership_above_70_percent",
            "consistent_dividend_payments_or_buyback_programs", 
            "strong_competitive_moats_from_annual_reports"
        ],
        "sources": ["proxy_statements", "annual_reports", "industry_analysis"],
        "verification_required": True
    }
}

# =============================================================================
# VERIFICATION REQUIREMENTS - CRITICAL CONSTRAINTS
# =============================================================================

VERIFICATION_REQUIREMENTS = {
    "basic_eligibility": {
        "stock_price": "above_20_dollars_per_share",
        "market_cap": "above_1B_for_liquidity", 
        "listing_status": "no_pending_bankruptcy_delisting_major_litigation",
        "exchange": "primary_listing_nyse_or_nasdaq"
    },
    "source_verification": ["exchange_listings", "sec_filings", "court_records"],
    "mandatory_constraints": [
        "base_analysis_only_on_publicly_available_verifiable_sources",
        "if_information_cannot_be_confirmed_state_information_not_available",
        "include_confidence_level_high_medium_low_for_each_selection",
        "cite_specific_sources_for_all_claims_sec_filing_dates_press_releases"
    ],
    "prohibited_claims": [
        "real_time_stock_prices_or_options_chains",
        "intraday_trading_volumes_or_technical_indicators", 
        "proprietary_analyst_price_targets",
        "forward_looking_earnings_beyond_company_guidance",
        "insider_trading_activity_or_institutional_flow_data"
    ]
}

# =============================================================================
# OUTPUT FORMAT - COPY THIS STRUCTURE EXACTLY
# =============================================================================

# Monthly refresh script – Generated [TODAY'S_DATE]
# Research period: [30_DAYS_AGO] to [TODAY'S_DATE]

OPTIMAL_45_GPT = [
    # Tier 1: Always liquid (15) – Core positions, never remove
    "SPY", "QQQ", "IWM", "AAPL", "MSFT", "NVDA", "AMZN", "META", 
    "GOOGL", "TSLA", "AMD", "NFLX", "JPM", "BAC", "XOM",
    
    # Tier 2: Recent earnings/event driven (15) – Monthly rotation based on catalysts
    "REPLACE_WITH_ACTUAL_TICKER", "REPLACE_WITH_ACTUAL_TICKER", "REPLACE_WITH_ACTUAL_TICKER", 
    "REPLACE_WITH_ACTUAL_TICKER", "REPLACE_WITH_ACTUAL_TICKER", "REPLACE_WITH_ACTUAL_TICKER",
    "REPLACE_WITH_ACTUAL_TICKER", "REPLACE_WITH_ACTUAL_TICKER", "REPLACE_WITH_ACTUAL_TICKER", 
    "REPLACE_WITH_ACTUAL_TICKER", "REPLACE_WITH_ACTUAL_TICKER", "REPLACE_WITH_ACTUAL_TICKER",
    "REPLACE_WITH_ACTUAL_TICKER", "REPLACE_WITH_ACTUAL_TICKER", "REPLACE_WITH_ACTUAL_TICKER",
    
    # Tier 3: Sector leaders (15) – Stable positions, change only on major events
    "REPLACE_WITH_ACTUAL_TICKER", "REPLACE_WITH_ACTUAL_TICKER", "REPLACE_WITH_ACTUAL_TICKER",
    "REPLACE_WITH_ACTUAL_TICKER", "REPLACE_WITH_ACTUAL_TICKER", "REPLACE_WITH_ACTUAL_TICKER", 
    "REPLACE_WITH_ACTUAL_TICKER", "REPLACE_WITH_ACTUAL_TICKER", "REPLACE_WITH_ACTUAL_TICKER",
    "REPLACE_WITH_ACTUAL_TICKER", "REPLACE_WITH_ACTUAL_TICKER", "REPLACE_WITH_ACTUAL_TICKER",
    "REPLACE_WITH_ACTUAL_TICKER", "REPLACE_WITH_ACTUAL_TICKER", "REPLACE_WITH_ACTUAL_TICKER"
]

OPTIMAL_45_GROK = [
    # Tier 1: Always liquid (15) – Core positions, never remove
    "SPY", "QQQ", "IWM", "AAPL", "MSFT", "NVDA", "AMZN", "META", 
    "GOOGL", "TSLA", "AMD", "NFLX", "JPM", "BAC", "XOM",
    
    # Tier 2: Recent earnings/event driven (15) – Monthly rotation based on catalysts
    "DIFFERENT_SELECTION_FROM_GPT", "DIFFERENT_SELECTION_FROM_GPT", "DIFFERENT_SELECTION_FROM_GPT",
    "DIFFERENT_SELECTION_FROM_GPT", "DIFFERENT_SELECTION_FROM_GPT", "DIFFERENT_SELECTION_FROM_GPT",
    "DIFFERENT_SELECTION_FROM_GPT", "DIFFERENT_SELECTION_FROM_GPT", "DIFFERENT_SELECTION_FROM_GPT", 
    "DIFFERENT_SELECTION_FROM_GPT", "DIFFERENT_SELECTION_FROM_GPT", "DIFFERENT_SELECTION_FROM_GPT",
    "DIFFERENT_SELECTION_FROM_GPT", "DIFFERENT_SELECTION_FROM_GPT", "DIFFERENT_SELECTION_FROM_GPT",
    
    # Tier 3: Sector leaders (15) – Stable positions, change only on major events  
    "DIFFERENT_SELECTION_FROM_GPT", "DIFFERENT_SELECTION_FROM_GPT", "DIFFERENT_SELECTION_FROM_GPT",
    "DIFFERENT_SELECTION_FROM_GPT", "DIFFERENT_SELECTION_FROM_GPT", "DIFFERENT_SELECTION_FROM_GPT",
    "DIFFERENT_SELECTION_FROM_GPT", "DIFFERENT_SELECTION_FROM_GPT", "DIFFERENT_SELECTION_FROM_GPT", 
    "DIFFERENT_SELECTION_FROM_GPT", "DIFFERENT_SELECTION_FROM_GPT", "DIFFERENT_SELECTION_FROM_GPT",
    "DIFFERENT_SELECTION_FROM_GPT", "DIFFERENT_SELECTION_FROM_GPT", "DIFFERENT_SELECTION_FROM_GPT"
]

# AUTOMATIC SECTOR MAPPING - All new tickers with verified classifications
TICKER_SECTOR_MAP_UPDATE = {
    # Only include NEW tickers not in base mapping (exclude Tier 1)
    # Base mapping covers: SPY, QQQ, IWM, AAPL, MSFT, NVDA, AMZN, META, GOOGL, TSLA, AMD, NFLX, JPM, BAC, XOM
    
    "REPLACE_WITH_ACTUAL_TICKER": "Information Technology",     # Based on GICS sector classification
    "REPLACE_WITH_ACTUAL_TICKER": "Health Care",                # From company 10K business description  
    "REPLACE_WITH_ACTUAL_TICKER": "Consumer Discretionary",     # Primary revenue source analysis
    "REPLACE_WITH_ACTUAL_TICKER": "Financials",                 # SIC code verification
    "REPLACE_WITH_ACTUAL_TICKER": "Energy",                     # Business segment breakdown
    "REPLACE_WITH_ACTUAL_TICKER": "Communication Services",     # Revenue classification
    "REPLACE_WITH_ACTUAL_TICKER": "Industrials",                # Primary business operations
    "REPLACE_WITH_ACTUAL_TICKER": "Materials",                  # Manufacturing/production focus
    "REPLACE_WITH_ACTUAL_TICKER": "Utilities",                  # Regulated utility operations
    "REPLACE_WITH_ACTUAL_TICKER": "Consumer Staples",           # Defensive consumer products
    # Continue for all 30 new tickers with actual symbols and verified sectors
    
    # GICS_SECTOR_CLASSIFICATIONS - Use these exact categories:
    # "Information Technology" - software, semiconductors, hardware, IT services
    # "Health Care" - pharmaceuticals, biotechnology, medical equipment, healthcare services
    # "Financials" - banks, insurance, capital markets, fintech, REITs
    # "Consumer Discretionary" - retail, media, restaurants, automobiles, luxury goods
    # "Consumer Staples" - food products, beverages, household products, tobacco
    # "Energy" - oil_gas, renewable energy, energy equipment_services
    # "Communication Services" - telecommunications, media_entertainment, interactive media
    # "Industrials" - aerospace, machinery, transportation, construction, defense
    # "Materials" - chemicals, metals_mining, construction materials, packaging
    # "Utilities" - electric, gas, water utilities, renewable energy utilities
    # "Real Estate" - equity REITs, real estate management_development
}

# =============================================================================
# RESEARCH DOCUMENTATION REQUIREMENTS
# =============================================================================

RESEARCH_DOCUMENTATION = {
    "tier_2_tier_3_selections_must_include": [
        "ticker_symbol",
        "selection_rationale", # earnings_beat, index_addition, leadership_position, etc
        "source_verification", # 10Q_filed_DATE, press_release_DATE, etc  
        "sector_justification", # primary_revenue_source, GICS_classification, etc
        "confidence_level" # High, Medium, Low
    ],
    "quality_standards": [
        "all_30_new_tickers_verified_for_basic_eligibility", # above_20_dollars, above_1B_market_cap
        "sector_allocation_based_on_GICS_classifications_or_SEC_business_descriptions",
        "research_reasoning_must_cite_specific_verifiable_sources",
        "gpt_and_grok_selections_differ_by_at_least_10_tickers"
    ]
}

# =============================================================================
# EXECUTION INSTRUCTIONS
# =============================================================================

"""
Replace all REPLACE_WITH_ACTUAL_TICKER placeholders with real ticker symbols.
Replace all DIFFERENT_SELECTION_FROM_GPT with tickers different from GPT list.
Include research documentation for each non-Tier-1 selection.
Verify all sources and include confidence levels.
Ensure sector mapping uses official GICS classifications.
"""
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
