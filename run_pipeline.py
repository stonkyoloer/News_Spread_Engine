#!/usr/bin/env python3
"""
Credit Spread Pipeline Runner
Runs complete pipeline from filtering to final trades
"""
import subprocess
import sys
import time
from datetime import datetime

def run_step(step_num, script, description):
    """Run a pipeline step"""
    print(f"\n{'='*60}")
    print(f"STEP {step_num}: {description}")
    print(f"{'='*60}")
    
    result = subprocess.run([sys.executable, script], capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"✅ Step {step_num} complete")
        # Show key output
        if "Passed:" in result.stdout:
            for line in result.stdout.split('\n'):
                if "Passed:" in line:
                    print(f"   {line.strip()}")
        return True
    else:
        print(f"❌ Step {step_num} failed")
        print(result.stderr[:200])
        return False

def main():
    print("\n" + "="*80)
    print("CREDIT SPREAD PIPELINE")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*80)
    
    # Phase 1: Filter S&P 500 to 22 stocks
    print("\n📊 PHASE 1: STOCK FILTERING")
    filters = [
        ("0A", "pipeline/00a_get_sp500_live.py", "Get S&P 500 list"),
        ("0B", "pipeline/00_filter1_price.py", "Filter by price & liquidity"),
        ("0C", "pipeline/00_filter2_options.py", "Check options availability"),
        ("0D", "pipeline/00_filter3_iv.py", "Get IV data"),
        ("0E", "pipeline/00_filter4_select22.py", "Select final 22")
    ]
    
    for step, script, desc in filters:
        if not run_step(step, script, desc):
            print("Pipeline stopped. Fix error and retry.")
            return
    
    # Phase 2: Find credit spreads
    print("\n📈 PHASE 2: CREDIT SPREAD DISCOVERY")
    pipeline = [
        (1, "pipeline/02_get_stock_prices.py", "Get real-time prices"),
        (2, "pipeline/03_get_options_chains.py", "Get options chains"),
        (3, "pipeline/04_check_liquidity.py", "Check liquidity"),
        (4, "pipeline/05_get_greeks.py", "Get Greeks data"),
        (5, "pipeline/06_calculate_spreads_fixed.py", "Build credit spreads"),
        (6, "pipeline/07_calculate_pop_roi.py", "Calculate PoP"),
        (7, "pipeline/08_rank_spreads.py", "Rank spreads"),
        (8, "pipeline/09_build_report_table.py", "Build report"),
        (9, "pipeline/10_gpt_risk_analysis_top9.py", "GPT analysis")
    ]
    
    for step, script, desc in pipeline:
        if not run_step(step, script, desc):
            print("Pipeline stopped. Fix error and retry.")
            return
    
    print("\n" + "="*80)
    print("✅ PIPELINE COMPLETE!")
    print("="*80)
    print("\nCheck data/top9_analysis.json for final trades")

if __name__ == "__main__":
    main()
