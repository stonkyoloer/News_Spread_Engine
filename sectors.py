# sectors.py - Auto-Allocating Sector Configuration
"""
PASTE YOUR PROMPT OUTPUT HERE - Replace the OPTIMAL_45 lists below
"""
import time
from pathlib import Path
import json

# =============================================================================
# PASTE PROMPT OUTPUT HERE - Replace these placeholder lists
# =============================================================================

# Monthly refresh script – Generated 2025-08-27
# Research period: 2025-07-28 to 2025-08-27

# MISSING DEFINITION - ADD THIS:
OPTIMAL_45_GPT = [
    # Tier 1: Always liquid (15) – Core positions, never remove
    "SPY", "QQQ", "IWM", "AAPL", "MSFT", "NVDA", "AMZN", "META",
    "GOOGL", "TSLA", "AMD", "NFLX", "JPM", "BAC", "XOM",

    # Tier 2: Recent earnings/event driven (15) – Monthly rotation based on catalysts
    "WMT", "TGT", "HD", "LOW", "MCD", "BKNG",
    "SNOW", "DELL", "PLTR",
    "DIS", "WBD", "VZ",
    "PFE", "MRK", "COP",

    # Tier 3: Sector leaders (15) – Stable positions, change only on major events
    "COST", "PG", "PEP",
    "UNH", "LLY",
    "V", "MA", "BRK.B",
    "AVGO", "ORCL", "ASML",
    "LMT", "HON", "UNP", "NEE",
]

# MISSING DEFINITION - ADD THIS:
OPTIMAL_45_GROK = [
    # Tier 1: Always liquid (15) – Core positions, never remove
    "SPY", "QQQ", "IWM", "AAPL", "MSFT", "NVDA", "AMZN", "META",
    "GOOGL", "TSLA", "AMD", "NFLX", "JPM", "BAC", "XOM",
   
    # Tier 2: Recent earnings/event driven (15) – Monthly rotation based on catalysts
    "MDB", "OKTA", "AMAT", "REGN", "KSS", "NTAP", "VEEV", "APH", "VRNT", "IBKR", "SQ", "NEM", "UNH", "TGT", "CRWD",
   
    # Tier 3: Sector leaders (15) – Stable positions, change only on major events
    "LLY", "JNJ", "PG", "KO", "WMT", "CVX", "CAT", "HON", "GE", "LIN", "DOW", "DUK", "SO", "PLD", "VZ"
]

# This was the existing OPTIMAL_45 - rename it to avoid confusion
OPTIMAL_45_LEGACY = [
    # Tier 1: Always liquid (15) – Core positions, never remove
    "SPY", "QQQ", "IWM", "AAPL", "MSFT", "NVDA", "AMZN", "META",
    "GOOGL", "TSLA", "AMD", "NFLX", "JPM", "BAC", "XOM",

    # Tier 2: Recent earnings/event driven (15) – Monthly rotation based on catalysts
    "WMT", "TGT", "HD", "LOW", "MCD", "BKNG",
    "SNOW", "DELL", "PLTR",
    "DIS", "WBD", "VZ",
    "PFE", "MRK", "COP",

    # Tier 3: Sector leaders (15) – Stable positions, change only on major events
    "COST", "PG", "PEP",
    "UNH", "LLY",
    "V", "MA", "BRK.B",
    "AVGO", "ORCL", "ASML",
    "LMT", "HON", "UNP", "NEE",
]

