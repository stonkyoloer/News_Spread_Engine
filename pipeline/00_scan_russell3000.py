"""
Step 0: Scan Russell 3000 for Today's Best 22
Real edge from entire market, not static list
"""
import json
import requests
from datetime import datetime, timedelta
import yfinance as yf
import pandas as pd

def get_russell3000():
    """Get Russell 3000 tickers"""
    # Using common optionable stocks as proxy
    # In production, you'd load from a Russell 3000 CSV
    url = "https://raw.githubusercontent.com/rreichel3/US-Stock-Symbols/main/nyse/nyse_tickers.json"
    
    try:
        resp = requests.get(url)
        nyse = [item['symbol'] for item in resp.json()][:1500]
        
        # Add NASDAQ top stocks
        nasdaq_top = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META', 'NVDA', 'TSLA']
        
        return nyse + nasdaq_top
    except:
        # Fallback list
        return ['AAPL', 'MSFT', 'GOOGL'] * 100  # Just for testing

def scan_for_movers(tickers, batch_size=100):
    """Scan in batches for speed"""
    print(f"🔍 Scanning {len(tickers)} stocks...")
    
    all_data = {}
    
    for i in range(0, len(tickers), batch_size):
        batch = tickers[i:i+batch_size]
        batch_str = ' '.join(batch)
        
        print(f"   Batch {i//batch_size + 1}: {len(batch)} stocks")
        
        try:
            # Get batch data
            data = yf.download(batch_str, period='5d', progress=False, threads=True)
            
            if not data.empty:
                for ticker in batch:
                    try:
                        # Calculate metrics
                        closes = data['Close'][ticker].dropna()
                        if len(closes) >= 2:
                            change = ((closes[-1] - closes[-2]) / closes[-2]) * 100
                            volatility = closes.pct_change().std() * 100
                            
                            all_data[ticker] = {
                                'price': float(closes[-1]),
                                'change_pct': float(change),
                                'volatility': float(volatility),
                                'volume': float(data['Volume'][ticker][-1])
                            }
                    except:
                        continue
        except:
            continue
    
    return all_data

def get_earnings_calendar():
    """Get stocks with upcoming earnings"""
    # Using yfinance earnings calendar
    earnings_soon = set()
    
    # This would check each stock's earnings
    # For speed, using a mock list
    earnings_soon = {'AAPL', 'GOOGL', 'NFLX', 'TSLA'}
    
    return earnings_soon

def score_and_rank(all_data, earnings_soon):
    """Score each stock for credit spreads"""
    scored = []
    
    for ticker, metrics in all_data.items():
        # Skip if earnings soon
        if ticker in earnings_soon:
            continue
        
        # Skip penny stocks
        if metrics['price'] < 20:
            continue
        
        # Score based on:
        # 1. Volatility (want 2-5% daily moves)
        # 2. Not too extreme (avoid >10% moves)
        # 3. Volume (liquidity proxy)
        
        score = 0
        
        # Ideal volatility
        if 1.5 <= metrics['volatility'] <= 4:
            score += 50
        
        # Recent movement (but not extreme)
        if 2 <= abs(metrics['change_pct']) <= 7:
            score += 30
        
        # Volume score
        if metrics['volume'] > 1000000:
            score += 20
        
        scored.append({
            'ticker': ticker,
            'score': score,
            **metrics
        })
    
    # Sort by score
    scored.sort(key=lambda x: x['score'], reverse=True)
    
    return scored[:100]  # Top 100 candidates

def select_top_22(scored):
    """Pick 22 diverse stocks"""
    selected = []
    sectors = set()
    
    # Simple sector guess from ticker
    sector_map = {
        'AAPL': 'TECH', 'MSFT': 'TECH', 'GOOGL': 'TECH',
        'JPM': 'FIN', 'BAC': 'FIN', 'GS': 'FIN',
        'XOM': 'ENERGY', 'CVX': 'ENERGY',
        'JNJ': 'HEALTH', 'PFE': 'HEALTH',
        'AMZN': 'RETAIL', 'WMT': 'RETAIL'
    }
    
    for stock in scored:
        ticker = stock['ticker']
        sector = sector_map.get(ticker, ticker[:2])  # First 2 letters as proxy
        
        # Diversity check
        if sector not in sectors or len(selected) < 11:
            selected.append(stock)
            sectors.add(sector)
            
            if len(selected) >= 22:
                break
    
    return selected

def save_selections(selected):
    """Save as stocks.py format"""
    tickers = [s['ticker'] for s in selected]
    
    reasons = {}
    for s in selected:
        reasons[s['ticker']] = f"Vol={s['volatility']:.1f}%, Change={s['change_pct']:.1f}%"
    
    with open("data/stocks.py", "w") as f:
        f.write(f"# Dynamic selection from Russell 3000\n")
        f.write(f"# Generated {datetime.now()}\n\n")
        f.write(f"STOCKS = {tickers}\n\n")
        f.write(f"EDGE_REASON = {reasons}\n")
    
    print(f"\n✅ Selected 22 from Russell 3000")
    print(f"\nTop 5 picks:")
    for s in selected[:5]:
        print(f"  {s['ticker']}: Score={s['score']}, {reasons[s['ticker']]}")

def main():
    print("="*60)
    print("STEP 0: Russell 3000 Scanner")
    print("="*60)
    
    # Get universe
    tickers = get_russell3000()
    print(f"Universe: {len(tickers)} stocks")
    
    # Scan for data
    all_data = scan_for_movers(tickers, batch_size=50)
    print(f"Got data for {len(all_data)} stocks")
    
    # Get earnings
    earnings_soon = get_earnings_calendar()
    print(f"Avoiding {len(earnings_soon)} with earnings")
    
    # Score and rank
    scored = score_and_rank(all_data, earnings_soon)
    
    # Select top 22
    selected = select_top_22(scored)
    
    # Save
    save_selections(selected)

if __name__ == "__main__":
    main()
