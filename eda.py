import pandas as pd
import matplotlib.pyplot as plt
import os

def run_eda(csv_path):
    # Check if file exists
    if not os.path.exists(csv_path):
        print(f"❌ File not found: {csv_path}")
        return

    # Load data
    print(f"📂 Reading data from: {csv_path}")
    df = pd.read_csv(csv_path)

    print(f"✅ Data loaded successfully. Total rows: {len(df)}")
    print("Columns in dataset:", df.columns.tolist())
    print("\nMissing values per column:")
    print(df.isna().sum())

    # Create charts folder if not exists
    os.makedirs("eda/charts", exist_ok=True)

    # ---- 1️⃣ Price Distribution ----
    if "price_min" in df.columns:
        df["price_min"].dropna().plot(kind="hist", bins=20, alpha=0.7)
        plt.title("Price Distribution (price_min)")
        plt.xlabel("Price")
        plt.tight_layout()
        plt.savefig("eda/charts/price_distribution.png")
        plt.clf()
        print("📊 Saved: price_distribution.png")
    else:
        print("⚠️ No 'price_min' column found, skipping price distribution.")

    # ---- 2️⃣ Top Supplier Locations ----
    if "location" in df.columns:
        loc_counts = df["location"].dropna().value_counts().head(10)
        if not loc_counts.empty:
            loc_counts.plot(kind="bar")
            plt.title("Top 10 Supplier Locations")
            plt.tight_layout()
            plt.savefig("eda/charts/top_locations.png")
            plt.clf()
            print("📊 Saved: top_locations.png")
        else:
            print("⚠️ No location data available for plotting.")
    else:
        print("⚠️ No 'location' column found, skipping location plot.")

    # ---- 3️⃣ Missing Data Overview ----
    df.isnull().sum().plot(kind="bar")
    plt.title("Missing Values per Column")
    plt.tight_layout()
    plt.savefig("eda/charts/missing_values.png")
    plt.clf()
    print("📊 Saved: missing_values.png")

    print("\n✅ EDA completed successfully. Charts saved in: eda/charts/")

if __name__ == "__main__":
    # Example usage (edit your CSV file name below)
    csv_path = "sample_output/products.csv"
    run_eda(csv_path)
