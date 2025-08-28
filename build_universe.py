# build_universe.py - Complete Universe Builder
"""
FIXED - Processes ALL tickers for complete data collection.
Removed early exit optimization to ensure 100% ticker coverage.
"""
import json
import time
from datetime import datetime
from pathlib import Path
from tastytrade import Session
from tastytrade.instruments import get_option_chain
from config import USERNAME, PASSWORD
from sectors import get_sectors, alias_candidates, PORTFOLIO_MODE, PerfTimer

BUILD_MODES = ["gpt", "grok"]

def validate_chain_complete(sess, sym, timeout=5):
    """Complete chain validation - processes all aliases"""
    start_time = time.time()
    
    for alias in alias_candidates(sym):
        if time.time() - start_time > timeout:
            break
            
        try:
            chain = get_option_chain(sess, alias)
            if chain and len(chain) > 0:
                print(f"  ✅ {sym} -> {alias}")
                return alias
        except Exception as e:
            print(f"  ❌ {sym} -> {alias} ({str(e)[:30]})")
            continue
    
    print(f"  ⚠️ {sym} -> NO CHAIN")
    return None

def build_universe_complete(sess, mode):
    """Build universe with complete validation - NO EARLY EXIT"""
    print(f"\n🔨 Building {mode.upper()} universe...")
    
    with PerfTimer(f"{mode.upper()} universe build"):
        sectors = get_sectors(mode)
        validated_tickers = []
        failed_tickers = []
        
        # Get all tickers
        all_tickers = []
        ticker_to_sector = {}
        for sector, meta in sectors.items():
            for ticker in meta["tickers"]:
                all_tickers.append(ticker)
                ticker_to_sector[ticker] = sector
        
        print(f"📋 Validating ALL {len(all_tickers)} tickers...")
        
        # Process EVERY ticker - no early exit
        for i, ticker in enumerate(all_tickers, 1):
            print(f"[{i}/{len(all_tickers)}] {ticker}:")
            
            validated_alias = validate_chain_complete(sess, ticker)
            
            record = {
                "ticker": validated_alias or ticker,
                "requested": ticker,
                "sector": ticker_to_sector[ticker],
                "status": "ok" if validated_alias else "no_chain"
            }
            
            if validated_alias:
                validated_tickers.append(record)
            else:
                failed_tickers.append(record)
            
            # Show progress every 10 tickers
            if i % 10 == 0:
                success_rate = len(validated_tickers) / i * 100
                print(f"  📊 Progress: {i}/{len(all_tickers)} ({success_rate:.1f}% success)")
    
    all_results = validated_tickers + failed_tickers
    
    print(f"📊 COMPLETE Results: {len(validated_tickers)} OK, {len(failed_tickers)} failed")
    if failed_tickers:
        failed_symbols = [f["requested"] for f in failed_tickers]
        print(f"❌ Failed: {failed_symbols}")
    
    return all_results

def main():
    """Main universe builder - COMPLETE DATA COLLECTION"""
    start_time = time.time()
    print("🚀 Complete Universe Builder - NO EARLY EXIT")
    print(f"📅 Processing ALL tickers for complete data | Mode: {PORTFOLIO_MODE}")
    
    sess = Session(USERNAME, PASSWORD)
    
    for mode in BUILD_MODES:
        results = build_universe_complete(sess, mode)
        
        # Save results
        filename = f"universe_{mode}.json"
        with open(filename, "w") as f:
            json.dump(results, f, indent=2)
        
        print(f"💾 Saved: {filename}")
    
    # Set active universe
    active_file = f"universe_{PORTFOLIO_MODE}.json"
    if Path(active_file).exists():
        with open(active_file, "r") as f:
            active_data = f.read()
        with open("universe_active.json", "w") as f:
            f.write(active_data)
        print(f"🔗 Active: universe_active.json -> {PORTFOLIO_MODE}")
    
    total_time = time.time() - start_time
    print(f"\n⏱️ Total time: {total_time:.1f}s")
    print(f"🎯 Next: python spot.py")

if __name__ == "__main__":
    main()
