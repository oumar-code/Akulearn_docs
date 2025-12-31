/**
 * Wave 3 Analytics Dashboard Widgets
 * Comprehensive analytics widgets for web and mobile
 */

import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  Dimensions,
  ScrollView,
  TouchableOpacity,
  ActivityIndicator,
} from 'react-native';

// For web, you can use react-chartjs-2 or recharts
// For mobile, use react-native-svg and react-native-chart-kit

const { width } = Dimensions.get('window');

// ============================================================================
// API Hook
// ============================================================================

const useAnalyticsAPI = (studentId, token = null) => {
  const BASE_URL = 'http://localhost:8000/api/v3';

  const fetchData = async (endpoint) => {
    try {
      const response = await fetch(`${BASE_URL}${endpoint}`, {
        headers: {
          ...(token && { Authorization: `Bearer ${token}` }),
        },
      });
      if (!response.ok) throw new Error('Failed to fetch');
      return await response.json();
    } catch (error) {
      console.error(`API Error (${endpoint}):`, error);
      throw error;
    }
  };

  return {
    predictMastery: (lessonId) =>
      fetchData(`/analytics/predict-mastery/${studentId}/${lessonId}`),
    getStudyRecommendation: () =>
      fetchData(`/analytics/study-recommendation/${studentId}`),
    getLearningVelocity: () =>
      fetchData(`/analytics/learning-velocity/${studentId}`),
    getAtRiskStatus: () => fetchData(`/analytics/at-risk/${studentId}`),
    getProgress: () => fetchData(`/progress/${studentId}`),
  };
};

// ============================================================================
// Mastery Prediction Widget
// ============================================================================

