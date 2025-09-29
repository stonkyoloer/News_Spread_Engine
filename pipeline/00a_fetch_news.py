"""
Step 0A: Fetch Real-Time News and Market Data
Free data from Yahoo Finance
"""
import json
import yfinance as yf
from datetime import datetime, timedelta
import sys

def get_sp500_tickers():
    """Get top S&P 500 tickers"""
    # Top 30 most liquid for speed
    tickers = [
        "AAPL", "MSFT", "GOOGL", "AMZN", "META",
        "NVDA", "TSLA", "BRK-B", "JPM", "JNJ",
        "V", "UNH", "PG", "HD", "MA",
        "DIS", "BAC", "XOM", "CVX", "ABBV",
        "PFE", "WMT", "KO", "PEP", "AVGO",
        "CSCO", "VZ", "ADBE", "CMCSA", "INTC"
    ]
    return tickers

def fetch_market_data():
    """Get real-time market data"""
    print("📰 Fetching real-time market data...")
    
    tickers = get_sp500_tickers()
    market_data = {}
    
    for ticker in tickers:
        print(f"   Checking {ticker}...")
        try:
            stock = yf.Ticker(ticker)
            
            # Get recent price action
            hist = stock.history(period="5d")
            if not hist.empty:
                current = hist['Close'][-1]
                prev = hist['Close'][-2] if len(hist) > 1 else current
                change = ((current - prev) / prev) * 100
                
                # Get news headlines
                news = stock.news[:3] if hasattr(stock, 'news') else []
                headlines = [n.get('title', '') for n in news]
                
                # Get earnings date
                cal = stock.calendar
                earnings = cal.get('Earnings Date', [None])[0] if cal else None
                
                market_data[ticker] = {
                    'price': round(current, 2),
                    'change_pct': round(change, 2),
                    'headlines': headlines,
                    'earnings_date': str(earnings) if earnings else None
                }
                
        except Exception as e:
            print(f"   ⚠️ {ticker} error: {str(e)[:30]}")
    
    return market_data

def save_market_context(data):
    """Save data for GPT"""
    
    # Find movers
    movers = sorted(data.items(), 
                   key=lambda x: abs(x[1].get('change_pct', 0)), 
                   reverse=True)[:10]
    
    # Build context
    context = {
        'timestamp': datetime.now().isoformat(),
        'market_summary': {
            'top_gainers': [(t, d['change_pct']) for t, d in movers if d.get('change_pct', 0) > 0][:5],
            'top_losers': [(t, d['change_pct']) for t, d in movers if d.get('change_pct', 0) < 0][:5]
        },
        'earnings_today': [(t, d['earnings_date']) for t, d in data.items() 
                          if d.get('earnings_date')],
        'news_mentions': [(t, d['headlines'][0]) for t, d in data.items() 
                         if d.get('headlines')],
        'full_data': data
    }
    
    with open('data/market_context.json', 'w') as f:
        json.dump(context, f, indent=2)
    
    print(f"\n📊 Market Context Summary:")
    print(f"   Top Gainer: {context['market_summary']['top_gainers'][0] if context['market_summary']['top_gainers'] else 'None'}")
    print(f"   Top Loser: {context['market_summary']['top_losers'][0] if context['market_summary']['top_losers'] else 'None'}")
    print(f"   Stocks with earnings: {len(context['earnings_today'])}")
    print(f"   Stocks with news: {len(context['news_mentions'])}")

def main():
    print("="*60)
    print("STEP 0A: Fetch Real-Time Market Data")
    print("="*60)
    
    data = fetch_market_data()
    save_market_context(data)
    
    print("\n✅ Market context saved to market_context.json")

if __name__ == "__main__":
    main()
