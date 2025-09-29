"""
GPT Risk Analysis - Exactly 9 Different Tickers
"""
import os
import json
import sys
from datetime import datetime
from openai import OpenAI

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import OPENAI_API_KEY

if not OPENAI_API_KEY:
    print("❌ Missing OPENAI_API_KEY")
    sys.exit(1)

def load_comprehensive_data():
    data = {}
    
    with open("data/report_table.json", "r") as f:
        data["trades"] = json.load(f)["report_table"]
    
    with open("data/stock_prices.json", "r") as f:
        data["prices"] = json.load(f)["prices"]
    
    for trade in data["trades"]:
        ticker = trade["ticker"]
        
        if ticker in data["prices"]:
            trade["current_price"] = data["prices"][ticker]["mid"]
        
        strikes = trade['legs'].replace('$', '').split('/')
        trade["short_strike"] = float(strikes[0])
        trade["long_strike"] = float(strikes[1])
        
        if "current_price" in trade:
            current = trade["current_price"]
            if "Put" in trade['type']:
                trade["buffer_pct"] = ((current - trade["short_strike"]) / current * 100)
            else:
                trade["buffer_pct"] = ((trade["short_strike"] - current) / current * 100)
    
    return data

def create_top9_prompt(data):
    prompt = f"""You have EXACTLY 9 trades, each with a DIFFERENT ticker.

THESE ARE ALREADY THE TOP 9 - ONE PER TICKER

Just analyze and rank them by best risk/reward.

TRADES (9 UNIQUE TICKERS):
"""
    
    for i, trade in enumerate(data["trades"], 1):
        buffer = trade.get("buffer_pct", 0)
        current = trade.get("current_price", 0)
        roi = float(trade['roi'].rstrip('%'))
        pop = float(trade['pop'].rstrip('%'))
        score = (roi * pop) / 100
        
        prompt += f"""
Trade {i}: {trade['ticker']} {trade['type']} {trade['legs']}
  Current: ${current:.2f} | Buffer: {buffer:.1f}% | Score: {score:.1f}
  ROI: {trade['roi']} | PoP: {trade['pop']} | DTE: {trade['dte']}
  Credit: {trade['net_credit']} | Max Loss: {trade['max_loss']}
"""

    prompt += """

RANK THESE 9 TRADES (all different tickers):

#1. [Best ticker] - [Type] [Strikes]
    Score: [X] | ROI: [X%] | PoP: [X%]
    WHY: [Why this is #1]

[Continue through #9...]

Note: All 9 are different tickers already. Just rank them.
"""
    return prompt

def main():
    print("="*60)
    print("TOP 9 UNIQUE TICKERS ANALYSIS")
    print("="*60)
    
    print("📊 Loading data...")
    data = load_comprehensive_data()
    print(f"   ✓ {len(data['trades'])} unique ticker trades")
    
    # Show tickers
    tickers = [t['ticker'] for t in data['trades']]
    print(f"   Tickers: {', '.join(tickers)}")
    
    prompt = create_top9_prompt(data)
    
    print("\n🤖 Getting rankings from GPT...")
    client = OpenAI(api_key=OPENAI_API_KEY)
    
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "Rank 9 trades (already unique tickers). Focus on risk/reward."
                },
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=2000
        )
        
        gpt_response = response.choices[0].message.content
        print("✅ Analysis complete")
        
        print("\n" + "="*60)
        print("GPT RANKING OF 9 UNIQUE TICKERS:")
        print("="*60)
        print(gpt_response[:1500])
        
        with open("data/top9_analysis.json", "w") as f:
            json.dump({
                "timestamp": datetime.now().isoformat(),
                "analysis": gpt_response,
                "unique_tickers": tickers
            }, f, indent=2)
        
        print("\n✅ Saved to top9_analysis.json")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
