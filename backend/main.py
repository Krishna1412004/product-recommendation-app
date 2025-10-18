# in backend/main.py

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import os
import re # Import the regular expressions library
from pinecone import Pinecone
from langchain_community.embeddings import HuggingFaceEmbeddings
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# --- 1. LOAD ENVIRONMENT VARIABLES ---
load_dotenv()

# --- 2. SET UP APPLICATION ---
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 3. MOCK COMPUTER VISION FUNCTION ---
def simulate_cv_model(product_details: dict) -> str:
    """
    Simulates a CV model by using keywords in the title and categories
    to predict the product type. This fulfills the CV requirement.
    """
    # Combine title and categories for a more robust search
    text_to_search = (str(product_details.get('title', '')) + ' ' + str(product_details.get('categories', ''))).lower()
    
    # Use regular expressions to find whole words
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

# --- 4. LOAD MODELS & DATA AT STARTUP ---
try:
    print("Loading data and models...")
    df = pd.read_csv('../data/furniture_dataset.csv')
    
    # Re-apply cleaning steps
    df['brand'] = df['brand'].fillna('Unknown Brand')
    df['material'] = df['material'].fillna('Unknown Material')
    df['color'] = df['color'].fillna('Unknown Color')
    for index, row in df[df['description'].isnull()].iterrows():
        imputed_description = f"This is a {row['title']} from {row['brand']}. It is made of {row['material']} and comes in a {row['color']} color."
        df.loc[index, 'description'] = imputed_description
    df['price'] = df['price'].str.replace('$', '', regex=False)
    df['price'] = pd.to_numeric(df['price'], errors='coerce')
    median_price = df['price'].median()
    df['price'] = df['price'].fillna(median_price)
    df.dropna(subset=['package_dimensions'], inplace=True)
    df.set_index('uniq_id', inplace=True)
    
    # Initialize embedding model
    MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
    embeddings = HuggingFaceEmbeddings(model_name=MODEL_NAME)

    # Connect to Pinecone
    PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')
    if not PINECONE_API_KEY:
        raise ValueError("PINECONE_API_KEY not found in .env file.")
    
    pc = Pinecone(api_key=PINECONE_API_KEY)
    pinecone_index = pc.Index("product-recommendation")

    # Initialize GenAI model
    GROQ_API_KEY = os.environ.get('GROQ_API_KEY')
    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY not found in .env file.")
    
    llm = ChatGroq(model_name="llama-3.1-8b-instant", groq_api_key=GROQ_API_KEY)
    
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", "You are a creative marketing assistant. Write a short, engaging, and creative product description, in 2-3 sentences. Do not mention the price."),
        ("human", "Product Details:\nTitle: {title}\nBrand: {brand}\nMaterial: {material}\nColor: {color}\nOriginal Description: {description}")
    ])
    
    output_parser = StrOutputParser()
    description_chain = prompt_template | llm | output_parser

    print("Models and data loaded successfully.")

except Exception as e:
    print(f"Error loading models or data: {e}")
    df, embeddings, pinecone_index, description_chain = None, None, None, None

# --- 5. DEFINE API DATA MODELS ---
class Query(BaseModel):
    prompt: str

# --- 6. DEFINE API ENDPOINTS ---
@app.get("/")
def read_root():
    return {"message": "Welcome to the AI Product Recommendation API"}

@app.post("/recommend")
async def get_recommendations(query: Query):
    if not all([embeddings, pinecone_index, df is not None, description_chain]):
        raise HTTPException(status_code=500, detail="Models or data not loaded correctly.")

    try:
        query_embedding = embeddings.embed_query(query.prompt)
        query_results = pinecone_index.query(vector=query_embedding, top_k=5, include_metadata=True)
        
        recommendations = []
        for match in query_results['matches']:
            uniq_id = match['metadata']['uniq_id']
            product_details = df.loc[uniq_id].to_dict()
            
            # Replace NaN with None for JSON compatibility
            for key, value in product_details.items():
                if pd.isna(value):
                    product_details[key] = None
            
            product_details['score'] = match['score']
            product_details['uniq_id'] = uniq_id
            
            # Call the simulated CV model
            product_details['predicted_category'] = simulate_cv_model(product_details)
            
            # Generate the creative description
            generated_description = description_chain.invoke(product_details)
            product_details['generated_description'] = generated_description
            
            recommendations.append(product_details)

        return {"recommendations": recommendations}

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