export const MasteryPredictionWidget = ({ studentId, lessonId }) => {
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(true);
  const api = useAnalyticsAPI(studentId);

  useEffect(() => {
    loadPrediction();
  }, [studentId, lessonId]);

  const loadPrediction = async () => {
    try {
      const data = await api.predictMastery(lessonId);
      setPrediction(data);
    } catch (error) {
      console.error('Failed to load prediction:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <View style={styles.widgetCard}>
        <ActivityIndicator size="small" color="#3498db" />
      </View>
    );
  }

  if (!prediction) return null;

  const getConfidenceColor = (confidence) => {
    if (confidence >= 0.8) return '#4CAF50';
    if (confidence >= 0.6) return '#FF9800';
    return '#F44336';
  };

  return (
    <View style={styles.widgetCard}>
      <View style={styles.widgetHeader}>
        <Text style={styles.widgetTitle}>🎯 Mastery Prediction</Text>
      </View>

      <View style={styles.predictionContent}>
        <View style={styles.predictionCircle}>
          <Text style={styles.predictionValue}>
            {Math.round(prediction.predicted_mastery * 100)}%
          </Text>
          <Text style={styles.predictionLabel}>Predicted</Text>
        </View>

        <View style={styles.predictionDetails}>
          <View style={styles.detailRow}>
            <Text style={styles.detailLabel}>Current Level:</Text>
            <Text style={[styles.detailValue, styles.levelBadge]}>
              {prediction.current_level}
            </Text>
          </View>

          <View style={styles.detailRow}>
            <Text style={styles.detailLabel}>Predicted Level:</Text>
            <Text style={[styles.detailValue, styles.levelBadge]}>
              {prediction.predicted_level}
            </Text>
          </View>

          <View style={styles.detailRow}>
            <Text style={styles.detailLabel}>Confidence:</Text>
            <View style={styles.confidenceBar}>
              <View
                style={[
                  styles.confidenceFill,
                  {
                    width: `${prediction.confidence * 100}%`,
                    backgroundColor: getConfidenceColor(prediction.confidence),
                  },
                ]}
              />
            </View>
            <Text style={styles.confidenceText}>
              {Math.round(prediction.confidence * 100)}%
            </Text>
          </View>

          {prediction.time_to_mastery && (
            <View style={styles.detailRow}>
              <Text style={styles.detailLabel}>Est. Time to Mastery:</Text>
              <Text style={styles.detailValue}>
                {Math.round(prediction.time_to_mastery / 60)} min
              </Text>
            </View>
          )}
        </View>
      </View>

      {prediction.recommendations && prediction.recommendations.length > 0 && (
        <View style={styles.recommendationsSection}>
          <Text style={styles.sectionTitle}>💡 Recommendations</Text>
          {prediction.recommendations.map((rec, index) => (
            <Text key={index} style={styles.recommendationText}>
              • {rec}
            </Text>
          ))}
        </View>
      )}
    </View>
  );
};

// ============================================================================
// Study Time Recommendation Widget
// ============================================================================

export const StudyTimeWidget = ({ studentId }) => {
  const [recommendation, setRecommendation] = useState(null);
  const [loading, setLoading] = useState(true);
  const api = useAnalyticsAPI(studentId);

  useEffect(() => {
    loadRecommendation();
  }, [studentId]);

  const loadRecommendation = async () => {
    try {
      const data = await api.getStudyRecommendation();
      setRecommendation(data);
    } catch (error) {
      console.error('Failed to load study recommendation:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <View style={styles.widgetCard}>
        <ActivityIndicator size="small" color="#3498db" />
      </View>
    );
  }

  if (!recommendation) return null;

  const getTimeOfDayIcon = (timeOfDay) => {
    const icons = {
      morning: '🌅',
      afternoon: '☀️',
      evening: '🌆',
      night: '🌙',
    };
    return icons[timeOfDay] || '📚';
  };

  return (
    <View style={styles.widgetCard}>
      <View style={styles.widgetHeader}>
        <Text style={styles.widgetTitle}>⏰ Optimal Study Time</Text>
      </View>

      <View style={styles.studyTimeContent}>
        <View style={styles.optimalTimeCard}>
          <Text style={styles.timeIcon}>
            {getTimeOfDayIcon(recommendation.optimal_time_of_day)}
          </Text>
          <Text style={styles.timeOfDay}>
            {recommendation.optimal_time_of_day.toUpperCase()}
          </Text>
          <Text style={styles.timeRange}>{recommendation.time_range}</Text>
        </View>

        <View style={styles.studyMetrics}>
          <View style={styles.metricItem}>
            <Text style={styles.metricValue}>
              {recommendation.optimal_duration} min
            </Text>
            <Text style={styles.metricLabel}>Recommended Duration</Text>
          </View>

          <View style={styles.metricItem}>
            <Text style={styles.metricValue}>
              {recommendation.sessions_per_day}
            </Text>
            <Text style={styles.metricLabel}>Sessions/Day</Text>
          </View>

          <View style={styles.metricItem}>
            <Text style={styles.metricValue}>
              {Math.round(recommendation.peak_performance_score * 100)}%
            </Text>
            <Text style={styles.metricLabel}>Peak Performance</Text>
          </View>
        </View>

        <View style={styles.reasoningSection}>
          <Text style={styles.reasoningTitle}>Why This Time?</Text>
          <Text style={styles.reasoningText}>{recommendation.reasoning}</Text>
        </View>
      </View>
    </View>
  );
};

// ============================================================================
// Learning Velocity Widget
// ============================================================================

export const LearningVelocityWidget = ({ studentId }) => {
  const [velocity, setVelocity] = useState(null);
  const [loading, setLoading] = useState(true);
  const api = useAnalyticsAPI(studentId);

  useEffect(() => {
    loadVelocity();
  }, [studentId]);

  const loadVelocity = async () => {
    try {
      const data = await api.getLearningVelocity();
      setVelocity(data);
    } catch (error) {
      console.error('Failed to load velocity:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <View style={styles.widgetCard}>
        <ActivityIndicator size="small" color="#3498db" />
      </View>
    );
  }

  if (!velocity) return null;

  const getTrendIcon = (trend) => {
    if (trend === 'increasing') return '📈';
    if (trend === 'decreasing') return '📉';
    return '➡️';
  };

  const getTrendColor = (trend) => {
    if (trend === 'increasing') return '#4CAF50';
    if (trend === 'decreasing') return '#F44336';
    return '#FF9800';
  };

  return (
    <View style={styles.widgetCard}>
      <View style={styles.widgetHeader}>
        <Text style={styles.widgetTitle}>⚡ Learning Velocity</Text>
      </View>

      <View style={styles.velocityContent}>
        <View style={styles.velocityHeader}>
          <View style={styles.velocityMain}>
            <Text style={styles.velocityValue}>
              {velocity.lessons_per_week.toFixed(1)}
            </Text>
            <Text style={styles.velocityUnit}>lessons/week</Text>
          </View>
          <View
            style={[
              styles.trendBadge,
              { backgroundColor: getTrendColor(velocity.trend) },
            ]}
          >
            <Text style={styles.trendIcon}>{getTrendIcon(velocity.trend)}</Text>
            <Text style={styles.trendText}>{velocity.trend}</Text>
          </View>
        </View>

        <View style={styles.velocityGrid}>
          <View style={styles.velocityMetric}>
            <Text style={styles.metricNumber}>
              {velocity.avg_time_per_lesson} min
            </Text>
            <Text style={styles.metricCaption}>Avg Time/Lesson</Text>
          </View>

          <View style={styles.velocityMetric}>
            <Text style={styles.metricNumber}>
              {Math.round(velocity.completion_rate * 100)}%
            </Text>
            <Text style={styles.metricCaption}>Completion Rate</Text>
          </View>

          <View style={styles.velocityMetric}>
            <Text style={styles.metricNumber}>
              {velocity.active_days_per_week}
            </Text>
            <Text style={styles.metricCaption}>Active Days/Week</Text>
          </View>

          <View style={styles.velocityMetric}>
            <Text style={styles.metricNumber}>
              {Math.round(velocity.avg_quiz_score)}%
            </Text>
            <Text style={styles.metricCaption}>Avg Quiz Score</Text>
          </View>
        </View>

        {velocity.insights && velocity.insights.length > 0 && (
          <View style={styles.insightsSection}>
            <Text style={styles.insightsTitle}>💡 Insights</Text>
            {velocity.insights.map((insight, index) => (
              <Text key={index} style={styles.insightText}>
                • {insight}
              </Text>
            ))}
          </View>
        )}
      </View>
    </View>
  );
};

// ============================================================================
// At-Risk Status Widget
// ============================================================================

export const AtRiskWidget = ({ studentId }) => {
  const [riskStatus, setRiskStatus] = useState(null);
  const [loading, setLoading] = useState(true);
  const api = useAnalyticsAPI(studentId);

  useEffect(() => {
    loadRiskStatus();
  }, [studentId]);

  const loadRiskStatus = async () => {
    try {
      const data = await api.getAtRiskStatus();
      setRiskStatus(data);
    } catch (error) {
      console.error('Failed to load risk status:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <View style={styles.widgetCard}>
        <ActivityIndicator size="small" color="#3498db" />
      </View>
    );
  }

  if (!riskStatus) return null;

  const getRiskColor = (level) => {
    if (level === 'high') return '#F44336';
    if (level === 'medium') return '#FF9800';
    return '#4CAF50';
  };

  const getRiskIcon = (level) => {
    if (level === 'high') return '🚨';
    if (level === 'medium') return '⚠️';
    return '✅';
  };

  return (
    <View
      style={[
        styles.widgetCard,
        { borderLeftWidth: 4, borderLeftColor: getRiskColor(riskStatus.risk_level) },
      ]}
    >
      <View style={styles.widgetHeader}>
        <Text style={styles.widgetTitle}>
          {getRiskIcon(riskStatus.risk_level)} At-Risk Assessment
        </Text>
      </View>

      <View style={styles.riskContent}>
        <View
          style={[
            styles.riskLevelBadge,
            { backgroundColor: getRiskColor(riskStatus.risk_level) },
          ]}
        >
          <Text style={styles.riskLevelText}>
            {riskStatus.risk_level.toUpperCase()} RISK
          </Text>
          <Text style={styles.riskScoreText}>
            Score: {Math.round(riskStatus.risk_score * 100)}%
          </Text>
        </View>

        {riskStatus.risk_factors && riskStatus.risk_factors.length > 0 && (
          <View style={styles.riskFactorsSection}>
            <Text style={styles.sectionTitle}>Risk Factors:</Text>
            {riskStatus.risk_factors.map((factor, index) => (
              <View key={index} style={styles.riskFactorItem}>
                <Text style={styles.riskFactorIcon}>⚠️</Text>
                <Text style={styles.riskFactorText}>{factor}</Text>
              </View>
            ))}
          </View>
        )}

        {riskStatus.interventions && riskStatus.interventions.length > 0 && (
          <View style={styles.interventionsSection}>
            <Text style={styles.sectionTitle}>Recommended Actions:</Text>
            {riskStatus.interventions.map((intervention, index) => (
              <View key={index} style={styles.interventionItem}>
                <Text style={styles.interventionIcon}>💡</Text>
                <Text style={styles.interventionText}>{intervention}</Text>
              </View>
            ))}
          </View>
        )}
      </View>
    </View>
  );
};

// ============================================================================
// Progress Overview Widget
// ============================================================================

export const ProgressOverviewWidget = ({ studentId }) => {
  const [progress, setProgress] = useState(null);
  const [loading, setLoading] = useState(true);
  const api = useAnalyticsAPI(studentId);

  useEffect(() => {
    loadProgress();
  }, [studentId]);

  const loadProgress = async () => {
    try {
      const data = await api.getProgress();
      setProgress(data);
    } catch (error) {
      console.error('Failed to load progress:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <View style={styles.widgetCard}>
        <ActivityIndicator size="small" color="#3498db" />
      </View>
    );
  }

  if (!progress) return null;

  return (
    <View style={styles.widgetCard}>
      <View style={styles.widgetHeader}>
        <Text style={styles.widgetTitle}>📊 Progress Overview</Text>
      </View>

      <View style={styles.progressGrid}>
        <View style={styles.progressItem}>
          <View style={styles.progressCircle}>
            <Text style={styles.progressCircleValue}>
              {progress.lessons_completed}
            </Text>
          </View>
          <Text style={styles.progressLabel}>Lessons Completed</Text>
        </View>

        <View style={styles.progressItem}>
          <View style={styles.progressCircle}>
            <Text style={styles.progressCircleValue}>
              {Math.round(progress.avg_mastery * 100)}%
            </Text>
          </View>
          <Text style={styles.progressLabel}>Avg Mastery</Text>
        </View>

        <View style={styles.progressItem}>
          <View style={styles.progressCircle}>
            <Text style={styles.progressCircleValue}>
              {progress.total_study_time_hours}h
            </Text>
          </View>
          <Text style={styles.progressLabel}>Study Time</Text>
        </View>

        <View style={styles.progressItem}>
          <View style={styles.progressCircle}>
            <Text style={styles.progressCircleValue}>
              {Math.round(progress.avg_quiz_score)}%
            </Text>
          </View>
          <Text style={styles.progressLabel}>Quiz Average</Text>
        </View>
      </View>

      {progress.recent_achievements && progress.recent_achievements.length > 0 && (
        <View style={styles.recentAchievements}>
          <Text style={styles.sectionTitle}>🏆 Recent Achievements</Text>
          <ScrollView horizontal showsHorizontalScrollIndicator={false}>
            {progress.recent_achievements.map((achievement, index) => (
              <View key={index} style={styles.achievementBadge}>
                <Text style={styles.achievementIcon}>{achievement.icon}</Text>
                <Text style={styles.achievementName}>{achievement.name}</Text>
              </View>
            ))}
          </ScrollView>
        </View>
      )}
    </View>
  );
};

// ============================================================================
// Complete Analytics Dashboard
// ============================================================================

export const AnalyticsDashboard = ({ studentId, currentLessonId }) => {
  const [activeTab, setActiveTab] = useState('overview');

  return (
    <View style={styles.dashboard}>
      {/* Tab Navigation */}
      <View style={styles.tabBar}>
        {['overview', 'velocity', 'prediction', 'study-time'].map((tab) => (
          <TouchableOpacity
            key={tab}
            style={[styles.tab, activeTab === tab && styles.tabActive]}
            onPress={() => setActiveTab(tab)}
          >
            <Text style={[styles.tabText, activeTab === tab && styles.tabTextActive]}>
              {tab.charAt(0).toUpperCase() + tab.slice(1).replace('-', ' ')}
            </Text>
          </TouchableOpacity>
        ))}
      </View>

      {/* Dashboard Content */}
      <ScrollView style={styles.dashboardContent}>
        {activeTab === 'overview' && (
          <>
            <ProgressOverviewWidget studentId={studentId} />
            <AtRiskWidget studentId={studentId} />
          </>
        )}

        {activeTab === 'velocity' && (
          <LearningVelocityWidget studentId={studentId} />
        )}

        {activeTab === 'prediction' && currentLessonId && (
          <MasteryPredictionWidget
            studentId={studentId}
            lessonId={currentLessonId}
          />
        )}

        {activeTab === 'study-time' && <StudyTimeWidget studentId={studentId} />}
      </ScrollView>
    </View>
  );
};

// ============================================================================
// Styles
// ============================================================================

const styles = StyleSheet.create({
  // Widget Card
  widgetCard: {
    backgroundColor: '#fff',
    borderRadius: 12,
    padding: 20,
    marginBottom: 20,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  widgetHeader: {
    marginBottom: 15,
  },
  widgetTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#333',
  },

  // Mastery Prediction
  predictionContent: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  predictionCircle: {
    width: 100,
    height: 100,
    borderRadius: 50,
    backgroundColor: '#3498db',
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 20,
  },
  predictionValue: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#fff',
  },
  predictionLabel: {
    fontSize: 12,
    color: '#fff',
    marginTop: 4,
  },
  predictionDetails: {
    flex: 1,
  },
  detailRow: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 10,
  },
  detailLabel: {
    fontSize: 14,
    color: '#666',
    marginRight: 10,
    flex: 1,
  },
  detailValue: {
    fontSize: 14,
    fontWeight: '600',
    color: '#333',
  },
  levelBadge: {
    backgroundColor: '#e3f2fd',
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 4,
    color: '#1976d2',
  },
  confidenceBar: {
    flex: 2,
    height: 8,
    backgroundColor: '#e0e0e0',
    borderRadius: 4,
    overflow: 'hidden',
    marginHorizontal: 10,
  },
  confidenceFill: {
    height: '100%',
  },
  confidenceText: {
    fontSize: 12,
    fontWeight: '600',
    minWidth: 35,
  },
  recommendationsSection: {
    marginTop: 15,
    paddingTop: 15,
    borderTopWidth: 1,
    borderTopColor: '#e0e0e0',
  },
  sectionTitle: {
    fontSize: 14,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 10,
  },
  recommendationText: {
    fontSize: 13,
    color: '#666',
    marginBottom: 5,
    lineHeight: 18,
  },

  // Study Time
  studyTimeContent: {
    alignItems: 'center',
  },
  optimalTimeCard: {
    alignItems: 'center',
    backgroundColor: '#f8f9fa',
    padding: 20,
    borderRadius: 10,
    width: '100%',
    marginBottom: 20,
  },
  timeIcon: {
    fontSize: 48,
    marginBottom: 10,
  },
  timeOfDay: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 5,
  },
  timeRange: {
    fontSize: 14,
    color: '#666',
  },
  studyMetrics: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    width: '100%',
    marginBottom: 20,
  },
  metricItem: {
    alignItems: 'center',
  },
  metricValue: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#3498db',
  },
  metricLabel: {
    fontSize: 11,
    color: '#999',
    marginTop: 4,
    textAlign: 'center',
  },
  reasoningSection: {
    backgroundColor: '#e3f2fd',
    padding: 15,
    borderRadius: 8,
    width: '100%',
  },
  reasoningTitle: {
    fontSize: 14,
    fontWeight: '600',
    color: '#1976d2',
    marginBottom: 8,
  },
  reasoningText: {
    fontSize: 13,
    color: '#666',
    lineHeight: 18,
  },

  // Learning Velocity
  velocityContent: {},
  velocityHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 20,
  },
  velocityMain: {
    alignItems: 'center',
  },
  velocityValue: {
    fontSize: 36,
    fontWeight: 'bold',
    color: '#3498db',
  },
  velocityUnit: {
    fontSize: 14,
    color: '#666',
    marginTop: 4,
  },
  trendBadge: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: 12,
    paddingVertical: 8,
    borderRadius: 20,
  },
  trendIcon: {
    fontSize: 16,
    marginRight: 6,
  },
  trendText: {
    fontSize: 12,
    fontWeight: '600',
    color: '#fff',
    textTransform: 'capitalize',
  },
  velocityGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'space-between',
    marginBottom: 20,
  },
  velocityMetric: {
    width: '48%',
    backgroundColor: '#f8f9fa',
    padding: 15,
    borderRadius: 8,
    marginBottom: 10,
    alignItems: 'center',
  },
  metricNumber: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#333',
  },
  metricCaption: {
    fontSize: 11,
    color: '#999',
    marginTop: 5,
    textAlign: 'center',
  },
  insightsSection: {
    backgroundColor: '#fff3cd',
    padding: 15,
    borderRadius: 8,
  },
  insightsTitle: {
    fontSize: 14,
    fontWeight: '600',
    color: '#856404',
    marginBottom: 8,
  },
  insightText: {
    fontSize: 13,
    color: '#666',
    marginBottom: 5,
    lineHeight: 18,
  },

  // At-Risk Widget
  riskContent: {},
  riskLevelBadge: {
    padding: 15,
    borderRadius: 8,
    alignItems: 'center',
    marginBottom: 20,
  },
  riskLevelText: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#fff',
  },
  riskScoreText: {
    fontSize: 14,
    color: '#fff',
    marginTop: 5,
    opacity: 0.9,
  },
  riskFactorsSection: {
    marginBottom: 20,
  },
  riskFactorItem: {
    flexDirection: 'row',
    alignItems: 'flex-start',
    marginBottom: 8,
  },
  riskFactorIcon: {
    fontSize: 16,
    marginRight: 10,
  },
  riskFactorText: {
    flex: 1,
    fontSize: 14,
    color: '#666',
    lineHeight: 20,
  },
  interventionsSection: {},
  interventionItem: {
    flexDirection: 'row',
    alignItems: 'flex-start',
    marginBottom: 8,
    backgroundColor: '#e8f5e9',
    padding: 10,
    borderRadius: 6,
  },
  interventionIcon: {
    fontSize: 16,
    marginRight: 10,
  },
  interventionText: {
    flex: 1,
    fontSize: 14,
    color: '#2e7d32',
    lineHeight: 20,
  },

  // Progress Overview
  progressGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'space-between',
    marginBottom: 20,
  },
  progressItem: {
    width: '48%',
    alignItems: 'center',
    marginBottom: 20,
  },
  progressCircle: {
    width: 80,
    height: 80,
    borderRadius: 40,
    backgroundColor: '#3498db',
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 10,
  },
  progressCircleValue: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#fff',
  },
  progressLabel: {
    fontSize: 12,
    color: '#666',
    textAlign: 'center',
  },
  recentAchievements: {
    paddingTop: 15,
    borderTopWidth: 1,
    borderTopColor: '#e0e0e0',
  },
  achievementBadge: {
    backgroundColor: '#FFD700',
    padding: 12,
    borderRadius: 8,
    marginRight: 10,
    alignItems: 'center',
    minWidth: 80,
  },
  achievementIcon: {
    fontSize: 24,
    marginBottom: 5,
  },
  achievementName: {
    fontSize: 10,
    fontWeight: '600',
    color: '#333',
    textAlign: 'center',
  },

  // Dashboard
  dashboard: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  tabBar: {
    flexDirection: 'row',
    backgroundColor: '#fff',
    borderBottomWidth: 1,
    borderBottomColor: '#e0e0e0',
  },
  tab: {
    flex: 1,
    paddingVertical: 15,
    alignItems: 'center',
  },
  tabActive: {
    borderBottomWidth: 3,
    borderBottomColor: '#3498db',
  },
  tabText: {
    fontSize: 13,
    color: '#666',
  },
  tabTextActive: {
    color: '#3498db',
    fontWeight: '600',
  },
  dashboardContent: {
    flex: 1,
    padding: 15,
  },
});

export default {
  MasteryPredictionWidget,
  StudyTimeWidget,
  LearningVelocityWidget,
  AtRiskWidget,
  ProgressOverviewWidget,
  AnalyticsDashboard,
};
