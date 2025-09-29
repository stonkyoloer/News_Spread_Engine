"""
FILTER 3: IV Check (Get Current IV)
402 stocks → ~300 stocks
Stream Greeks for IV data
"""
import json
import asyncio
import sys
import os
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import USERNAME, PASSWORD

from tastytrade import Session, DXLinkStreamer
from tastytrade.dxfeed import Greeks

def load_filter2_results():
    """Load Filter 2 results"""
    with open("data/filter2_results.json", "r") as f:
        data = json.load(f)
    return data["passed_stocks"]

async def get_stock_iv():
    """Get IV for each stock"""
    print("="*60)
    print("FILTER 3: IV Data Collection")
    print("="*60)
    
    stocks = load_filter2_results()
    print(f"Input: {len(stocks)} stocks from Filter 2")
    print("Criteria: Get current IV, filter <15% or >80%\n")
    
    sess = Session(USERNAME, PASSWORD)
    passed = []
    failed = []
    
    async with DXLinkStreamer(sess) as streamer:
        # Process in batches of 20 for Greeks
        BATCH_SIZE = 20
        
        for i in range(0, len(stocks), BATCH_SIZE):
            batch = stocks[i:i+BATCH_SIZE]
            batch_num = i//BATCH_SIZE + 1
            print(f"Batch {batch_num}: Processing {len(batch)} stocks...")
            
            # Get ATM option symbols from chains
            symbols_to_check = []
            ticker_map = {}
            
            for stock_data in batch:
                ticker = stock_data['ticker']
                # Create ATM symbol approximation
                # Format: .TICKER241025C100 (example)
                exp_date = stock_data['best_expiration']['date'].replace('-', '')[2:8]
                strike = int(stock_data['mid'])
                symbol = f".{ticker}{exp_date}C{strike}"
                symbols_to_check.append(symbol)
                ticker_map[symbol] = stock_data
            
            if not symbols_to_check:
                continue
            
            await streamer.subscribe(Greeks, symbols_to_check)
            
            ivs = {}
            start_time = asyncio.get_event_loop().time()
            
            # Collect for 3 seconds per batch
            while asyncio.get_event_loop().time() - start_time < 3:
                try:
                    greek = await asyncio.wait_for(streamer.get_event(Greeks), timeout=0.3)
                    
                    if greek and greek.event_symbol in symbols_to_check:
                        iv = float(greek.volatility or 0)
                        if iv > 0:
                            stock_data = ticker_map[greek.event_symbol]
                            ticker = stock_data['ticker']
                            ivs[ticker] = iv
                except asyncio.TimeoutError:
                    continue
            
            await streamer.unsubscribe(Greeks, symbols_to_check)
            
            # Process results
            for stock_data in batch:
                ticker = stock_data['ticker']
                
                if ticker in ivs:
                    iv = ivs[ticker]
                    iv_pct = iv * 100
                    
                    # Filter criteria
                    if 15 <= iv_pct <= 80:
                        passed.append({
                            **stock_data,
                            'iv': round(iv, 4),
                            'iv_pct': round(iv_pct, 1)
                        })
                        print(f"   ✅ {ticker}: IV={iv_pct:.1f}%")
                    else:
                        failed.append({'ticker': ticker, 'reason': f'IV {iv_pct:.1f}% out of range'})
                else:
                    # No IV data - use default
                    passed.append({
                        **stock_data,
                        'iv': 0.25,  # Default 25%
                        'iv_pct': 25.0
                    })
    
    return passed, failed

def save_filter3_results(passed, failed):
    """Save results"""
    output = {
        'timestamp': datetime.now().isoformat(),
        'filter': 'IV Data',
        'input_count': len(passed) + len(failed),
        'passed_count': len(passed),
        'failed_count': len(failed),
        'passed_stocks': passed,
        'failed_reasons': failed[:20]
    }
    
    with open('data/filter3_results.json', 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"\n{'='*60}")
    print(f"FILTER 3 RESULTS:")
    print(f"   Input: {len(passed) + len(failed)} stocks")
    print(f"   Passed: {len(passed)} stocks")
    print(f"   Failed: {len(failed)} stocks")
    
    # Show IV distribution
    if passed:
        ivs = [s['iv_pct'] for s in passed if 'iv_pct' in s]
        if ivs:
            print(f"\nIV Distribution:")
            print(f"   Min: {min(ivs):.1f}%")
            print(f"   Max: {max(ivs):.1f}%")
            print(f"   Avg: {sum(ivs)/len(ivs):.1f}%")

async def main():
    passed, failed = await get_stock_iv()
    save_filter3_results(passed, failed)
    print(f"\n✅ Filter 3 complete. Results in filter3_results.json")

if __name__ == "__main__":
    asyncio.run(main())
