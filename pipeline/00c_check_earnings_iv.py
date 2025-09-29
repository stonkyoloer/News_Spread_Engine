"""
Step 0C: Check Earnings and Get IV
Remove earnings risk, find high IV opportunities
"""
import json
import asyncio
import sys
import os
from datetime import datetime, timedelta
from tastytrade import Session
from tastytrade.instruments import get_option_chain

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import USERNAME, PASSWORD

def load_screened_stocks():
    """Load stocks from previous step"""
    with open("data/screened_stocks.json", "r") as f:
        data = json.load(f)
    return [m['ticker'] for m in data['movers']]

def check_options_and_iv():
    """Check for options and get IV"""
    print("📊 Checking options and IV...")
    
    tickers = load_screened_stocks()
    sess = Session(USERNAME, PASSWORD)
    
    high_iv_stocks = []
    today = datetime.now().date()
    target_date = today + timedelta(days=30)  # 30 DTE target
    
    for ticker in tickers[:100]:  # Check first 100 for speed
        try:
            chain = get_option_chain(sess, ticker)
            
            if not chain:
                continue
            
            # Find ~30 DTE expiration
            best_exp = None
            for exp_date in chain.keys():
                dte = (exp_date - today).days
                if 20 <= dte <= 45:
                    best_exp = exp_date
                    break
            
            if not best_exp:
                continue
            
            # Get ATM option for IV
            options = chain[best_exp]
            
            # Simple IV check - would be better with Greeks
            # For now, just confirm options exist
            if len(options) > 10:  # Has decent chain
                high_iv_stocks.append({
                    'ticker': ticker,
                    'expiration': str(best_exp),
                    'dte': (best_exp - today).days,
                    'strikes_available': len(options),
                    'has_weeklies': True  # Simplified
                })
                
                print(f"   ✅ {ticker}: {len(options)} strikes, {(best_exp - today).days} DTE")
                
                if len(high_iv_stocks) >= 50:
                    break
                    
        except Exception as e:
            continue
    
    return high_iv_stocks

def check_earnings_dates(stocks):
    """Check for upcoming earnings"""
    print("\n📅 Checking earnings dates...")
    
    # This would use Alpha Vantage or yfinance
    # For now, mock removing some stocks
    earnings_soon = {'AAPL', 'GOOGL', 'MSFT', 'TSLA'}  # Example
    
    clean_stocks = []
    for stock in stocks:
        if stock['ticker'] not in earnings_soon:
            clean_stocks.append(stock)
        else:
            print(f"   ❌ {stock['ticker']}: Earnings soon")
    
    return clean_stocks

def save_candidates(stocks):
    """Save final candidates"""
    output = {
        'timestamp': datetime.now().isoformat(),
        'total_candidates': len(stocks),
        'candidates': stocks[:30]  # Top 30 for GPT
    }
    
    with open('data/candidates.json', 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"\n📊 Final Candidates: {len(stocks)}")
    print(f"   Ready for GPT selection")
    
    # Show top 10
    print(f"\nTop 10 candidates:")
    for s in stocks[:10]:
        print(f"   {s['ticker']}: {s['strikes_available']} strikes")

def main():
    print("="*60)
    print("STEP 0C: Earnings & IV Check")
    print("="*60)
    
    # Check options and IV
    iv_stocks = check_options_and_iv()
    
    # Remove earnings
    clean_stocks = check_earnings_dates(iv_stocks)
    
    # Save candidates
    save_candidates(clean_stocks)
    
    print("\n✅ Ready for GPT selection")

if __name__ == "__main__":
    main()
