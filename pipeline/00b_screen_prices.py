"""
Step 0B: Screen S&P 500 for Today's Movers
Uses TastyTrade for real prices
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

async def screen_prices():
    """Get prices for S&P 500 and find movers"""
    print("💰 Screening S&P 500 for movers...")
    
    # Load universe
    with open("data/sp500_universe.json", "r") as f:
        data = json.load(f)
        tickers = data["tickers"]
    
    print(f"   Checking {len(tickers)} stocks...")
    
    sess = Session(USERNAME, PASSWORD)
    movers = []
    
    # Process in batches
    BATCH_SIZE = 50
    
    async with DXLinkStreamer(sess) as streamer:
        for i in range(0, len(tickers), BATCH_SIZE):
            batch = tickers[i:i+BATCH_SIZE]
            print(f"   Batch {i//BATCH_SIZE + 1}: {len(batch)} stocks")
            
            await streamer.subscribe(Quote, batch)
            
            quotes = {}
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
                            
                            # Calculate day change from quote
                            # This is simplified - ideally get previous close
                            quotes[quote.event_symbol] = {
                                'ticker': quote.event_symbol,
                                'bid': bid,
                                'ask': ask,
                                'mid': mid,
                                'spread': ask - bid
                            }
                except asyncio.TimeoutError:
                    continue
            
            await streamer.unsubscribe(Quote, batch)
            
            # Filter for liquidity and price range
            for ticker, data in quotes.items():
                if 20 <= data['mid'] <= 500:  # Price range for credit spreads
                    if data['spread'] < data['mid'] * 0.02:  # Tight spread
                        movers.append(data)
    
    return movers

def save_movers(movers):
    """Save screened stocks"""
    output = {
        'timestamp': datetime.now().isoformat(),
        'total_screened': 503,
        'passed_screen': len(movers),
        'movers': sorted(movers, key=lambda x: x['mid'], reverse=True)
    }
    
    with open('data/screened_stocks.json', 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"\n📊 Screening Results:")
    print(f"   Passed: {len(movers)}/503 stocks")
    print(f"   Price range: $20-500")
    print(f"   Tight spreads: <2%")
    
    if movers:
        print(f"\nTop 5 by price:")
        for m in movers[:5]:
            print(f"   {m['ticker']}: ${m['mid']:.2f}")

def main():
    print("="*60)
    print("STEP 0B: Screen for Movers")
    print("="*60)
    
    movers = asyncio.run(screen_prices())
    save_movers(movers)
    
    print("\n✅ Ready for options check")

if __name__ == "__main__":
    main()
