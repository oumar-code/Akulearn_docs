import React, { useState, useEffect } from 'react';
import './RecommendationsComponent.css';

/**
 * Wave 3 Recommendations Component
 * React component for displaying personalized lesson recommendations
 * 
 * Props:
 *   - studentId: string (required)
 *   - method: 'content' | 'collaborative' | 'hybrid' | 'prerequisite' (default: 'hybrid')
 *   - limit: number (default: 5)
 *   - apiUrl: string (default: 'http://localhost:8000/api/v3')
 *   - token: string (optional)
 *   - onLessonClick: function (optional)
 */
const RecommendationsComponent = ({
  studentId,
  method = 'hybrid',
  limit = 5,
  apiUrl = 'http://localhost:8000/api/v3',
  token = null,
  onLessonClick = null,
  className = ''
}) => {
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedMethod, setSelectedMethod] = useState(method);

  useEffect(() => {
    fetchRecommendations();
  }, [studentId, selectedMethod, limit]);

  const fetchRecommendations = async () => {
    setLoading(true);
    setError(null);

    try {
      const headers = {
        'Content-Type': 'application/json',
        ...(token && { 'Authorization': `Bearer ${token}` })
      };

      const response = await fetch(
        `${apiUrl}/recommendations/${studentId}?method=${selectedMethod}&limit=${limit}`,
        { headers }
      );

      if (!response.ok) {
        throw new Error(`Failed to fetch recommendations: ${response.statusText}`);
      }

      const data = await response.json();
      setRecommendations(data.recommendations || []);
    } catch (err) {
      setError(err.message);
      console.error('Recommendations error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleLessonClick = async (recommendation) => {
    // Record interaction
    try {
      await fetch(`${apiUrl}/recommendations/interaction`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...(token && { 'Authorization': `Bearer ${token}` })
        },
        body: JSON.stringify({
          student_id: studentId,
          lesson_id: recommendation.lesson.id,
          interaction_type: 'click',
          metadata: { source: 'recommendations', method: selectedMethod }
        })
      });
    } catch (err) {
      console.error('Failed to record interaction:', err);
    }

    // Call custom handler if provided
    if (onLessonClick) {
      onLessonClick(recommendation.lesson);
    }
  };

  const getScoreColor = (score) => {
    if (score >= 0.8) return '#4CAF50';
    if (score >= 0.6) return '#FF9800';
    return '#FFC107';
  };

  const getMethodIcon = (methodType) => {
    const icons = {
      content: '📚',
      collaborative: '👥',
      hybrid: '🎯',
      prerequisite: '🔗'
    };
    return icons[methodType] || '📖';
  };

  const getMethodLabel = (methodType) => {
    const labels = {
      content: 'Similar Content',
      collaborative: 'Students Like You',
      hybrid: 'Best Match',
      prerequisite: 'Build Foundation'
    };
    return labels[methodType] || methodType;
  };

  if (loading) {
    return (
      <div className={`recommendations-container ${className}`}>
        <div className="recommendations-loading">
          <div className="spinner"></div>
          <p>Loading recommendations...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className={`recommendations-container ${className}`}>
        <div className="recommendations-error">
          <p>❌ {error}</p>
          <button onClick={fetchRecommendations}>Retry</button>
        </div>
      </div>
    );
  }

  return (
    <div className={`recommendations-container ${className}`}>
      {/* Header */}
      <div className="recommendations-header">
        <h2>
          {getMethodIcon(selectedMethod)} Recommended for You
        </h2>
        <p className="recommendations-subtitle">
          {getMethodLabel(selectedMethod)}
        </p>
      </div>

      {/* Method Selector */}
      <div className="method-selector">
        {['hybrid', 'content', 'collaborative', 'prerequisite'].map((m) => (
          <button
            key={m}
            className={`method-button ${selectedMethod === m ? 'active' : ''}`}
            onClick={() => setSelectedMethod(m)}
          >
            {getMethodIcon(m)} {m.charAt(0).toUpperCase() + m.slice(1)}
          </button>
        ))}
      </div>

      {/* Recommendations List */}
      {recommendations.length === 0 ? (
        <div className="recommendations-empty">
          <p>No recommendations available yet.</p>
          <p className="hint">Complete some lessons to get personalized recommendations!</p>
        </div>
      ) : (
        <div className="recommendations-list">
          {recommendations.map((rec, index) => (
            <div
              key={rec.lesson.id}
              className="recommendation-card"
              onClick={() => handleLessonClick(rec)}
            >
              {/* Rank Badge */}
              <div className="rank-badge">#{index + 1}</div>

              {/* Lesson Info */}
              <div className="lesson-info">
                <div className="lesson-subject">{rec.lesson.subject}</div>
                <h3 className="lesson-title">{rec.lesson.title}</h3>
                <p className="lesson-description">{rec.lesson.description}</p>

                {/* Meta Info */}
                <div className="lesson-meta">
                  <span className="meta-item">
                    ⏱️ {rec.lesson.duration_minutes} min
                  </span>
                  <span className="meta-item">
                    📊 {rec.lesson.difficulty_level}
                  </span>
                  <span className="meta-item">
                    📝 {rec.lesson.num_problems} problems
                  </span>
                </div>

                {/* Tags */}
                {rec.lesson.nerdc_codes && rec.lesson.nerdc_codes.length > 0 && (
                  <div className="lesson-tags">
                    {rec.lesson.nerdc_codes.slice(0, 3).map((code, i) => (
                      <span key={i} className="tag">{code}</span>
                    ))}
                  </div>
                )}
              </div>

              {/* Match Score */}
              <div className="match-score">
                <div className="score-circle">
                  <svg width="80" height="80">
                    <circle
                      cx="40"
                      cy="40"
                      r="35"
                      fill="none"
                      stroke="#e0e0e0"
                      strokeWidth="6"
                    />
                    <circle
                      cx="40"
                      cy="40"
                      r="35"
                      fill="none"
                      stroke={getScoreColor(rec.score)}
                      strokeWidth="6"
                      strokeDasharray={`${rec.score * 220} 220`}
                      strokeLinecap="round"
                      transform="rotate(-90 40 40)"
                    />
                    <text
                      x="40"
                      y="45"
                      textAnchor="middle"
                      fontSize="18"
                      fontWeight="bold"
                      fill={getScoreColor(rec.score)}
                    >
                      {Math.round(rec.score * 100)}%
                    </text>
                  </svg>
                </div>
                <div className="score-label">Match</div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Refresh Button */}
      <button className="refresh-button" onClick={fetchRecommendations}>
        🔄 Refresh Recommendations
      </button>
    </div>
  );
};

export default RecommendationsComponent;

// Example Usage:
/*
import RecommendationsComponent from './components/RecommendationsComponent';

function App() {
  const handleLessonClick = (lesson) => {
    console.log('Lesson clicked:', lesson);
    // Navigate to lesson detail page
    history.push(`/lessons/${lesson.id}`);
  };

  return (
    <div className="app">
      <RecommendationsComponent
        studentId="student_001"
        method="hybrid"
        limit={5}
        apiUrl="http://localhost:8000/api/v3"
        token={userToken}
        onLessonClick={handleLessonClick}
      />
    </div>
  );
}
*/
