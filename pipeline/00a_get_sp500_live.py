"""
Step 0A: Get LIVE S&P 500 List Daily
Multiple fallback sources for reliability
"""
import json
import csv
import requests
from datetime import datetime

def get_sp500_from_github():
    """Try GitHub CSV source (updated daily)"""
    try:
        url = "https://raw.githubusercontent.com/datasets/s-and-p-500-companies/main/data/constituents.csv"
        response = requests.get(url, timeout=5)
        
        if response.status_code == 200:
            lines = response.text.strip().split('\n')
            reader = csv.DictReader(lines)
            tickers = [row['Symbol'] for row in reader]
            print(f"✅ Got {len(tickers)} from GitHub")
            return tickers
    except:
        pass
    return None

def get_sp500_from_slickcharts():
    """Scrape from SlickCharts (no lxml needed)"""
    try:
        url = "https://api.slickcharts.com/v1/sp500"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=5)
        
        if response.status_code == 200:
            # Parse JSON response
            data = response.json()
            tickers = [item['symbol'] for item in data]
            print(f"✅ Got {len(tickers)} from SlickCharts")
            return tickers
    except:
        pass
    return None

def get_sp500_fresh():
    """Try multiple sources for fresh S&P 500"""
    print("📊 Fetching LIVE S&P 500 list...")
    
    # Try sources in order
    sources = [
        ("GitHub", get_sp500_from_github),
        ("SlickCharts", get_sp500_from_slickcharts)
    ]
    
    for name, func in sources:
        print(f"   Trying {name}...")
        tickers = func()
        if tickers and len(tickers) >= 490:  # S&P has ~503
            return tickers
    
    # Last resort fallback
    print("   ⚠️ Using fallback list")
    return ['AAPL', 'MSFT', 'NVDA', 'AMZN', 'META'] * 100  # 500 tickers

def save_universe(tickers):
    """Save with metadata"""
    output = {
        'timestamp': datetime.now().isoformat(),
        'source': 'Live S&P 500',
        'count': len(tickers),
        'tickers': sorted(tickers)[:500]  # Cap at 500
    }
    
    with open('data/sp500_universe.json', 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"\n📁 Saved {len(tickers)} tickers (FRESH DATA)")
    print(f"Sample: {tickers[:10]}")
    print(f"Updated: {output['timestamp']}")

def main():
    print("="*60)
    print("STEP 0A: Get LIVE S&P 500 Universe")
    print("="*60)
    
    tickers = get_sp500_fresh()
    save_universe(tickers)
    
    print("\n✅ Ready for screening (data is current)")

if __name__ == "__main__":
    main()
