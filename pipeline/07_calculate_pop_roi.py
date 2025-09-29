"""
Calculate PoP and ROI: Fixed probability calculation
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
        print("❌ spreads.json not found")
        sys.exit(1)

def calculate_pop_from_delta(delta, spread_type):
    """
    Calculate probability of profit from delta
    For credit spreads, PoP = probability of expiring OTM
    """
    if spread_type == "Bear Call":
        # For calls, delta is already the ITM probability
        # So PoP = 1 - delta
        pop = (1 - delta) * 100
    else:  # Bull Put
        # For puts, delta is negative of ITM probability
        # So PoP = 1 - abs(delta)
        pop = (1 - abs(delta)) * 100
    
    return pop

def calculate_all_pops():
    """Calculate PoP for all spreads"""
    print("="*60)
    print("STEP 7: Calculate PoP and ROI (FIXED)")
    print("="*60)
    print("\n📊 Calculating PoP from delta...")
    
    spreads = load_spreads()
    
    # Process ALL spreads - ensure they all have PoP and score
    for spread in spreads:
        current_pop = spread.get("pop", 0)
        delta = spread["short_delta"]
        
        # If PoP is already reasonable (50-85%), keep it
        if 50 <= current_pop <= 85:
            # Still need to calculate score
            spread["score"] = round((spread["roi"] * current_pop) / 100, 1)
            continue
        
        # Otherwise recalculate from delta
        new_pop = calculate_pop_from_delta(delta, spread["type"])
        spread["pop"] = round(new_pop, 1)
        
        # Calculate score (ROI × PoP / 100)
        spread["score"] = round((spread["roi"] * spread["pop"]) / 100, 1)
    
    # Sort by score
    spreads.sort(key=lambda x: x.get("score", 0), reverse=True)
    
    # Save analyzed spreads with correct structure
    output = {
        "timestamp": datetime.now().isoformat(),
        "total_analyzed": len(spreads),
        "analyzed_spreads": spreads  # Note: using analyzed_spreads not spreads
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
    
    # Show top spreads with REALISTIC probabilities
    print(f"\n🏆 Top 5 by Score (ROI × PoP):")
    for spread in spreads[:5]:
        print(f"   {spread['ticker']} {spread['type']}: Score={spread['score']}, ROI={spread['roi']}%, PoP={spread['pop']}%")
    
    # Calculate average PoP
    avg_pop = sum(s["pop"] for s in spreads) / len(spreads) if spreads else 0
    output["avg_pop"] = round(avg_pop, 1)
    
    # Re-save with avg_pop
    with open("data/analyzed_spreads.json", "w") as f:
        json.dump(output, f, indent=2)
    
    print(f"\n📈 Average PoP: {avg_pop:.1f}%")
    print("\n✅ Step 7 complete: analyzed_spreads.json created")

if __name__ == "__main__":
    calculate_all_pops()