# AUTOMATIC SECTOR MAPPING - All new tickers with verified classifications
# (Base mapping covers: SPY, QQQ, IWM, AAPL, MSFT, NVDA, AMZN, META, GOOGL, TSLA, AMD, NFLX, JPM, BAC, XOM)
TICKER_SECTOR_MAP_UPDATE = {
    # GPT Tier 2 (event-driven)
    "WMT":  "Consumer Staples",
    "TGT":  "Consumer Discretionary",
    "HD":   "Consumer Discretionary",
    "LOW":  "Consumer Discretionary",
    "MCD":  "Consumer Discretionary",
    "BKNG": "Consumer Discretionary",
    "SNOW": "Information Technology",
    "DELL": "Information Technology",
    "PLTR": "Information Technology",
    "DIS":  "Communication Services",
    "WBD":  "Communication Services",
    "VZ":   "Communication Services",
    "PFE":  "Health Care",
    "MRK":  "Health Care",
    "COP":  "Energy",

    # GPT Tier 3 (sector leaders)
    "COST": "Consumer Staples",
    "PG":   "Consumer Staples",
    "PEP":  "Consumer Staples",
    "UNH":  "Health Care",
    "LLY":  "Health Care",
    "V":    "Financials",
    "MA":   "Financials",
    "BRK.B":"Financials",
    "AVGO": "Information Technology",
    "ORCL": "Information Technology",
    "ASML": "Information Technology",
    "LMT":  "Industrials",
    "HON":  "Industrials",
    "UNP":  "Industrials",
    "NEE":  "Utilities",

    # GROK specific tickers
    "MDB": "Information Technology",
    "OKTA": "Information Technology",
    "AMAT": "Information Technology",
    "REGN": "Health Care",
    "KSS": "Consumer Discretionary",
    "NTAP": "Information Technology",
    "VEEV": "Health Care",
    "APH": "Information Technology",
    "VRNT": "Information Technology",
    "IBKR": "Financials",
    "SQ": "Information Technology",
    "NEM": "Materials",
    "CRWD": "Information Technology",
    "JNJ": "Health Care",
    "KO": "Consumer Staples",
    "CVX": "Energy",
    "CAT": "Industrials",
    "GE": "Industrials",
    "LIN": "Materials",
    "DOW": "Materials",
    "DUK": "Utilities",
    "SO": "Utilities",
    "PLD": "Real Estate",
}

# =============================================================================
# AUTOMATIC SECTOR ALLOCATION (no manual work needed)
# =============================================================================

# Base ticker-to-sector mapping (covers Tier 1 + common tickers)
TICKER_SECTOR_MAP = {
    # ETFs & Indices
    "SPY": "ETFs & Indices", "QQQ": "ETFs & Indices", "IWM": "ETFs & Indices",
    
    # Information Technology (Tier 1)
    "AAPL": "Information Technology", "MSFT": "Information Technology", 
    "NVDA": "Information Technology", "AMD": "Information Technology",
    "GOOGL": "Information Technology", "META": "Information Technology",
    
    # Communication Services
    "NFLX": "Communication Services",
    
    # Consumer Discretionary
    "AMZN": "Consumer Discretionary", "TSLA": "Consumer Discretionary",
    
    # Financials (Tier 1)
    "JPM": "Financials", "BAC": "Financials",
    
    # Energy (Tier 1)  
    "XOM": "Energy",
    
    # Add common mappings for likely tickers
    "V": "Financials", "MA": "Financials", "COIN": "Financials",
    "HOOD": "Financials", "SQ": "Financials", "PYPL": "Financials",
    "LLY": "Health Care", "JNJ": "Health Care", "UNH": "Health Care", 
    "MRNA": "Health Care", "PFE": "Health Care", "ABBV": "Health Care",
    "CVX": "Energy", "COP": "Energy", "OXY": "Energy",
    "WMT": "Consumer Staples", "COST": "Consumer Staples", "PG": "Consumer Staples",
    "HD": "Consumer Discretionary", "LOW": "Consumer Discretionary",
    "CAT": "Industrials", "BA": "Industrials", "GE": "Industrials",
    "NEE": "Utilities", "SO": "Utilities", "DUK": "Utilities",
    "SNAP": "Communication Services", "TTD": "Communication Services",
    "CRWD": "Information Technology", "NET": "Information Technology",
    "PLTR": "Information Technology", "SMCI": "Information Technology",
    "MDB": "Information Technology", "SHOP": "Information Technology",
    "ARM": "Information Technology", "AVGO": "Information Technology",
}

