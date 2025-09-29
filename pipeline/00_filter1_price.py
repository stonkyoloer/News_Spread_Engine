"""
FILTER 1: Price & Liquidity Check
500 stocks → ~250 stocks
Real TastyTrade quotes only
"""
import json
import asyncio
import sys
import os
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import USERNAME, PASSWORD

from tastytrade import Session, DXLinkStreamer
from tastytrade.dxfeed import Quote

async def filter_price_liquidity():
    """Filter 1: $30-400, spread <1%"""
    print("="*60)
    print("FILTER 1: Price & Liquidity")
    print("="*60)
    
    # Load S&P 500
    with open("data/sp500_universe.json", "r") as f:
        tickers = json.load(f)["tickers"]
    
    print(f"Input: {len(tickers)} stocks")
    
    sess = Session(USERNAME, PASSWORD)
    passed = []
    failed = []
    
    async with DXLinkStreamer(sess) as streamer:
        # Process in batches of 50
        for i in range(0, len(tickers), 50):
            batch = tickers[i:i+50]
            print(f"\nBatch {i//50 + 1}: Processing {len(batch)} stocks...")
            
            await streamer.subscribe(Quote, batch)
            
            batch_quotes = {}
            start_time = asyncio.get_event_loop().time()
            
            # Collect for 5 seconds per batch
            while asyncio.get_event_loop().time() - start_time < 5:
                try:
                    quote = await asyncio.wait_for(streamer.get_event(Quote), timeout=0.5)
                    
                    if quote and quote.event_symbol in batch:
                        bid = float(quote.bid_price or 0)
                        ask = float(quote.ask_price or 0)
                        
                        if bid > 0 and ask > 0:
                            mid = (bid + ask) / 2
                            spread = ask - bid
                            spread_pct = (spread / mid) * 100
                            
                            batch_quotes[quote.event_symbol] = {
                                'ticker': quote.event_symbol,
                                'bid': round(bid, 2),
                                'ask': round(ask, 2),
                                'mid': round(mid, 2),
                                'spread': round(spread, 3),
                                'spread_pct': round(spread_pct, 2)
                            }
                except asyncio.TimeoutError:
                    continue
            
            await streamer.unsubscribe(Quote, batch)
            
            # Apply filter criteria
            for ticker, data in batch_quotes.items():
                if 30 <= data['mid'] <= 400 and data['spread_pct'] < 1.0:
                    passed.append(data)
                    print(f"   ✅ {ticker}: ${data['mid']:.2f} (spread {data['spread_pct']:.2f}%)")
                else:
                    reason = ""
                    if data['mid'] < 30:
                        reason = "too cheap"
                    elif data['mid'] > 400:
                        reason = "too expensive"
                    else:
                        reason = f"wide spread {data['spread_pct']:.2f}%"
                    failed.append({'ticker': ticker, 'reason': reason})
    
    return passed, failed

def save_filter1_results(passed, failed):
    """Save results"""
    output = {
        'timestamp': datetime.now().isoformat(),
        'filter': 'Price & Liquidity',
        'input_count': 503,
        'passed_count': len(passed),
        'failed_count': len(failed),
        'passed_stocks': passed,
        'failed_reasons': failed[:20]  # Show first 20 failures
    }
    
    with open('data/filter1_results.json', 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"\n{'='*60}")
    print(f"FILTER 1 RESULTS:")
    print(f"   Input: 503 stocks")
    print(f"   Passed: {len(passed)} stocks")
    print(f"   Failed: {len(failed)} stocks")
    print(f"\n   Criteria:")
    print(f"   - Price: $30-400")
    print(f"   - Spread: <1%")
    
    if passed:
        print(f"\n   Top 5 most liquid:")
        sorted_by_spread = sorted(passed, key=lambda x: x['spread_pct'])
        for stock in sorted_by_spread[:5]:
            print(f"   {stock['ticker']}: ${stock['mid']:.2f} (spread {stock['spread_pct']:.2f}%)")

async def main():
    passed, failed = await filter_price_liquidity()
    save_filter1_results(passed, failed)
    print(f"\n✅ Filter 1 complete. Results in filter1_results.json")

if __name__ == "__main__":
    asyncio.run(main())
