# MAQ Software - Furniture Recommendation App Deployment Guide

## Overview
This is a React + FastAPI application deployed on Vercel. The frontend serves the React app, while the backend runs FastAPI with AI/ML models for furniture recommendations.

## Project Structure
```
maq_software/
├── frontend/          # React application
├── backend/           # FastAPI application
├── data/              # Dataset files
├── vercel.json        # Vercel deployment configuration
└── README.md
```

## Prerequisites
1. Vercel account
2. Pinecone account (for vector database)
3. Groq account (for AI model)

## Environment Variables Setup

### Required Environment Variables
You need to set these in your Vercel project settings:

1. **PINECONE_API_KEY**: Your Pinecone API key
2. **GROQ_API_KEY**: Your Groq API key

### How to Set Environment Variables in Vercel:
1. Go to your Vercel dashboard
2. Select your project
3. Go to Settings → Environment Variables
4. Add the following variables:
   - `PINECONE_API_KEY`: Your Pinecone API key
   - `GROQ_API_KEY`: Your Groq API key

## Deployment Steps

### 1. Prepare Your Repository
Make sure your code is pushed to GitHub/GitLab/Bitbucket.

### 2. Connect to Vercel
1. Go to [vercel.com](https://vercel.com)
2. Click "New Project"
3. Import your repository
4. Vercel will automatically detect the configuration from `vercel.json`

### 3. Configure Build Settings
Vercel will automatically:
- Build the React frontend from `frontend/` directory
- Deploy the FastAPI backend from `backend/main.py`
- Route API calls to `/api/*` to the backend
- Serve the React app for all other routes

### 4. Set Environment Variables
Add your environment variables in Vercel dashboard:
- `PINECONE_API_KEY`
- `GROQ_API_KEY`

### 5. Deploy
Click "Deploy" and wait for the build to complete.

## API Endpoints

Once deployed, your API will be available at:
- `https://your-app.vercel.app/api/recommend` - POST endpoint for furniture recommendations
- `https://your-app.vercel.app/api/analytics` - GET endpoint for analytics data

## Troubleshooting

### Common Issues:

1. **Build Failures**:
   - Check that all dependencies are in `requirements.txt`
   - Ensure Python version compatibility
   - Check Vercel logs for specific errors

2. **API Not Working**:
   - Verify environment variables are set correctly
   - Check CORS settings
   - Ensure Pinecone and Groq API keys are valid

3. **Frontend Not Loading**:
   - Check that React build completed successfully
   - Verify routing configuration in `vercel.json`

### Vercel Function Limits:
- Maximum execution time: 10 seconds (Hobby plan) / 60 seconds (Pro plan)
- Maximum memory: 1024 MB
- Maximum payload size: 4.5 MB

## Local Development

To run locally:
1. Backend: `cd backend && uvicorn main:app --reload`
2. Frontend: `cd frontend && npm start`

## Production Considerations

1. **Performance**: The ML models may take time to load on cold starts
2. **Scaling**: Consider upgrading to Vercel Pro for better performance
3. **Monitoring**: Use Vercel Analytics to monitor performance
4. **Security**: Consider restricting CORS origins in production

## Support

If you encounter issues:
1. Check Vercel deployment logs
2. Verify environment variables
3. Test API endpoints individually
4. Check browser console for frontend errors
