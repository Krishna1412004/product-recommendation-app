# Simplified backend for Vercel deployment
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import os
import re
import httpx
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

# Mock CV function (same as before)
def simulate_cv_model(product_details: dict) -> str:
    text_to_search = (str(product_details.get('title', '')) + ' ' + str(product_details.get('categories', ''))).lower()
    
    if re.search(r'\b(chair|sofa|couch|stool|ottoman)\b', text_to_search):
        return 'Seating'
    if re.search(r'\b(table|desk|stand)\b', text_to_search):
        return 'Table / Stand'
    if re.search(r'\b(rack|shelf|organizer|storage)\b', text_to_search):
        return 'Storage / Organizer'
    if re.search(r'\b(mat|rug|doormat)\b', text_to_search):
        return 'Mat / Rug'
    if re.search(r'\b(lamp|light)\b', text_to_search):
        return 'Lighting'
        
    return 'Miscellaneous'

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

# API Models
class Query(BaseModel):
    prompt: str

# API Endpoints
@app.get("/")
def read_root():
    return {"message": "Welcome to the AI Product Recommendation API"}

@app.post("/recommend")
async def get_recommendations(query: Query):
    if df is None:
        raise HTTPException(status_code=500, detail="Data not loaded correctly.")

    try:
        # Simple keyword-based search instead of ML
        search_terms = query.prompt.lower().split()
        recommendations = []
        
        for idx, row in df.iterrows():
            score = 0
            product_text = f"{row['title']} {row['brand']} {row['material']} {row['color']}".lower()
            
            for term in search_terms:
                if term in product_text:
                    score += 1
            
            if score > 0:
                product_details = row.to_dict()
                for key, value in product_details.items():
                    if pd.isna(value):
                        product_details[key] = None
                
                product_details['score'] = score / len(search_terms)
                product_details['uniq_id'] = idx
                product_details['predicted_category'] = simulate_cv_model(product_details)
                product_details['generated_description'] = f"This is a {row['title']} from {row['brand']}. It features {row['material']} construction in {row['color']} color."
                
                recommendations.append(product_details)
        
        # Sort by score and return top 5
        recommendations.sort(key=lambda x: x['score'], reverse=True)
        return {"recommendations": recommendations[:5]}

    except Exception as e:
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve recommendations.")

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
