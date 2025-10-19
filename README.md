# AI Furniture Recommendation & Analytics App

This project is a full-stack web application built over two days that uses multiple AI domains (ML, NLP, GenAI, and simulated CV) to provide furniture recommendations and display product analytics. It was developed to demonstrate skills in integrating advanced AI with full-stack development.

---

## Features

* **AI-Powered Recommendations**: Users can describe the furniture they want in a conversational manner, and the app provides semantically similar products using text embeddings and a vector database.
* **Generative Descriptions**: Each recommended product comes with a unique, AI-generated creative description using Groq's `llama-3.1-8b-instant` model, orchestrated via LangChain.
* **Product Analytics**: A dedicated page shows key metrics about the product dataset, such as top brands, top materials, and price distribution statistics.
* **Simulated Computer Vision**: A mock CV model predicts the product category (e.g., "Seating", "Storage") based on keywords in the product's text data, fulfilling the CV requirement.

---

## Tech Stack

* **Backend**: FastAPI
* **Frontend**: React
* **Vector Database**: Pinecone
* **AI Integration**: LangChain
* **AI Models**:
    * **Embeddings (NLP)**: `sentence-transformers/all-MiniLM-L6-v2` via HuggingFace
    * **Generative AI (GenAI)**: `llama-3.1-8b-instant` via Groq API

---

## Setup and Installation

### Prerequisites

* Python 3.10+
* Node.js and npm
* A Pinecone API Key
* A Groq API Key

### 1. Clone the Repository

```bash
git clone [https://github.com/Krishna1412004/product-recommendation-app.git](https://github.com/Krishna1412004/product-recommendation-app.git)
cd product-recommendation-app

```
### 2. Backend Setup

```bash
# Navigate to the backend folder
cd backend

# Create and activate a virtual environment
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate

# Install dependencies from the requirements file
pip install -r requirements.txt

# Create a .env file
# In the backend/ directory, create a new file named .env and add your API keys:
# PINECONE_API_KEY="your_pinecone_api_key_here"
# GROQ_API_KEY="your_groq_api_key_here"
```
### 3. Frontend Setup

```bash
# Navigate to the frontend folder from the root directory
cd frontend

# Install dependencies
npm install
```
---

## How to Run the Application

You will need two separate terminals to run the application.

### 1. Run the Backend Server

* **Terminal 1:** Navigate to the `backend/` directory and ensure your virtual environment is active.
* Run the FastAPI server:

    ```bash
    uvicorn main:app --reload
    ```
* The backend will be running at `http://127.0.0.1:8000`.

### 2. Run the Frontend App

* **Terminal 2:** Navigate to the `frontend/` directory.
* Start the React development server:

    ```bash
    npm start
    ```
* The application will open automatically in your browser at `http://localhost:3000`.
  ---

## Project Deliverables

This repository contains all the required deliverables:

1.  **Frontend (React App)** in the `/frontend` directory.
2.  **Backend (FastAPI App)** in the `/backend` directory.
3.  **Data Analytics Notebook** (`Data_Analytics.ipynb`) in the `/notebooks` directory.
4.  **Model Training Notebook** (`Model_Training.ipynb`) in the `/notebooks` directory.
5.  **This README.md file** with detailed setup and usage instructions.
