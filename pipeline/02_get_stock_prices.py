"""
Get Stock Prices: Real prices from TastyTrade
Enhanced with better error handling and diagnostics
"""
import asyncio
import json
import sys
import os
from datetime import datetime

def check_prerequisites():
    """Check if everything is set up correctly"""
    # Check credentials
    username = os.getenv("TASTY_USERNAME")
    password = os.getenv("TASTY_PASSWORD")
    
    if not username or not password:
        print("❌ Missing TastyTrade credentials")
        print("Set them with:")
        print("export TASTY_USERNAME='your_username'")
        print("export TASTY_PASSWORD='your_password'")
        sys.exit(1)
    
    # Check if data directory exists
    if not os.path.exists("data"):
        print("📁 Creating data directory...")
        os.makedirs("data", exist_ok=True)
    
    # Try to import stocks
    try:
        sys.path.insert(0, 'data')
        from stocks import STOCKS
        return STOCKS, username, password
    except ImportError:
        print("❌ data/stocks.py not found - run step 1 first")
        sys.exit(1)

async def get_real_prices():
    """Get real stock prices with better error handling"""
    print("💰 Getting real stock prices from TastyTrade...")
    
    STOCKS, username, password = check_prerequisites()
    
    # Try imports
    try:
        from tastytrade import Session, DXLinkStreamer
        from tastytrade.dxfeed import Quote
    except ImportError as e:
        print(f"❌ TastyTrade import error: {e}")
        print("Install with: pip install tastytrade")
        sys.exit(1)
    
    prices = {}
    failed = []
    
    try:
        # Create session
        print("📡 Connecting to TastyTrade...")
        sess = Session(username, password)
        print("✅ Connected successfully")
        
        async with DXLinkStreamer(sess) as streamer:
            # Subscribe to all stocks
            print(f"📡 Subscribing to {len(STOCKS)} stocks...")
            await streamer.subscribe(Quote, STOCKS)
            print(f"✅ Subscribed successfully")
            
            # Collect for 15 seconds (longer timeout)
            start_time = asyncio.get_event_loop().time()
            collected = set()
            
            while asyncio.get_event_loop().time() - start_time < 15:
                try:
                    quote = await asyncio.wait_for(streamer.get_event(Quote), timeout=0.5)
                    
                    if quote and quote.event_symbol in STOCKS:
                        ticker = quote.event_symbol
                        bid = float(quote.bid_price or 0)
                        ask = float(quote.ask_price or 0)
                        
                        if bid > 0 and ask > 0 and ticker not in collected:
                            mid = (bid + ask) / 2
                            prices[ticker] = {
                                "ticker": ticker,
                                "bid": round(bid, 2),
                                "ask": round(ask, 2),
                                "mid": round(mid, 2),
                                "spread": round(ask - bid, 2),
                                "timestamp": datetime.now().isoformat()
                            }
                            collected.add(ticker)
                            print(f"   ✅ {ticker}: ${mid:.2f} (bid: ${bid:.2f}, ask: ${ask:.2f})")
                            
                except asyncio.TimeoutError:
                    continue
            
            await streamer.unsubscribe(Quote, STOCKS)
            print(f"📡 Unsubscribed from quotes")
        
    except Exception as e:
        print(f"❌ TastyTrade connection error: {e}")
        print("This could be:")
        print("1. Wrong credentials")
        print("2. Network issues")
        print("3. TastyTrade API problems")
        sys.exit(1)
    
    # Check what we're missing
    for ticker in STOCKS:
        if ticker not in prices:
            failed.append(ticker)
            print(f"   ❌ {ticker}: No data received")
    
    return prices, failed

def save_prices(prices, failed):
    """Save price data"""
    # Import stocks again to get the original list
    sys.path.insert(0, 'data')
    from stocks import STOCKS
    
    output = {
        "timestamp": datetime.now().isoformat(),
        "requested": len(STOCKS),
        "success": len(prices),
        "failed": len(failed),
        "prices": prices,
        "missing_tickers": failed
    }
    
    with open("data/stock_prices.json", "w") as f:
        json.dump(output, f, indent=2)
    
    print(f"\n📊 Results:")
    print(f"   Success: {len(prices)}/{len(STOCKS)} ({len(prices)/len(STOCKS)*100:.1f}%)")
    print(f"   Failed: {len(failed)}")
    
    if len(prices) == 0:
        print("❌ FATAL: No prices collected")
        print("Check your TastyTrade credentials and network connection")
        sys.exit(1)
    elif len(prices) < len(STOCKS) * 0.5:
        print("⚠️ WARNING: Less than 50% success rate")
        print("Pipeline will continue but may have limited results")

def main():
    """Main execution"""
    print("="*60)
    print("STEP 2: Get Real Stock Prices (ENHANCED)")
    print("="*60)
    
    # Get prices
    prices, failed = asyncio.run(get_real_prices())
    
    # Save results
    save_prices(prices, failed)
    
    print("✅ Step 2 complete: stock_prices.json created")

if __name__ == "__main__":
    main()
