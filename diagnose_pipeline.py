import json
import os

print("PIPELINE DIAGNOSTIC")
print("="*60)

# Check each data file
files = [
    ("stock_prices.json", ["success", "requested"]),
    ("chains.json", ["success", "chains", "total_expirations"]),  
    ("liquid_chains.json", ["tickers_with_liquidity"]),
    ("greeks.json", ["overall_coverage"]),
    ("spreads.json", ["total_spreads"])
]

for filename, keys in files:
    path = f"data/{filename}"
    if os.path.exists(path):
        with open(path) as f:
            data = json.load(f)
        print(f"\n{filename}:")
        print(f"  Timestamp: {data.get('timestamp', 'N/A')}")
        for key in keys:
            if key in data:
                if isinstance(data[key], dict):
                    print(f"  {key}: {len(data[key])} items")
                else:
                    print(f"  {key}: {data[key]}")
    else:
        print(f"\n{filename}: NOT FOUND")

# Check chain structure
if os.path.exists("data/chains.json"):
    with open("data/chains.json") as f:
        chains = json.load(f)
    
    if "chains" in chains and chains["chains"]:
        first_ticker = list(chains["chains"].keys())[0]
        first_chain = chains["chains"][first_ticker]
        print(f"\nChain structure for {first_ticker}:")
        print(f"  Type: {type(first_chain)}")
        if isinstance(first_chain, list):
            print(f"  Expirations: {len(first_chain)}")
            if first_chain:
                print(f"  First exp keys: {first_chain[0].keys()}")