# Merge with AI-generated mappings  
TICKER_SECTOR_MAP.update(TICKER_SECTOR_MAP_UPDATE)

def auto_allocate_sectors(ticker_list, mode_name):
    """Automatically allocate tickers to sectors"""
    sectors = {}
    unassigned = []
    
    # Group tickers by sector
    sector_tickers = {}
    for ticker in ticker_list:
        if ticker == "PLACEHOLDER":
            continue  # Skip placeholder entries
            
        sector = TICKER_SECTOR_MAP.get(ticker)
        if sector:
            if sector not in sector_tickers:
                sector_tickers[sector] = []
            sector_tickers[sector].append(ticker)
        else:
            unassigned.append(ticker)
    
    # Add sector metadata - 11 SPDR sectors only
    sector_metadata = {
        "Information Technology": {"etf": "XLK", "description": "software, semiconductors, hardware, IT services"},
        "Communication Services": {"etf": "XLC", "description": "telecom, media, entertainment, interactive"},
        "Consumer Discretionary": {"etf": "XLY", "description": "retail, restaurants, autos, entertainment"},
        "Consumer Staples": {"etf": "XLP", "description": "food, beverages, household products, tobacco"},
        "Energy": {"etf": "XLE", "description": "oil, gas, renewable energy, equipment"},
        "Financials": {"etf": "XLF", "description": "banks, insurance, capital markets, REITs"},
        "Health Care": {"etf": "XLV", "description": "pharma, biotech, medical equipment, services"},
        "Industrials": {"etf": "XLI", "description": "aerospace, machinery, transportation, defense"},
        "Materials": {"etf": "XLB", "description": "chemicals, metals, mining, construction materials"},
        "Utilities": {"etf": "XLU", "description": "electric, gas, water utilities"},
        "Real Estate": {"etf": "XLRE", "description": "REITs, real estate services"}
    }
    
    # Special handling for ETF indices
    if "SPY" in [t for tickers in sector_tickers.values() for t in tickers] or \
       "QQQ" in [t for tickers in sector_tickers.values() for t in tickers] or \
       "IWM" in [t for tickers in sector_tickers.values() for t in tickers]:
        # Create ETFs & Indices sector for broad market ETFs
        etf_tickers = []
        for sector_name in list(sector_tickers.keys()):
            etf_tickers.extend([t for t in sector_tickers[sector_name] if t in ["SPY", "QQQ", "IWM"]])
            sector_tickers[sector_name] = [t for t in sector_tickers[sector_name] if t not in ["SPY", "QQQ", "IWM"]]
            if not sector_tickers[sector_name]:  # Remove empty sectors
                del sector_tickers[sector_name]
        
        if etf_tickers:
            sector_tickers["ETFs & Indices"] = etf_tickers
            sector_metadata["ETFs & Indices"] = {"etf": "SPY", "description": "broad market ETFs"}
    
    # Build final structure
    for sector_name, tickers in sector_tickers.items():
        meta = sector_metadata.get(sector_name, {"etf": "SPY", "description": "misc"})
        sectors[sector_name] = {
            "etf": meta["etf"],
            "description": meta["description"],
            "tickers": sorted(tickers)
        }
    
    # Handle unassigned tickers - force them into Information Technology as default
    if unassigned:
        if "Information Technology" not in sectors:
            sectors["Information Technology"] = {
                "etf": "XLK", 
                "description": "growth/innovation beta",
                "tickers": []
            }
        sectors["Information Technology"]["tickers"].extend(unassigned)
        sectors["Information Technology"]["tickers"] = sorted(sectors["Information Technology"]["tickers"])
        print(f"WARNING {mode_name}: {len(unassigned)} unassigned tickers added to Information Technology: {unassigned}")
    
    return sectors

