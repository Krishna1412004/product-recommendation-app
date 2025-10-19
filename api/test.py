from fastapi import FastAPI
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

@app.get("/test")
def test_endpoint():
    return {"message": "Backend is working!", "data_loaded": df is not None}

# Vercel handler
def handler(request):
    return app(request.scope, request.receive, request.send)
