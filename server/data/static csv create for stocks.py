import csv
import os
import requests
from bs4 import BeautifulSoup

csv_file = "sm.csv"

def initialize_csv(file_name):
    if not os.path.exists(file_name):
        with open(file_name, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Stock Symbol", "Full Name", "Theme"])

def fetch_stock_full_name_stockanalysis(stock_symbol):
    try:
        url = f"https://stockanalysis.com/quote/nse/{stock_symbol}/"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        response = requests.get(url, headers=headers)
        print(f"Fetching {url} - Status Code: {response.status_code}")
        
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Extract company name from <title> tag
        title_tag = soup.find("title")
        if title_tag:
            title_text = title_tag.text.strip()
            company_name = title_text.split(" (NSE:")[0]  # Extract company name before (NSE:TICKER)
            return company_name
        else:
            print(f"⚠ Could not find company name for {stock_symbol}")
            return "Unknown"
    except Exception as e:
        print(f"❌ Error fetching name for {stock_symbol}: {e}")
        return "Unknown"

def add_stock(file_name, stock_symbol, theme):
    existing_entries = set()
    
    if os.path.exists(file_name):
        with open(file_name, mode="r") as file:
            reader = csv.reader(file)
            next(reader, None)
            for row in reader:
                existing_entries.add((row[0].strip().lower(), row[2].strip().lower()))

    if (stock_symbol.strip().lower(), theme.strip().lower()) in existing_entries:
        print(f"{stock_symbol} with theme '{theme}' already exists. Skipping.")
    else:
        full_name = fetch_stock_full_name_stockanalysis(stock_symbol)
        with open(file_name, mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([stock_symbol, full_name, theme])
            print(f"{stock_symbol} ({full_name}) with theme '{theme}' added to CSV.")

initialize_csv(csv_file)

# stocks = [ "YESBANK", "SRF", "SBICARD", "FEDERALBNK", "MARICO", 
#     "COLPAL", "CONCOR", "MPHASIS", "POLICYBZR", "DIXON", 
#     "MRF", "ACC", "HINDPETRO", "MUTHOOTFIN", "GMRAIRPORT", 
#     "PHOENIXLTD", "CUMMINSIND", "KPITTECH", "TATACOMM", "INDHOTEL", 
#     "ALKEM", "NMDC", "ASTRAL", "BHARATFORG", "POLYCAB", 
#     "LUPIN", "VOLTAS", "UPL", "GODREJPROP", "SUNDARMFIN", 
#     "AUROPHARMA", "ABCAPITAL", "APLAPOLLO", "SAIL", "ASHOKLEY", 
#     "MAXHEALTH", "LTF", "PETRONET", "OFSS", "PERSISTENT", 
#     "PIIND", "OBEROIRLTY", "INDUSTOWER", "HDFCAMC", "CGPOWER", 
#     "SUZLON", "IDEA", "SUPREMEIND", "IDFCFIRSTB", "AUBANK"]


# stocks = ["TATAMOTORS", "BHARATFORG", "MOTHERSON", "BAJAJ AUTO LIMITED", "APOLLOTYRE", "ASHOKLEY", 
#           "MARUTI", "EXIDEIND", "MRF", "HEROMOTOCO", "UNOMINDA", "EICHERMOT", "TVSMOTOR", 
#           "BALKRISIND", "BOSCHLTD", "TIINDIA", "SUNDRMFAST", "M&M"]

# stocks = ["ABBOTINDIA", "ALKEM", "APOLLOHOSP", "AUROPHARMA", "BIOCON", "CIPLA", "DIVISLAB", "DRREDDY", 
#           "FORTIS", "GLENMARK", "GRANULES", "IPCALAB", "LAURUSLABS", "LUPIN", "MANKIND", "MAXHEALTH", 
#           "SUNPHARMA", "SYNGENE", "TORNTPHARM", "ZYDUSLIFE"]

# 

# stocks = [
#     "TATAMOTORS", "MARUTI","M&M", "EICHERMOT", 
#     "ASIANPAINT", "TITAN", "DMART", "DLF", "HAVELLS", 
#     "ZOMATO", "VOLTAS", "MOTHERSON", "BHARATFORG", "GODREJPROP", 
#     "TRENT", "JUBLFOOD", "MRF", "TVSMOTOR", "PAGEIND", 
#     "BATAINDIA", "DIXON", "AMBER", "INDHOTEL", "NAUKRI", 
#     "IRCTC", "UNOMINDA", "SUNTV", "SYMPHONY", "CROMPTON",
#     "KAJARIACER", "WHIRLPOOL", "VGUARD", "METROBRAND", "PVRINOX",
#     "JUSTDIAL", "NYKAA", "OLECTRA", "KALYANKJIL"
# ]

#stocks = ['HINDUNILVR', 'ITC', 'NESTLEIND', 'BRITANNIA', 'TATACONSUM', 'DABUR', 'GODREJCP', 'MARICO', 'COLPAL', 'PGHH', 'PATANJALI', 'EMAMILTD', 'LTFOODS', 'RADICO', 'VBL', 'JYOTHYLAB','UBL', 'KRBL', 'BAJAJCON', 'HERITGFOOD', 'GODREJAGRO', 'VSTIND', 'RENUKA', 'SULA']

# stocks = [
#     "ANANTRAJ", "GODREJPROP", "DLF", "SIGNATURE",
#     "LODHA", "SOBHA", "PRESTIGE", "PHOENIXLTD",
#     "OBEROIRLTY", "BRIGADE"
# ]

#stocks = ['RELIANCE', 'TCS', 'HINDUNILVR', 'ITC', 'INFY', 'LT', 'ASIANPAINT', 'MARUTI', 'SUNPHARMA', 'TATAMOTORS', 'NESTLEIND', 'M&M', 'ULTRACEMCO', 'ADANIENT', 'ADANIPORTS', 'TATASTEEL', 'POWERGRID', 'JSWSTEEL', 'WIPRO', 'TITAN', 'COALINDIA', 'GRASIM', 'DRREDDY', 'NTPC', 'EICHERMOT', 'TECHM', 'CIPLA', 'ONGC', 'TATACONSUM']

stocks = [
    'TATACHEM', 'RAMCOCEM', 'AARTIIND', 'RADICO', 'AMARAJABAT', 
    'LAURUSLABS', 'CROMPTON', 'NAVINFLUOR', 'ABREL', 'BSOFT', 
    'DELHIVERY', 'CASTROLIND', 'GESHIP', 'GSPL', 'KEC', 
    'SONATSOFTW', 'ASTERDM', 'CESC', 'LALPATHLAB', 'AMBER', 
    'CYIENT', 'AFFLE', 'HFCL', 'KAYNES', 'NATCOPHARM', 
    'CAMS', 'CDSL', 'HSCL', 'HINDCOPPER', 'NEULANDLAB'
]

theme = "Smallcap"

for stock in stocks:
    add_stock(csv_file, stock, theme)
