import pandas as pd
import numpy as np

# Load the original CSV file
file_path = 'sm.csv'  # Replace with your original file path
df = pd.read_csv(file_path)

# Clean the Theme column by stripping whitespace and converting to lowercase for consistent comparison
df['Theme'] = df['Theme'].str.strip().str.lower()

# Get all unique themes in the dataset
all_themes = df['Theme'].unique()

# Process each theme separately
for theme in all_themes:
    if pd.isna(theme):  # Skip if theme is NaN
        continue
        
    # Filter only stocks that match the current theme
    filtered_df = df[df['Theme'] == theme].copy()
    
    # Replace placeholders with NaN in the copied DataFrame
    filtered_df.replace(['n/a', 'Data not found', '-', ''], np.nan, inplace=True)
    
    # Remove commas and % from all string/object columns
    filtered_df = filtered_df.apply(lambda x: x.str.replace(',', '', regex=True) if x.dtype == 'object' else x)
    filtered_df = filtered_df.apply(lambda x: x.str.replace('%', '', regex=True) if x.dtype == 'object' else x)
    
    # Columns to exclude from conversion
    exclude_columns = ['Stock Symbol', 'Theme', 'Full Name', 'Expert Recommendation', 'News Sentiment']
    
    # Convert all other columns to float and round to 2 decimal places
    for column in filtered_df.columns:
        if column not in exclude_columns:
            filtered_df[column] = pd.to_numeric(filtered_df[column], errors='coerce').round(2)
    
    # Capitalize the theme name for the filename
    theme_filename = f"{theme.capitalize()}.csv"
    
    # Save the cleaned and filtered data to a new CSV file
    filtered_df.to_csv(theme_filename, index=False)
    
    print(f"Filtered and cleaned data for theme '{theme}' has been saved to '{theme_filename}'")

print("Processing complete. Separate CSV files have been created for each theme.")