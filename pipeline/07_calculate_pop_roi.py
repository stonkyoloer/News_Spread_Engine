"""
Calculate PoP and ROI: Real probability using Black-Scholes
No fake numbers - uses real IV from Greeks
"""
import json
import sys
import math
from datetime import datetime
from scipy.stats import norm

def load_spreads():
    """Load spreads data"""
    try:
        with open("data/spreads.json", "r") as f:
            data = json.load(f)
        return data["spreads"]
    except FileNotFoundError:
        print("❌ spreads.json not found - run calculate_spreads.py first")
        sys.exit(1)

def black_scholes_pop(stock_price, strike, net_credit, dte, iv, spread_type):
    """Calculate real PoP using Black-Scholes"""
    if dte <= 0 or iv <= 0:
        return 0
    
    if spread_type == "Bear Call":
        breakeven = strike + net_credit
        d2_sign = -1
    else:  # Bull Put
        breakeven = strike - net_credit
        d2_sign = 1
    
    T = dte / 365.0
    r = 0.05  # Risk-free rate
    
    # Calculate d2
    iv = iv/100
    d1 = (math.log(stock_price / breakeven) + (r + 0.5 * iv**2) * T) / (iv * math.sqrt(T))
    d2 = d1 - iv * math.sqrt(T)
    
    return norm.cdf(d2_sign * d2) * 100

def calculate_all_pops():
    """Calculate PoP for all spreads"""
    print("📊 Calculating real PoP using Black-Scholes...")
    
    spreads = load_spreads()
    analyzed_spreads = []
    
    for spread in spreads:
        # Calculate PoP
        pop = black_scholes_pop(
            spread["stock_price"],
            spread["short_strike"],
            spread["net_credit"],
            spread["expiration"]["dte"],
            spread["short_iv"],
            spread["type"]
        )
        
        # Add PoP to spread
        spread["pop"] = round(pop, 1)
        
        # Calculate risk-adjusted score
        if spread["roi"] > 0 and pop > 0:
            spread["score"] = round((spread["roi"] * pop) / 100, 1)
        else:
            spread["score"] = 0
        
        analyzed_spreads.append(spread)
    
    # Sort by score
    analyzed_spreads.sort(key=lambda x: x["score"], reverse=True)
    
    return analyzed_spreads

def save_analyzed_spreads(spreads):
    """Save spreads with PoP and scores"""
    output = {
        "timestamp": datetime.now().isoformat(),
        "total_spreads": len(spreads),
        "analyzed_spreads": spreads
    }
    
    with open("data/analyzed_spreads.json", "w") as f:
        json.dump(output, f, indent=2)
    
    print(f"\n📊 Results:")
    print(f"   Analyzed: {len(spreads)} spreads")
    
    # Show PoP distribution
    high_pop = len([s for s in spreads if s["pop"] >= 70])
    mid_pop = len([s for s in spreads if 50 <= s["pop"] < 70])
    low_pop = len([s for s in spreads if s["pop"] < 50])
    
    print(f"\n🎲 PoP Distribution:")
    print(f"   High (≥70%): {high_pop}")
    print(f"   Mid (50-70%): {mid_pop}")
    print(f"   Low (<50%): {low_pop}")
    
    # Show top spreads
    print(f"\n🏆 Top 5 by Score (ROI × PoP):")
    for spread in spreads[:5]:
        print(f"   {spread['ticker']} {spread['type']}: Score={spread['score']}, ROI={spread['roi']}%, PoP={spread['pop']}%")

def main():
    """Main execution"""
    print("="*60)
    print("STEP 7: Calculate PoP and ROI")
    print("="*60)
    
    # Calculate PoPs
    analyzed_spreads = calculate_all_pops()
    
    # Save results
    save_analyzed_spreads(analyzed_spreads)
    
    print("✅ Step 7 complete: analyzed_spreads.json created")

if __name__ == "__main__":
    main()
