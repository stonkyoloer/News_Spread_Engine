"""
Step 1: Dynamic GPT Stock Selection with Real-Time Data
"""
import os
import sys
import json
from datetime import datetime
from openai import OpenAI

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import OPENAI_API_KEY

if not OPENAI_API_KEY:
    print("❌ Set OPENAI_API_KEY")
    exit(1)

def load_market_context():
    """Load real-time market data"""
    try:
        with open("data/market_context.json", "r") as f:
            return json.load(f)
    except:
        print("⚠️ No market context - run 00a_fetch_news.py first")
        return None

def create_dynamic_prompt(context):
    """Build prompt with real-time data"""
    
    prompt = f"TODAY: {datetime.now().strftime('%Y-%m-%d')}\n\n"
    
    if context:
        prompt += "REAL-TIME MARKET DATA:\n"
        
        # Add top movers
        prompt += "\nTOP GAINERS TODAY:\n"
        for ticker, change in context['market_summary']['top_gainers'][:5]:
            prompt += f"- {ticker}: +{change}%\n"
        
        prompt += "\nTOP LOSERS TODAY:\n"
        for ticker, change in context['market_summary']['top_losers'][:5]:
            prompt += f"- {ticker}: {change}%\n"
        
        # Add earnings
        if context['earnings_today']:
            prompt += "\nEARNINGS TODAY (AVOID):\n"
            for ticker, date in context['earnings_today'][:5]:
                prompt += f"- {ticker}\n"
        
        # Add news
        if context['news_mentions']:
            prompt += "\nRECENT NEWS:\n"
            for ticker, headline in context['news_mentions'][:5]:
                prompt += f"- {ticker}: {headline[:60]}...\n"
    
    prompt += """
SELECT 22 STOCKS for credit spreads based on TODAY'S CONDITIONS.

CRITERIA:
1. AVOID stocks with earnings today
2. PREFER stocks with 2-5% moves (volatility)
3. INCLUDE top movers if liquid
4. DIVERSIFY across sectors
5. Must have weekly options

OUTPUT EXACTLY:
STOCKS = [22 tickers]
EDGE_REASON = {"TICKER": "why chosen today"}
"""
    return prompt

def main():
    print("="*60)
    print("STEP 1: Dynamic Stock Selection")
    print("="*60)
    
    # Load market data
    context = load_market_context()
    
    # Create dynamic prompt
    prompt = create_dynamic_prompt(context)
    
    print("🤖 Calling GPT with today's data...")
    
    # Call GPT
    client = OpenAI(api_key=OPENAI_API_KEY)
    
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Select stocks based on real-time data. Output Python code only."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=1500
    )
    
    content = response.choices[0].message.content
    print("✅ Got dynamic response")
    
    # Parse response
    if "```python" in content:
        start = content.find("```python") + 9
        end = content.find("```", start)
        code = content[start:end]
    else:
        code = content
    
    exec_globals = {}
    exec(code, exec_globals)
    
    stocks = exec_globals.get("STOCKS", [])
    reasons = exec_globals.get("EDGE_REASON", {})
    
    # Save
    with open("data/stocks.py", "w") as f:
        f.write(f"# Generated {datetime.now()} with real-time data\n")
        f.write(f"STOCKS = {stocks}\n\n")
        f.write(f"EDGE_REASON = {reasons}\n")
    
    print(f"✅ Selected {len(stocks)} stocks based on TODAY")
    
    # Show selections
    print("\nToday's picks:")
    for stock in stocks[:5]:
        reason = reasons.get(stock, "")
        print(f"  {stock}: {reason}")

if __name__ == "__main__":
    main()
