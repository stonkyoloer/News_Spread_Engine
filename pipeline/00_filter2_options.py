"""
FILTER 2: Options Chain Check
403 stocks → ~250 stocks
Check for liquid options chains
"""
import json
import sys
import os
from datetime import datetime, timedelta
from tastytrade import Session
from tastytrade.instruments import get_option_chain

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import USERNAME, PASSWORD

def filter_options_chains():
    """Filter 2: Has options with good chains"""
    print("="*60)
    print("FILTER 2: Options Chain Check")
    print("="*60)
    
    # Load Filter 1 results
    with open("data/filter1_results.json", "r") as f:
        data = json.load(f)
        stocks = data["passed_stocks"]
    
    print(f"Input: {len(stocks)} stocks from Filter 1")
    print("Criteria: Has options, 20+ strikes, 15-45 DTE\n")
    
    sess = Session(USERNAME, PASSWORD)
    passed = []
    failed = []
    
    today = datetime.now().date()
    
    for i, stock_data in enumerate(stocks, 1):
        ticker = stock_data['ticker']
        
        if i % 10 == 0:
            print(f"Progress: {i}/{len(stocks)}...")
        
        try:
            chain = get_option_chain(sess, ticker)
            
            if not chain:
                failed.append({'ticker': ticker, 'reason': 'no chain'})
                continue
            
            # Find 15-45 DTE expirations
            good_exps = []
            for exp_date in chain.keys():
                dte = (exp_date - today).days
                if 15 <= dte <= 45:
                    good_exps.append({'date': str(exp_date), 'dte': dte})
            
            if not good_exps:
                failed.append({'ticker': ticker, 'reason': 'no 15-45 DTE'})
                continue
            
            # Check strike count
            best_exp = datetime.strptime(good_exps[0]['date'], '%Y-%m-%d').date()
            options = chain[best_exp]
            
            if len(options) < 20:
                failed.append({'ticker': ticker, 'reason': f'only {len(options)} strikes'})
                continue
            
            # Passed
            passed.append({
                **stock_data,
                'expirations': len(good_exps),
                'best_expiration': good_exps[0],
                'strikes_count': len(options)
            })
            
            print(f"   ✅ {ticker}: {len(options)} strikes, {len(good_exps)} exp")
            
        except Exception as e:
            failed.append({'ticker': ticker, 'reason': str(e)[:30]})
    
    return passed, failed

def save_filter2_results(passed, failed):
    """Save results"""
    output = {
        'timestamp': datetime.now().isoformat(),
        'filter': 'Options Chains',
        'input_count': len(passed) + len(failed),
        'passed_count': len(passed),
        'failed_count': len(failed),
        'passed_stocks': passed,
        'failed_reasons': failed[:20]
    }
    
    with open('data/filter2_results.json', 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"\n{'='*60}")
    print(f"FILTER 2 RESULTS:")
    print(f"   Input: {len(passed) + len(failed)} stocks")
    print(f"   Passed: {len(passed)} stocks")
    print(f"   Failed: {len(failed)} stocks")

def main():
    passed, failed = filter_options_chains()
    save_filter2_results(passed, failed)
    print(f"\n✅ Filter 2 complete. Results in filter2_results.json")

if __name__ == "__main__":
    main()
