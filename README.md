# B2B-scraper-Data-Collection-mini-project
# Step 1: Get all project files
# Step 2 Take all the .py files and folders from your repository (crawler/, etl/, eda/) and your requirements.txt.
# Step 3 Copy them to a folder on your local system. Example:C:\Users\YourName\Desktop\b2b-scraper\
 
# Step 4: Open the folder in VS Code
# Step 5: Open VS Code.
# Step 6: Click File → Open Folder, and select the folder you just created (b2b-scraper).
# Step 7: YOU SEE All your .py files should appear in the Explorer panel.

# Step 8: Install Python dependencies
# Step 9: Open a Terminal in VS Code: Terminal → New Terminal.
# Step 10: Make sure you are in the root folder (b2b-scraper) in the terminal.
    Step 10.1: Create the virtual environment: "python -m venv venv"
    Step 10.2: Activate the virtual environment: "venv\Scripts\activate" on Windows
    Step 10.3: You should see "(venv)" in the terminal prompt
# Step 11: then Run this command to install all required libraries: "pip install -r requirements.txt"

# Step 12: Run the Crawler (Data Collection)
# Step 13: In the VS Code terminal, then run: "python -m crawler.async_crawler"
# Step 14: The crawler will start collecting product data from IndiaMART.
# Step 15: Wait until it finishes — you’ll see OUTPUT like:
                                              INFO:root:Saved: Soldering Iron 60W
                                              INFO:root:Saved: Mini Soldering Station

# Step16: Output files will be created here: OUTPUT SEE HERE sample_output/products.csv
                                           OUTPUT SEE HERE sample_output/products.jsonl

# Step 17: Run the EDA (Exploratory Data Analysis)
# Step 18: After the crawler finishes, then run: python -m eda.eda

# Step 19: he script will analyze the CSV data and generate charts:eda/charts/price_distribution.png
                                                        eda/charts/top_locations.png
                                                        eda/charts/missing_values.png
# Step 20: Check the Output
# Step 21: Open sample_output/products.csv to see all collected product data.
# Step 22: Open the charts in eda/charts/ to understand trends, top suppliers, price distribution, and missing values.
