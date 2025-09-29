"""
Build Report Table: Exactly 9 unique tickers
"""
import json
import sys
import os
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def load_ranked_spreads():
    try:
        with open("data/ranked_spreads.json", "r") as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        print("❌ ranked_spreads.json not found")
        sys.exit(1)

def load_edge_reasons():
    try:
        from data.stocks import EDGE_REASON
        return EDGE_REASON
    except ImportError:
        return {}

def build_report_table():
    """Build report with exactly 9 unique tickers"""
    print("📋 Building report (9 unique tickers)...")
    
    data = load_ranked_spreads()
    edge_reasons = load_edge_reasons()
    
    # Get all ranked spreads (already unique)
    spreads = data["ranked_spreads"][:9]
    
    report_entries = []
    
    sector_map = {
        "AAPL": "XLK", "MSFT": "XLK", "GOOGL": "XLK",
        "JPM": "XLF", "GS": "XLF",
        "UNH": "XLV", "CVS": "XLV",
        "AMZN": "XLY", "TSLA": "XLY",
        "PG": "XLP", "KO": "XLP",
        "XOM": "XLE", "CVX": "XLE",
        "BA": "XLI", "CAT": "XLI",
        "LIN": "XLB", "FCX": "XLB",
        "PLD": "XLRE", "AMT": "XLRE",
        "NEE": "XLU", "DUK": "XLU",
        "META": "XLC"
    }
    
    for spread in spreads:
        ticker = spread["ticker"]
        sector = sector_map.get(ticker, "Unknown")
        
        entry = {
            "rank": spread["rank"],
            "sector": sector,
            "ticker": ticker,
            "type": spread["type"],
            "legs": f"${spread['short_strike']:.0f}/${spread['long_strike']:.0f}",
            "exp_date": spread["expiration"]["date"],
            "dte": spread["expiration"]["dte"],
            "roi": f"{spread['roi']}%",
            "pop": f"{spread['pop']}%",
            "net_credit": f"${spread['net_credit']:.2f}",
            "max_loss": f"${spread['max_loss']:.2f}",
            "decision": spread["decision"],
            "edge_reason": edge_reasons.get(ticker, ""),
            "iv": spread["short_iv"],
            "delta": spread["short_delta"],
            "score": spread["rank_score"]
        }
        report_entries.append(entry)
    
    return report_entries

def save_report_table(entries):
    output = {
        "timestamp": datetime.now().isoformat(),
        "total_entries": len(entries),
        "report_table": entries
    }
    
    with open("data/report_table.json", "w") as f:
        json.dump(output, f, indent=2)
    
    print(f"\n📊 Report Table: {len(entries)} unique tickers")
    
    print(f"\n📋 Preview:")
    print(f"{'Rank':<5} {'Ticker':<8} {'Type':<10} {'ROI':<8} {'PoP':<8}")
    print("-" * 45)
    
    for entry in entries:
        print(f"{entry['rank']:<5} {entry['ticker']:<8} {entry['type']:<10} {entry['roi']:<8} {entry['pop']:<8}")

def main():
    print("="*60)
    print("STEP 9: Build Report (9 Unique Tickers)")
    print("="*60)
    
    entries = build_report_table()
    save_report_table(entries)
    
    print("✅ Step 9 complete: 9 unique tickers")

if __name__ == "__main__":
    main()
