"""
Step 0A: Get ALL News from Last 72 Hours
"""
import json
import yfinance as yf
from datetime import datetime, timedelta

def get_sp500_tickers():
    """Get top S&P 500 tickers"""
    return [
        "AAPL", "MSFT", "GOOGL", "AMZN", "META",
        "NVDA", "TSLA", "BRK-B", "JPM", "JNJ",
        "V", "UNH", "PG", "HD", "MA",
        "DIS", "BAC", "XOM", "CVX", "ABBV",
        "PFE", "WMT", "KO", "PEP", "AVGO",
        "CSCO", "VZ", "ADBE", "CMCSA", "INTC"
    ]

def fetch_all_news_72hr():
    """Get ALL news from last 72 hours"""
    print("📰 Fetching 72-hour news window...")
    
    tickers = get_sp500_tickers()
    cutoff = datetime.now() - timedelta(hours=72)
    
    all_news = {}
    
    for ticker in tickers:
        print(f"\n{ticker}: Getting ALL news...")
        try:
            stock = yf.Ticker(ticker)
            
            # Get ALL news, not just 3
            news = stock.news if hasattr(stock, 'news') else []
            
            # Filter to 72 hours
            recent_news = []
            for article in news:
                # Check publish time
                pub_time = article.get('providerPublishTime', 0)
                if pub_time:
                    article_time = datetime.fromtimestamp(pub_time)
                    if article_time > cutoff:
                        recent_news.append({
                            'title': article.get('title', ''),
                            'publisher': article.get('publisher', ''),
                            'time': article_time.strftime('%Y-%m-%d %H:%M'),
                            'hours_ago': int((datetime.now() - article_time).total_seconds() / 3600)
                        })
            
            if recent_news:
                all_news[ticker] = {
                    'count': len(recent_news),
                    'articles': sorted(recent_news, key=lambda x: x['hours_ago'])
                }
                print(f"   ✅ {len(recent_news)} articles in 72hr")
                
                # Show headlines
                for article in recent_news[:5]:
                    print(f"      {article['hours_ago']}h ago: {article['title'][:60]}...")
            
        except Exception as e:
            print(f"   ⚠️ Error: {str(e)[:50]}")
    
    return all_news

def analyze_news_patterns(all_news):
    """Find patterns in news"""
    patterns = {
        'heavy_news': [],  # >5 articles
        'earnings_mentions': [],
        'analyst_actions': [],
        'product_news': [],
        'legal_regulatory': [],
        'no_news': []
    }
    
    for ticker, data in all_news.items():
        count = data['count']
        
        # Heavy news volume
        if count > 5:
            patterns['heavy_news'].append((ticker, count))
        
        # Scan headlines for keywords
        headlines = ' '.join([a['title'].lower() for a in data['articles']])
        
        if 'earnings' in headlines or 'revenue' in headlines or 'eps' in headlines:
            patterns['earnings_mentions'].append(ticker)
        if 'upgrade' in headlines or 'downgrade' in headlines or 'analyst' in headlines:
            patterns['analyst_actions'].append(ticker)
        if 'launch' in headlines or 'announce' in headlines or 'release' in headlines:
            patterns['product_news'].append(ticker)
        if 'sue' in headlines or 'lawsuit' in headlines or 'sec' in headlines or 'fda' in headlines:
            patterns['legal_regulatory'].append(ticker)
    
    # Find no-news stocks
    all_tickers = get_sp500_tickers()
    for ticker in all_tickers:
        if ticker not in all_news:
            patterns['no_news'].append(ticker)
    
    return patterns

def save_news_context(all_news, patterns):
    """Save comprehensive news data"""
    
    output = {
        'timestamp': datetime.now().isoformat(),
        'window_hours': 72,
        'total_articles': sum(d['count'] for d in all_news.values()),
        'stocks_with_news': len(all_news),
        'patterns': patterns,
        'detailed_news': all_news
    }
    
    with open('data/news_72hr.json', 'w') as f:
        json.dump(output, f, indent=2)
    
    print("\n" + "="*60)
    print("📊 72-HOUR NEWS SUMMARY:")
    print("="*60)
    print(f"Total articles: {output['total_articles']}")
    print(f"Stocks with news: {output['stocks_with_news']}")
    print(f"\nHeavy news (>5 articles): {patterns['heavy_news']}")
    print(f"Earnings mentioned: {patterns['earnings_mentions']}")
    print(f"Analyst actions: {patterns['analyst_actions']}")
    print(f"No news (quiet): {patterns['no_news']}")

def main():
    print("="*60)
    print("STEP 0A: Comprehensive 72-Hour News")
    print("="*60)
    
    all_news = fetch_all_news_72hr()
    patterns = analyze_news_patterns(all_news)
    save_news_context(all_news, patterns)
    
    print("\n✅ Complete news saved to news_72hr.json")

if __name__ == "__main__":
    main()
