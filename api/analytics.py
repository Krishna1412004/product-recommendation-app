from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up application
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load data (lightweight)
try:
    print("Loading data...")
    df = pd.read_csv('data/furniture_dataset.csv')
    
    # Basic cleaning
    df['brand'] = df['brand'].fillna('Unknown Brand')
    df['material'] = df['material'].fillna('Unknown Material')
    df['color'] = df['color'].fillna('Unknown Color')
    df['price'] = df['price'].str.replace('$', '', regex=False)
    df['price'] = pd.to_numeric(df['price'], errors='coerce')
    median_price = df['price'].median()
    df['price'] = df['price'].fillna(median_price)
    df.dropna(subset=['package_dimensions'], inplace=True)
    df.set_index('uniq_id', inplace=True)
    
    print("Data loaded successfully.")
except Exception as e:
    print(f"Error loading data: {e}")
    df = None

@app.get("/analytics")
async def get_analytics():
    if df is None:
        raise HTTPException(status_code=500, detail="Data not loaded correctly.")

    try:
        brand_counts = df['brand'].value_counts().head(10).to_dict()
        material_counts = df['material'].value_counts().head(10).to_dict()
        price_stats = df['price'].describe().to_dict()

        return {
            "brand_counts": brand_counts,
            "material_counts": material_counts,
            "price_stats": price_stats
        }

    except Exception as e:
        print(f"An error occurred during analytics calculation: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate analytics.")

# Vercel handler
def handler(request):
    return app(request.scope, request.receive, request.send)
