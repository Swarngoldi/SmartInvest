import csv
import os
import json
import sys
from typing import List, Dict, Union

def load_stocks_from_csv(filepath: str) -> List[Dict[str, Union[str, float]]]:
    """Load stock data from CSV file with validation"""
    if not os.path.exists(filepath):
        print(f"Error: CSV file not found - {filepath}")
        return []
    
    if os.path.getsize(filepath) < 10:
        print(f"Error: CSV file too small - {filepath}")
        return []

    stocks = []
    try:
        with open(filepath, mode='r') as file:
            reader = csv.DictReader(file)
            if not reader.fieldnames:
                print(f"Error: Empty CSV file - {filepath}")
                return []
                
            print(f"\nLoading {filepath}...")
            for i, row in enumerate(reader):
                try:
                    processed_row = {
                        'symbol': row.get('Stock Symbol', '').strip(),
                        'name': row.get('Full Name', '').strip(),
                        'price': float(row['Current Price']) if row.get('Current Price') else 0.0,
                        'rank': float(row['Rank']) if '.' in row.get('Rank', '') else int(row.get('Rank', 0)),
                        'theme': os.path.splitext(os.path.basename(filepath))[0],
                        '52_week_low': float(row['52-Week Low']) if row.get('52-Week Low') else 0.0,
                        '52_week_high': float(row['52-Week High']) if row.get('52-Week High') else 0.0,
                        'current_price': float(row['Current Price']) if row.get('Current Price') else 0.0
                    }
                    if not processed_row['symbol']:
                        raise ValueError("Missing stock symbol")
                    stocks.append(processed_row)
                except Exception as e:
                    print(f"  Row {i+1} error: {str(e)}")
                    continue
                    
        print(f"  Loaded {len(stocks)} valid stocks from {filepath}")
        return stocks
        
    except Exception as e:
        print(f"Fatal error reading {filepath}: {str(e)}")
        return []

def generate_pure_basket(investment: float, stocks: List[dict], theme: str, risk: str) -> dict:
    """Generate basket for a single theme with debugging"""
    print(f"\nGenerating {theme} basket (₹{investment:,.2f})...")
    
    basket = {
        'theme': theme,
        'type': 'pure',
        'stocks': [],
        'investment': investment,
        'remaining': investment,
        'count': 0,
        'risk': risk
    }
    
    eligible_stocks = [s for s in stocks if s['rank'] <= 15]
    print(f"  Found {len(eligible_stocks)} eligible stocks (rank ≤ 15)")
    
    sorted_stocks = sorted(eligible_stocks, key=lambda x: x['rank'])
    
    for stock in sorted_stocks:
        if basket['count'] >= 10:
            print(f"  Reached max 10 stocks for {theme}")
            break
        if stock['price'] <= basket['remaining']:
            basket['stocks'].append(stock)
            basket['remaining'] -= stock['price']
            basket['count'] += 1
            print(f"  Added {stock['symbol']} (₹{stock['price']:.2f})")
        else:
            print(f"  Skipped {stock['symbol']} (₹{stock['price']:.2f} - insufficient funds)")
    
    basket['invested'] = investment - basket['remaining']
    print(f"  Final: {len(basket['stocks'])} stocks, ₹{basket['invested']:,.2f} invested")
    return basket

def generate_hybrid_basket(investment: float, theme_files: List[str], risk: str) -> dict:
    """Generate hybrid basket with detailed logging"""
    print(f"\nGenerating Hybrid basket (₹{investment:,.2f})...")
    
    basket = {
        'theme': "Hybrid",
        'type': 'hybrid',
        'stocks': [],
        'investment': investment,
        'remaining': investment,
        'count': 0,
        'risk': risk
    }
    
    all_stocks = []
    theme_stocks = {}
    
    for theme_file in theme_files:
        theme_name = os.path.splitext(theme_file)[0]
        stocks = load_stocks_from_csv(theme_file)
        filtered = [s for s in stocks if s['rank'] <= 15]
        theme_stocks[theme_name] = sorted(filtered, key=lambda x: x['rank'])
        print(f"  {theme_name}: {len(filtered)} eligible stocks")
        all_stocks.extend(stocks)
    
    max_rank = 15
    used_symbols = set()
    
    for rank in range(1, max_rank + 1):
        for theme, stocks in theme_stocks.items():
            if basket['count'] >= 10:
                break
            
            for stock in stocks:
                if (stock['rank'] == rank and 
                    stock['symbol'] not in used_symbols and 
                    stock['price'] <= basket['remaining']):
                    
                    basket['stocks'].append(stock)
                    used_symbols.add(stock['symbol'])
                    basket['remaining'] -= stock['price']
                    basket['count'] += 1
                    print(f"  Added {stock['symbol']} from {theme} (Rank {rank}, ₹{stock['price']:.2f})")
                    break
    
    basket['invested'] = investment - basket['remaining']
    print(f"  Final: {len(basket['stocks'])} stocks, ₹{basket['invested']:,.2f} invested")
    return basket

