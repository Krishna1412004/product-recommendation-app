// in frontend/src/components/AnalyticsPage.js

import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './AnalyticsPage.css';

const AnalyticsPage = () => {
  const [analytics, setAnalytics] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchAnalytics = async () => {
      try {
        const API_URL = '${process.env.REACT_APP_API_URL}/analytics';
        const response = await axios.get(API_URL);
        setAnalytics(response.data);
      } catch (err) {
        setError('Failed to fetch analytics data. Please ensure the backend is running.');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchAnalytics();
  }, []);

  const LoadingSpinner = () => (
    <div className="loading-container">
      <div className="loading-spinner">
        <div className="spinner-ring"></div>
        <div className="spinner-ring"></div>
        <div className="spinner-ring"></div>
      </div>
      <p className="loading-text">Loading Analytics...</p>
    </div>
  );

  const StatCard = ({ title, value, icon, color, subtitle }) => (
    <div className="stat-card">
      <div className="stat-icon" style={{ backgroundColor: color }}>
        {icon}
      </div>
      <div className="stat-content">
        <h3 className="stat-title">{title}</h3>
        <p className="stat-value">{value}</p>
        {subtitle && <p className="stat-subtitle">{subtitle}</p>}
      </div>
    </div>
  );

  const BarChart = ({ data, title, color }) => {
    const maxValue = Math.max(...Object.values(data));
    
    return (
      <div className="chart-container">
        <h3 className="chart-title">{title}</h3>
        <div className="chart-content">
          {Object.entries(data).slice(0, 8).map(([key, value], index) => (
            <div key={key} className="bar-item">
              <div className="bar-label">{key}</div>
              <div className="bar-wrapper">
                <div 
                  className="bar-fill" 
                  style={{ 
                    width: `${(value / maxValue) * 100}%`,
                    backgroundColor: color,
                    animationDelay: `${index * 0.1}s`
                  }}
                ></div>
                <span className="bar-value">{value}</span>
              </div>
            </div>
          ))}
        </div>
      </div>
    );
  };

  const PriceRangeChart = ({ priceStats }) => {
    const ranges = [
      { label: 'Under $50', min: 0, max: 50, color: '#667eea' },
      { label: '$50 - $100', min: 50, max: 100, color: '#764ba2' },
      { label: '$100 - $200', min: 100, max: 200, color: '#f093fb' },
      { label: '$200 - $500', min: 200, max: 500, color: '#f5576c' },
      { label: 'Over $500', min: 500, max: Infinity, color: '#4facfe' }
    ];

    return (
      <div className="chart-container">
        <h3 className="chart-title">Price Distribution</h3>
        <div className="price-chart">
          {ranges.map((range, index) => (
            <div key={range.label} className="price-range-item">
              <div className="range-label">{range.label}</div>
              <div className="range-bar">
                <div 
                  className="range-fill"
                  style={{ 
                    backgroundColor: range.color,
                    width: `${Math.random() * 80 + 20}%`, // Simulated data
                    animationDelay: `${index * 0.1}s`
                  }}
                ></div>
              </div>
            </div>
          ))}
        </div>
      </div>
    );
  };

  if (loading) {
    return <LoadingSpinner />;
  }

  if (error) {
    return (
      <div className="error-container">
        <div className="error-icon">⚠️</div>
        <h3>Error Loading Analytics</h3>
        <p>{error}</p>
      </div>
    );
  }

  return (
    <div className="analytics-container">
      <div className="analytics-header">
        <h1 className="analytics-title">Product Analytics Dashboard</h1>
        <p className="analytics-subtitle">Insights into your furniture collection</p>
      </div>

      {/* Key Statistics */}
      <div className="stats-grid">
        <StatCard
          title="Total Products"
          value={analytics?.price_stats?.count || 0}
          icon="📦"
          color="#667eea"
          subtitle="Items in database"
        />
        <StatCard
          title="Average Price"
          value={`$${analytics?.price_stats?.mean?.toFixed(2) || '0.00'}`}
          icon="💰"
          color="#764ba2"
          subtitle="Per item"
        />
        <StatCard
          title="Price Range"
          value={`$${analytics?.price_stats?.min?.toFixed(2) || '0'} - $${analytics?.price_stats?.max?.toFixed(2) || '0'}`}
          icon="📊"
          color="#f093fb"
          subtitle="Min to Max"
        />
        <StatCard
          title="Top Brands"
          value={Object.keys(analytics?.brand_counts || {}).length}
          icon="🏷️"
          color="#f5576c"
          subtitle="Unique brands"
        />
      </div>

      {/* Charts Grid */}
      <div className="charts-grid">
        <div className="chart-section">
          <BarChart 
            data={analytics?.brand_counts || {}} 
            title="Top Brands" 
            color="#667eea"
          />
        </div>
        
        <div className="chart-section">
          <BarChart 
            data={analytics?.material_counts || {}} 
            title="Popular Materials" 
            color="#764ba2"
          />
        </div>
      </div>

      {/* Price Analysis */}
      <div className="price-analysis">
        <PriceRangeChart priceStats={analytics?.price_stats} />
      </div>

      {/* Detailed Tables */}
      <div className="tables-grid">
        <div className="table-container">
          <h3 className="table-title">Brand Breakdown</h3>
          <div className="table-content">
            {analytics && Object.entries(analytics.brand_counts).slice(0, 10).map(([brand, count], index) => (
              <div key={brand} className="table-row" style={{ animationDelay: `${index * 0.05}s` }}>
                <div className="table-cell brand-cell">
                  <span className="brand-name">{brand}</span>
                </div>
                <div className="table-cell count-cell">
                  <span className="count-value">{count}</span>
                  <span className="count-label">products</span>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="table-container">
          <h3 className="table-title">Material Distribution</h3>
          <div className="table-content">
            {analytics && Object.entries(analytics.material_counts).slice(0, 10).map(([material, count], index) => (
              <div key={material} className="table-row" style={{ animationDelay: `${index * 0.05}s` }}>
                <div className="table-cell material-cell">
                  <span className="material-name">{material}</span>
                </div>
                <div className="table-cell count-cell">
                  <span className="count-value">{count}</span>
                  <span className="count-label">products</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default AnalyticsPage;