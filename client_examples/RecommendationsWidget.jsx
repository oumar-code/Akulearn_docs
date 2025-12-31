import React, { useState, useEffect } from 'react';
import './RecommendationsWidget.css';

/**
 * Wave 3 Recommendations Component
 * Displays personalized lesson recommendations with scores
 */
const RecommendationsWidget = ({
  studentId,
  method = 'hybrid',
  limit = 5,
  apiUrl = 'http://localhost:8000/api/v3',
  token = null,
  onLessonClick = null,
  showScores = true,
  autoRefresh = false,
  refreshInterval = 60000, // 1 minute
}) => {
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedMethod, setSelectedMethod] = useState(method);

  useEffect(() => {
    fetchRecommendations();

    if (autoRefresh) {
      const intervalId = setInterval(fetchRecommendations, refreshInterval);
      return () => clearInterval(intervalId);
    }
  }, [studentId, selectedMethod, limit]);

  const fetchRecommendations = async () => {
    setLoading(true);
    setError(null);

    try {
      const params = new URLSearchParams({
        method: selectedMethod,
        limit: limit.toString(),
      });

      const headers = {};
      if (token) {
        headers['Authorization'] = `Bearer ${token}`;
      }

      const response = await fetch(
        `${apiUrl}/recommendations/${studentId}?${params.toString()}`,
        { headers }
      );

      if (!response.ok) {
        throw new Error(`Failed to fetch recommendations: ${response.statusText}`);
      }

      const data = await response.json();
      setRecommendations(data.recommendations || []);
    } catch (err) {
      console.error('Error fetching recommendations:', err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleLessonClick = async (recommendation) => {
    // Record interaction
    try {
      const headers = { 'Content-Type': 'application/json' };
      if (token) {
        headers['Authorization'] = `Bearer ${token}`;
      }

      await fetch(`${apiUrl}/recommendations/interaction`, {
        method: 'POST',
        headers,
        body: JSON.stringify({
          student_id: studentId,
          lesson_id: recommendation.lesson.id,
          interaction_type: 'click',
          metadata: {
            source: 'recommendations_widget',
            recommendation_method: selectedMethod,
            score: recommendation.score,
          },
        }),
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
    if (score >= 0.6) return '#2196F3';
    if (score >= 0.4) return '#FF9800';
    return '#9E9E9E';
  };

  const getDifficultyColor = (level) => {
    const colors = {
      Beginner: '#4CAF50',
      Intermediate: '#2196F3',
      Advanced: '#FF9800',
      Expert: '#F44336',
    };
    return colors[level] || '#9E9E9E';
  };

  if (loading && recommendations.length === 0) {
    return (
      <div className="recommendations-widget loading">
        <div className="spinner"></div>
        <p>Loading recommendations...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="recommendations-widget error">
        <div className="error-icon">⚠️</div>
        <h3>Failed to load recommendations</h3>
        <p>{error}</p>
        <button onClick={fetchRecommendations} className="retry-button">
          Retry
        </button>
      </div>
    );
  }

  if (recommendations.length === 0) {
    return (
      <div className="recommendations-widget empty">
        <div className="empty-icon">📚</div>
        <h3>No recommendations available</h3>
        <p>Start learning to get personalized recommendations!</p>
      </div>
    );
  }

  return (
    <div className="recommendations-widget">
      <div className="widget-header">
        <h2>Recommended for You</h2>
        <div className="method-selector">
          <button
            className={selectedMethod === 'content' ? 'active' : ''}
            onClick={() => setSelectedMethod('content')}
            title="Based on lesson content similarity"
          >
            Content
          </button>
          <button
            className={selectedMethod === 'collaborative' ? 'active' : ''}
            onClick={() => setSelectedMethod('collaborative')}
            title="Based on similar students"
          >
            Collaborative
          </button>
          <button
            className={selectedMethod === 'hybrid' ? 'active' : ''}
            onClick={() => setSelectedMethod('hybrid')}
            title="Best of both methods"
          >
            Hybrid
          </button>
        </div>
      </div>

      <div className="recommendations-list">
        {recommendations.map((rec, index) => (
          <div
            key={rec.lesson.id}
            className="recommendation-card"
            onClick={() => handleLessonClick(rec)}
          >
            <div className="card-rank">#{index + 1}</div>
            
            <div className="card-content">
              <div className="card-header">
                <h3 className="lesson-title">{rec.lesson.title}</h3>
                <span
                  className="difficulty-badge"
                  style={{ backgroundColor: getDifficultyColor(rec.lesson.difficulty_level) }}
                >
                  {rec.lesson.difficulty_level}
                </span>
              </div>

              <p className="lesson-subject">{rec.lesson.subject}</p>
              <p className="lesson-description">{rec.lesson.description}</p>

              <div className="lesson-meta">
                <span className="meta-item">
                  ⏱️ {rec.lesson.duration_minutes} min
                </span>
                <span className="meta-item">
                  📚 {rec.lesson.num_objectives} objectives
                </span>
                <span className="meta-item">
                  📝 {rec.lesson.num_problems} problems
                </span>
              </div>

              {rec.reason && (
                <div className="recommendation-reason">
                  <span className="reason-icon">💡</span>
                  {rec.reason}
                </div>
              )}

              {showScores && (
                <div className="score-bar">
                  <span className="score-label">Match</span>
                  <div className="score-fill-container">
                    <div
                      className="score-fill"
                      style={{
                        width: `${rec.score * 100}%`,
                        backgroundColor: getScoreColor(rec.score),
                      }}
                    ></div>
                  </div>
                  <span
                    className="score-value"
                    style={{ color: getScoreColor(rec.score) }}
                  >
                    {Math.round(rec.score * 100)}%
                  </span>
                </div>
              )}
            </div>
          </div>
        ))}
      </div>

      <div className="widget-footer">
        <button onClick={fetchRecommendations} className="refresh-button">
          🔄 Refresh
        </button>
      </div>
    </div>
  );
};

export default RecommendationsWidget;
