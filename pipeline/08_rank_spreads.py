"""
Rank Spreads: One spread per ticker only
"""
import json
import sys
from datetime import datetime

def load_analyzed_spreads():
    """Load analyzed spreads"""
    try:
        with open("data/analyzed_spreads.json", "r") as f:
            data = json.load(f)
        return data["analyzed_spreads"]
    except FileNotFoundError:
        print("❌ analyzed_spreads.json not found")
        sys.exit(1)

def rank_spreads():
    """Rank spreads - keep only best per ticker"""
    print("🏆 Ranking spreads (1 per ticker)...")
    
    spreads = load_analyzed_spreads()
    
    # Add ranking factors
    for spread in spreads:
        score_rank = spread["score"]
        pop_rank = spread["pop"] / 100
        roi_rank = min(spread["roi"] / 100, 1.0)
        distance = abs(spread["short_strike"] - spread["stock_price"]) / spread["stock_price"]
        distance_rank = min(distance * 10, 1.0)
        
        spread["rank_score"] = round(
            score_rank * 0.4 +
            pop_rank * 0.3 +
            roi_rank * 0.2 +
            distance_rank * 0.1,
            2
        )
        
        if spread["pop"] >= 70 and spread["roi"] >= 20:
            spread["decision"] = "ENTER"
        elif spread["pop"] >= 60 and spread["roi"] >= 30:
            spread["decision"] = "WATCH"
        else:
            spread["decision"] = "SKIP"
    
    # Sort by score
    spreads.sort(key=lambda x: x["rank_score"], reverse=True)
    
    # KEEP ONLY BEST PER TICKER
    seen_tickers = set()
    unique_spreads = []
    
    for spread in spreads:
        if spread["ticker"] not in seen_tickers:
            seen_tickers.add(spread["ticker"])
            unique_spreads.append(spread)
    
    # Re-rank
    for i, spread in enumerate(unique_spreads):
        spread["rank"] = i + 1
    
    return unique_spreads

def save_ranked_spreads(spreads):
    """Save ranked spreads"""
    enter = [s for s in spreads if s["decision"] == "ENTER"]
    watch = [s for s in spreads if s["decision"] == "WATCH"]
    skip = [s for s in spreads if s["decision"] == "SKIP"]
    
    output = {
        "timestamp": datetime.now().isoformat(),
        "summary": {
            "total": len(spreads),
            "enter": len(enter),
            "watch": len(watch),
            "skip": len(skip)
        },
        "ranked_spreads": spreads,
        "enter_trades": enter[:10],
        "watch_list": watch[:10]
    }
    
    with open("data/ranked_spreads.json", "w") as f:
        json.dump(output, f, indent=2)
    
    print(f"\n📊 Unique Tickers: {len(spreads)}")
    print(f"   🟢 ENTER: {len(enter)}")
    print(f"   🟡 WATCH: {len(watch)}")
    print(f"   🔴 SKIP: {len(skip)}")
    
    print(f"\n🎯 Top 9 UNIQUE Tickers:")
    for spread in spreads[:9]:
        print(f"   #{spread['rank']}: {spread['ticker']} {spread['type']}")
        print(f"        ROI: {spread['roi']}% | PoP: {spread['pop']}%")

def main():
    print("="*60)
    print("STEP 8: Rank Spreads (Unique Tickers)")
    print("="*60)
    
    ranked_spreads = rank_spreads()
    save_ranked_spreads(ranked_spreads)
    
    print("✅ Step 8 complete: unique tickers only")

if __name__ == "__main__":
    main()