# Auto-generate sectors from OPTIMAL_45 lists
SECTORS_GPT = auto_allocate_sectors(OPTIMAL_45_GPT, "GPT")
SECTORS_GROK = auto_allocate_sectors(OPTIMAL_45_GROK, "GROK")

# Performance tracking class
class PerfTimer:
    def __init__(self, name):
        self.name = name
        self.start_time = None
        
    def __enter__(self):
        self.start_time = time.time()
        return self
        
    def __exit__(self, *args):
        elapsed = time.time() - self.start_time
        print(f"⏱️ {self.name}: {elapsed:.2f}s")

# Default portfolio mode
PORTFOLIO_MODE = "gpt"

def get_sectors(mode: str = PORTFOLIO_MODE) -> dict:
    """Get sectors with validation and performance tracking"""
    with PerfTimer(f"Loading {mode.upper()} sectors"):
        mode = (mode or "").lower()
        
        if mode == "gpt":
            sectors = SECTORS_GPT
        elif mode == "grok": 
            sectors = SECTORS_GROK
        elif mode == "merged":
            # Merge GPT and Grok (dedupe by ticker)
            sectors = {}
            all_keys = set(SECTORS_GPT.keys()) | set(SECTORS_GROK.keys())
            for key in all_keys:
                gpt_tickers = SECTORS_GPT.get(key, {}).get("tickers", [])
                grok_tickers = SECTORS_GROK.get(key, {}).get("tickers", [])
                combined_tickers = []
                seen = set()
                for ticker in gpt_tickers + grok_tickers:
                    if ticker not in seen and ticker != "PLACEHOLDER":
                        combined_tickers.append(ticker)
                        seen.add(ticker)
                
                if combined_tickers:  # Only create sector if it has real tickers
                    sectors[key] = {
                        "etf": SECTORS_GPT.get(key, {}).get("etf") or SECTORS_GROK.get(key, {}).get("etf"),
                        "description": SECTORS_GPT.get(key, {}).get("description") or SECTORS_GROK.get(key, {}).get("description"), 
                        "tickers": combined_tickers
                    }
        else:
            raise ValueError(f"Unknown mode '{mode}' (use 'gpt' | 'grok' | 'merged')")
    
    # Validation - filter out placeholder tickers
    for sector_name, sector_data in sectors.items():
        sectors[sector_name]["tickers"] = [t for t in sector_data["tickers"] if t != "PLACEHOLDER"]
    
    total_tickers = sum(len(meta["tickers"]) for meta in sectors.values())
    print(f"📊 Loaded {len(sectors)} sectors, {total_tickers} tickers for {mode.upper()}")
    
    return sectors

# Symbol aliases for data providers
SYMBOL_ALIASES = {
    "BRK.B": ["BRK.B", "BRK-B", "BRK/B"],
    "GOOGL": ["GOOGL", "GOOG"],
    "GOOG": ["GOOG", "GOOGL"],
}

def alias_candidates(sym: str) -> list[str]:
    """Return preferred symbol + any alias candidates"""
    return [sym] + SYMBOL_ALIASES.get(sym, [])

if __name__ == "__main__":
    print("📊 OPTIMAL_45 Auto-Allocation")
    print("=" * 50)
    
    for mode in ["gpt", "grok"]:
        sectors = get_sectors(mode)
        total = sum(len(meta["tickers"]) for meta in sectors.values())
        
        print(f"\n{mode.upper()}: {len(sectors)} sectors, {total} tickers")
        
        # Show allocation
        for sector_name, sector_data in sectors.items():
            tickers = sector_data["tickers"]
            print(f"  {sector_name}: {len(tickers)} tickers")
            if len(tickers) <= 8:
                print(f"    {', '.join(tickers)}")
            else:
                print(f"    {', '.join(tickers[:5])} ... (+{len(tickers)-5} more)")
    
    print("\n✅ Ready for build_universe.py")
    print("Next: python3 build_universe.py")
