// in frontend/src/components/RecommendationPage.js

import React, { useState } from 'react';
import axios from 'axios';
import './RecommendationPage.css';

const RecommendationPage = () => {
  const [prompt, setPrompt] = useState('');
  const [recommendations, setRecommendations] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [hasSearched, setHasSearched] = useState(false);

  // 🔹 Helper function to parse image string
  const getFirstImage = (imagesString) => {
    if (!imagesString) return '';
    try {
      // Convert stringified Python list to valid JSON
      const urls = JSON.parse(
        imagesString
          .replace(/'/g, '"') // replace single quotes with double quotes
          .replace(/\s+/g, '') // remove extra spaces
      );
      return urls[0] || '';
    } catch (e) {
      console.error('Error parsing image string:', imagesString);
      return '';
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!prompt.trim()) {
      setError('Please enter a description.');
      return;
    }

    setIsLoading(true);
    setError('');
    setRecommendations([]);
    setHasSearched(true);

    try {
      const API_URL = 'http://127.0.0.1:8000/recommend';
      const response = await axios.post(API_URL, { prompt });
      setRecommendations(response.data.recommendations);
    } catch (err) {
      setError('Failed to fetch recommendations. Please ensure the backend is running.');
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  const LoadingSpinner = () => (
    <div className="loading-container">
      <div className="loading-spinner">
        <div className="spinner-ring"></div>
        <div className="spinner-ring"></div>
        <div className="spinner-ring"></div>
      </div>
      <p className="loading-text">Finding your perfect furniture...</p>
    </div>
  );

  const EmptyState = () => (
    <div className="empty-state">
      <div className="empty-icon">🔍</div>
      <h3>Discover Amazing Furniture</h3>
      <p>Describe what you're looking for and let our AI find the perfect pieces for your space.</p>
      <div className="example-prompts">
        <span className="example-tag">Modern leather sofa</span>
        <span className="example-tag">Wooden dining table</span>
        <span className="example-tag">Minimalist bookshelf</span>
        <span className="example-tag">Comfortable office chair</span>
      </div>
    </div>
  );

  return (
    <div className="recommendation-container">
      <div className="hero-section">
        <h1 className="hero-title">Find Your Perfect Furniture</h1>
        <p className="hero-subtitle">
          Describe what you're looking for, and our AI will find the best matches for you.
        </p>
      </div>

      <form onSubmit={handleSubmit} className="search-form">
        <div className="search-input-container">
          <input
            type="text"
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            placeholder="e.g., a modern leather sofa for a small apartment"
            className="search-input"
            disabled={isLoading}
          />
          <button type="submit" className="search-button" disabled={isLoading || !prompt.trim()}>
            {isLoading ? (
              <div className="button-spinner"></div>
            ) : (
              <>
                <span className="button-icon">🔍</span>
                Find Furniture
              </>
            )}
          </button>
        </div>
      </form>

      {error && (
        <div className="error-message">
          <span className="error-icon">⚠️</span>
          {error}
        </div>
      )}

      <div className="results-section">
        {isLoading ? (
          <LoadingSpinner />
        ) : !hasSearched ? (
          <EmptyState />
        ) : recommendations.length > 0 ? (
          <>
            <div className="results-header">
              <h2>Found {recommendations.length} Perfect Matches</h2>
              <p>Based on your search: "{prompt}"</p>
            </div>
            <div className="results-grid">
              {recommendations.map((item, index) => (
                <div 
                  key={item.uniq_id} 
                  className="product-card"
                  style={{ animationDelay: `${index * 0.1}s` }}
                >
                  <div className="product-image-container">
                    <img
                      src={getFirstImage(item.images)}
                      alt={item.title}
                      className="product-image"
                      onError={(event) => {
                        event.target.src = 'https://placehold.co/600x400/eee/ccc?text=Image+Not+Available';
                        event.onerror = null;
                      }}
                    />
                    <div className="product-category-tag">{item.predicted_category}</div>
                    <div className="product-score">
                      {Math.round(item.score * 100)}% match
                    </div>
                  </div>
                  <div className="product-info">
                    <h3 className="product-title">{item.title}</h3>
                    <p className="product-brand">by {item.brand}</p>
                    <p className="product-description">{item.generated_description}</p>
                    <div className="product-footer">
                      <p className="product-price">
                        {typeof item.price === 'number'
                          ? `$${item.price.toFixed(2)}`
                          : 'Price not available'}
                      </p>
                      <div className="product-specs">
                        <span className="spec-item">
                          <span className="spec-icon">🎨</span>
                          {item.color}
                        </span>
                        <span className="spec-item">
                          <span className="spec-icon">🪵</span>
                          {item.material}
                        </span>
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </>
        ) : (
          <div className="no-results">
            <div className="no-results-icon">😔</div>
            <h3>No Results Found</h3>
            <p>Try adjusting your search terms or be more specific about what you're looking for.</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default RecommendationPage;