def export_baskets_to_json(baskets: List[dict], filename: str = 'baskets.json'):
    """Export with validation and backup"""
    try:
        print("\n=== EXPORTING BASKETS ===")
        json_str = json.dumps(baskets, indent=2)
        
        if len(json_str) < 100:
            raise ValueError("JSON output too small - possible data loss")
            
        # Create backup if file exists
        if os.path.exists(filename):
            backup_name = f"{filename}.bak"
            os.replace(filename, backup_name)
            print(f"  Created backup: {backup_name}")
        
        with open(filename, 'w') as f:
            f.write(json_str)
            f.flush()
            os.fsync(f.fileno())
            
        print(f"Successfully exported to {filename}")
        print(f"  File size: {os.path.getsize(filename)/1024:.1f} KB")
        print(f"  Total baskets: {len(baskets)}")
        print(f"  Total stocks: {sum(len(b['stocks']) for b in baskets)}")
        
    except Exception as e:
        print(f"\nERROR exporting JSON: {str(e)}")
        raise

def main(income: float, risk: str, theme_files: List[str]):
    """Main function with enhanced logging"""
    print(f"\n{' STARTING BASKET GENERATOR ':=^80}")
    print(f"Income: ₹{income:,.2f} | Risk: {risk} | Themes: {len(theme_files)}")
    
    risk_multiplier = {'low': 0.1, 'medium': 0.2, 'high': 0.3}.get(risk.lower(), 0.2)
    basket_investment = income * risk_multiplier  # Full amount for each basket
    print(f"Investment per basket: ₹{basket_investment:,.2f}")

    # Generate pure theme baskets (each gets full investment amount)
    pure_baskets = []
    print(f"\nGenerating {len(theme_files)} pure baskets (₹{basket_investment:,.2f} each)")
    
    for theme_file in theme_files:
        theme_name = os.path.splitext(theme_file)[0]
        stocks = load_stocks_from_csv(theme_file)
        if stocks:
            basket = generate_pure_basket(basket_investment, stocks, theme_name, risk)
            pure_baskets.append(basket)
        else:
            print(f"  Skipping {theme_name} - no valid stocks")

    # Generate hybrid basket (also gets full investment amount)
    print(f"\nGenerating hybrid basket (₹{basket_investment:,.2f})")
    hybrid_basket = generate_hybrid_basket(basket_investment, theme_files, risk)
    
    # Combine and export
    all_baskets = pure_baskets + [hybrid_basket]
    export_baskets_to_json(all_baskets)
    
    print("\n=== FINAL SUMMARY ===")
    for i, basket in enumerate(all_baskets):
        print(f"{i+1}. {basket['theme']}: {len(basket['stocks'])} stocks (₹{basket['invested']:,.2f})")
    
    print(f"\n{' GENERATION COMPLETE ':=^80}\n")
    return all_baskets

if __name__ == "__main__":
    if len(sys.argv) == 3:
        try:
            INCOME = float(sys.argv[1])
            RISK = sys.argv[2].lower()
            if RISK not in ['low', 'medium', 'high']:
                raise ValueError("Risk must be low/medium/high")
                
            THEME_FILES = [
                "Largecap.csv", "Midcap.csv", "Smallcap.csv", 
                "Realty.csv", "Healthcare.csv", "Auto.csv",
                "Consumer durables.csv", "IT.csv", 
                "Consumer Discretionary.csv"
            ]
            
            # Verify all CSV files exist
            missing_files = [f for f in THEME_FILES if not os.path.exists(f)]
            if missing_files:
                raise FileNotFoundError(f"Missing CSV files: {missing_files}")
            
            main(INCOME, RISK, THEME_FILES)
            
        except Exception as e:
            print(f"\nError: {str(e)}")
            print("Usage: python basket_generator.py <income> <risk>")
            print("Example: python basket_generator.py 500000 high")
            sys.exit(1)
    else:
        print("Usage: python basket_generator.py <income> <risk>")
        print("Example: python basket_generator.py 500000 high")