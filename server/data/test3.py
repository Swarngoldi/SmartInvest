import csv
import os
from typing import List, Dict, Union

def load_stocks_from_csv(filepath: str) -> List[Dict[str, Union[str, float]]]:
    """Load stock data from CSV file"""
    stocks = []
    try:
        with open(filepath, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    processed_row = {
                        'symbol': row['Stock Symbol'].strip(),
                        'name': row['Full Name'].strip(),
                        'price': float(row['Current Price']) if row['Current Price'].strip() else 0.0,
                        'rank': float(row['Rank']) if '.' in row['Rank'] else int(row['Rank']),
                        'theme': os.path.splitext(os.path.basename(filepath))[0]
                    }
                    stocks.append(processed_row)
                except Exception as e:
                    print(f"Error processing row {row.get('Stock Symbol', 'unknown')}: {str(e)}")
                    continue
    except FileNotFoundError:
        print(f"Error: File not found - {filepath}")
    return stocks

def generate_pure_basket(investment: float, stocks: List[dict], theme: str) -> dict:
    """Generate basket for a single theme with rank-based selection up to rank 15"""
    basket = {
        'theme': theme,
        'stocks': [],
        'investment': investment,
        'remaining': investment,
        'count': 0
    }
    
    # Filter stocks up to rank 15 and sort by rank
    eligible_stocks = [s for s in stocks if s['rank'] <= 15]
    sorted_stocks = sorted(eligible_stocks, key=lambda x: x['rank'])
    
    for stock in sorted_stocks:
        if basket['count'] >= 10:  # Max stocks
            break
        if stock['price'] <= basket['remaining']:
            basket['stocks'].append(stock)
            basket['remaining'] -= stock['price']
            basket['count'] += 1
    
    basket['invested'] = investment - basket['remaining']
    return basket

def generate_pure_baskets(income: float, theme_files: List[str], risk: str = 'medium') -> List[dict]:
    """Generate independent baskets for each theme"""
    risk_multiplier = {'low': 0.1, 'medium': 0.2, 'high': 0.3}.get(risk.lower(), 0.2)
    investment = income * risk_multiplier
    baskets = []
    
    for theme_file in theme_files:
        theme_name = os.path.splitext(theme_file)[0]
        stocks = load_stocks_from_csv(theme_file)
        if not stocks:
            print(f"Skipping {theme_name} - no stocks found")
            continue
        
        basket = generate_pure_basket(investment, stocks, theme_name)
        baskets.append(basket)
    
    return baskets

def generate_hybrid_basket(income: float, theme_files: List[str], risk: str = 'medium') -> dict:
    """Generate hybrid basket with interleaved ranking and no duplicates"""
    risk_multiplier = {'low': 0.1, 'medium': 0.2, 'high': 0.3}.get(risk.lower(), 0.2)
    investment = income * risk_multiplier
    
    # Load all stocks from all themes
    all_stocks = []
    theme_stocks = {}
    for theme_file in theme_files:
        theme_name = os.path.splitext(theme_file)[0]
        stocks = load_stocks_from_csv(theme_file)
        theme_stocks[theme_name] = sorted(
            [s for s in stocks if s['rank'] <= 15], 
            key=lambda x: x['rank']
        )
        all_stocks.extend(stocks)
    
    # Generate hybrid basket
    basket = {
        'theme': "Hybrid (" + "+".join(theme_stocks.keys()) + ")",
        'stocks': [],
        'investment': investment,
        'remaining': investment,
        'count': 0
    }
    
    # Interleave stocks by taking rank 1 from each theme, then rank 2, etc.
    max_rank = 15
    used_symbols = set()
    
    for rank in range(1, max_rank + 1):
        for theme, stocks in theme_stocks.items():
            if basket['count'] >= 10:  # Max stocks
                break
            
            # Find stock with current rank in this theme
            for stock in stocks:
                if (stock['rank'] == rank and 
                    stock['symbol'] not in used_symbols and 
                    stock['price'] <= basket['remaining']):
                    
                    basket['stocks'].append(stock)
                    used_symbols.add(stock['symbol'])
                    basket['remaining'] -= stock['price']
                    basket['count'] += 1
                    break
    
    basket['invested'] = investment - basket['remaining']
    return basket

def format_basket(basket: dict) -> str:
    """Format basket output"""
    output = [
        f"\nTHEME: {basket['theme']}",
        "-" * 40,
        f"Investment: ₹{basket['investment']:,.2f}",
        f"Stocks: {basket['count']}",
        "-" * 20
    ]
    
    for i, stock in enumerate(basket['stocks'], 1):
        theme_mark = f" ({stock['theme']})" if 'Hybrid' in basket['theme'] else ""
        output.append(f"{i}. {stock['symbol']}{theme_mark}: {stock['name']} (₹{stock['price']:,.2f}, Rank: {stock['rank']})")
    
    output.extend([
        "-" * 20,
        f"Invested: ₹{basket['invested']:,.2f}",
        f"Remaining: ₹{basket['remaining']:,.2f}",
        "=" * 60
    ])
    return "\n".join(output)

if __name__ == "__main__":
    # Configuration
    INCOME = 50000
    RISK = "medium"
    THEME_FILES = ["Midcap.csv", "IT.csv", "Healthcare.csv", "Auto.csv"]  # Update with your files
    
    print("=== STOCK BASKET GENERATOR ===")
    
    # Generate pure theme baskets
    print("\n=== PURE THEME BASKETS ===")
    pure_baskets = generate_pure_baskets(INCOME, THEME_FILES, RISK)
    for basket in pure_baskets:
        print(format_basket(basket))
    
    # Generate hybrid basket
    print("\n=== HYBRID BASKET ===")
    hybrid_basket = generate_hybrid_basket(INCOME, THEME_FILES, RISK)
    print(format_basket(hybrid_basket))