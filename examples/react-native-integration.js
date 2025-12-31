/**
 * Wave 3 React Native Integration Examples
 * Complete integration patterns for mobile apps
 */

import React, { useState, useEffect, useContext, useRef } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  ScrollView,
  ActivityIndicator,
  Modal,
  Animated,
} from 'react-native';

// ============================================================================
// API Service Hook
// ============================================================================

export const useWave3API = (token = null) => {
  const BASE_URL = 'http://localhost:8000/api/v3';

  const request = async (endpoint, options = {}) => {
    try {
      const response = await fetch(`${BASE_URL}${endpoint}`, {
        ...options,
        headers: {
          'Content-Type': 'application/json',
          ...(token && { 'Authorization': `Bearer ${token}` }),
          ...options.headers,
        },
      });

      if (!response.ok) {
        throw new Error(`API Error: ${response.statusText}`);
      }

      return await response.json();
    } catch (error) {
      console.error('API Request failed:', error);
      throw error;
    }
  };

  return {
    // Lessons
    getLessons: (subject, grade) => {
      const params = new URLSearchParams();
      if (subject) params.append('subject', subject);
      if (grade) params.append('grade', grade);
      return request(`/lessons?${params.toString()}`);
    },
    getLesson: (lessonId) => request(`/lessons/${lessonId}`),
    searchLessons: (query, searchType) =>
      request('/lessons/search', {
        method: 'POST',
        body: JSON.stringify({ query, search_type: searchType }),
      }),

    // Recommendations
    getRecommendations: (studentId, method, limit) =>
      request(`/recommendations/${studentId}?method=${method}&limit=${limit}`),
    recordInteraction: (studentId, lessonId, type, metadata) =>
      request('/recommendations/interaction', {
        method: 'POST',
        body: JSON.stringify({
          student_id: studentId,
          lesson_id: lessonId,
          interaction_type: type,
          metadata,
        }),
      }),

    // Gamification
    getStudentStats: (studentId) => request(`/gamification/stats/${studentId}`),
    getAchievements: (studentId) =>
      request(`/gamification/achievements/${studentId}`),
    getLeaderboard: (scope, limit) =>
      request(`/gamification/leaderboard?scope=${scope}&limit=${limit}`),
    getStreak: (studentId) => request(`/gamification/streak/${studentId}`),

    // Analytics
    predictMastery: (studentId, lessonId) =>
      request(`/analytics/predict-mastery/${studentId}/${lessonId}`),
    getStudyRecommendation: (studentId) =>
      request(`/analytics/study-recommendation/${studentId}`),
    getLearningVelocity: (studentId) =>
      request(`/analytics/learning-velocity/${studentId}`),
    getAtRiskStatus: (studentId) => request(`/analytics/at-risk/${studentId}`),

    // Progress
    submitQuiz: (quizData) =>
      request('/progress/quiz', {
        method: 'POST',
        body: JSON.stringify(quizData),
      }),
    recordActivity: (activityData) =>
      request('/progress/activity', {
        method: 'POST',
        body: JSON.stringify(activityData),
      }),
    getMastery: (studentId, lessonId) =>
      request(`/progress/mastery/${studentId}/${lessonId}`),
    getProgress: (studentId) => request(`/progress/${studentId}`),
  };
};

// ============================================================================
// WebSocket Hook for React Native
// ============================================================================

export const useWave3WebSocket = (studentId, onMessage, enabled = true) => {
  const wsRef = useRef(null);
  const [isConnected, setIsConnected] = useState(false);

  useEffect(() => {
    if (!enabled || !studentId) return;

    const ws = new WebSocket(`ws://localhost:8000/ws/${studentId}`);

    ws.onopen = () => {
      console.log('WebSocket connected');
      setIsConnected(true);
    };

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        onMessage(data);
      } catch (error) {
        console.error('WebSocket message error:', error);
      }
    };

    ws.onerror = (error) => {
      console.error('WebSocket error:', error);
    };

    ws.onclose = () => {
      console.log('WebSocket disconnected');
      setIsConnected(false);
    };

    wsRef.current = ws;

    return () => {
      if (wsRef.current) {
        wsRef.current.close();
      }
    };
  }, [studentId, enabled]);

  return { isConnected, ws: wsRef.current };
};

// ============================================================================
// Animated Achievement Notification
// ============================================================================

export const AchievementNotification = ({ achievement, visible, onClose }) => {
  const slideAnim = useRef(new Animated.Value(-100)).current;
  const opacityAnim = useRef(new Animated.Value(0)).current;

  useEffect(() => {
    if (visible) {
      Animated.parallel([
        Animated.spring(slideAnim, {
          toValue: 0,
          useNativeDriver: true,
        }),
        Animated.timing(opacityAnim, {
          toValue: 1,
          duration: 300,
          useNativeDriver: true,
        }),
      ]).start();

      const timer = setTimeout(() => {
        Animated.parallel([
          Animated.timing(slideAnim, {
            toValue: -100,
            duration: 300,
            useNativeDriver: true,
          }),
          Animated.timing(opacityAnim, {
            toValue: 0,
            duration: 300,
            useNativeDriver: true,
          }),
        ]).start(() => onClose());
      }, 4000);

      return () => clearTimeout(timer);
    }
  }, [visible]);

  if (!visible || !achievement) return null;

  const badgeColors = {
    Bronze: '#CD7F32',
    Silver: '#C0C0C0',
    Gold: '#FFD700',
    Platinum: '#E5E4E2',
    Diamond: '#B9F2FF',
  };

  return (
    <Animated.View
      style={[
        styles.achievementNotification,
        {
          transform: [{ translateY: slideAnim }],
          opacity: opacityAnim,
          backgroundColor: badgeColors[achievement.badge_level] || '#4CAF50',
        },
      ]}
    >
      <Text style={styles.achievementIcon}>{achievement.icon}</Text>
      <View style={styles.achievementContent}>
        <Text style={styles.achievementTitle}>Achievement Unlocked!</Text>
        <Text style={styles.achievementName}>{achievement.name}</Text>
        <Text style={styles.achievementDescription}>
          {achievement.description}
        </Text>
      </View>
    </Animated.View>
  );
};

// ============================================================================
// Student Stats Widget
// ============================================================================

export const StudentStatsWidget = ({ studentId }) => {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const api = useWave3API();

  useEffect(() => {
    loadStats();
  }, [studentId]);

  const loadStats = async () => {
    try {
      const data = await api.getStudentStats(studentId);
      setStats(data);
    } catch (error) {
      console.error('Failed to load stats:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <View style={styles.widgetContainer}>
        <ActivityIndicator size="small" color="#3498db" />
      </View>
    );
  }

  if (!stats) return null;

  return (
    <View style={styles.statsWidget}>
      <View style={styles.statItem}>
        <Text style={styles.statValue}>{stats.points}</Text>
        <Text style={styles.statLabel}>Points</Text>
      </View>
      <View style={styles.statItem}>
        <Text style={styles.statValue}>{stats.level}</Text>
        <Text style={styles.statLabel}>Level</Text>
      </View>
      <View style={styles.statItem}>
        <Text style={styles.statValue}>
          🔥 {stats.streak?.current_streak || 0}
        </Text>
        <Text style={styles.statLabel}>Day Streak</Text>
      </View>
      <View style={styles.statItem}>
        <Text style={styles.statValue}>{stats.achievements_unlocked || 0}</Text>
        <Text style={styles.statLabel}>Achievements</Text>
      </View>
    </View>
  );
};

// ============================================================================
// Mastery Progress Bar
// ============================================================================

export const MasteryProgressBar = ({ studentId, lessonId }) => {
  const [mastery, setMastery] = useState(null);
  const [loading, setLoading] = useState(true);
  const api = useWave3API();
  const progressAnim = useRef(new Animated.Value(0)).current;

  useEffect(() => {
    loadMastery();
  }, [studentId, lessonId]);

  const loadMastery = async () => {
    try {
      const data = await api.getMastery(studentId, lessonId);
      setMastery(data);
      
      Animated.timing(progressAnim, {
        toValue: data.mastery_percentage,
        duration: 1000,
        useNativeDriver: false,
      }).start();
    } catch (error) {
      console.error('Failed to load mastery:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading || !mastery) return null;

  const getMasteryColor = (level) => {
    const colors = {
      novice: '#9E9E9E',
      beginner: '#2196F3',
      intermediate: '#FF9800',
      advanced: '#9C27B0',
      proficient: '#4CAF50',
      expert: '#FFD700',
    };
    return colors[level] || '#9E9E9E';
  };

  return (
    <View style={styles.masteryContainer}>
      <View style={styles.masteryHeader}>
        <Text style={styles.masteryTitle}>Mastery Progress</Text>
        <Text
          style={[
            styles.masteryLevel,
            { color: getMasteryColor(mastery.mastery_level) },
          ]}
        >
          {mastery.mastery_level.toUpperCase()}
        </Text>
      </View>
      
      <View style={styles.progressBarContainer}>
        <View style={styles.progressBarBackground}>
          <Animated.View
            style={[
              styles.progressBarFill,
              {
                width: progressAnim.interpolate({
                  inputRange: [0, 100],
                  outputRange: ['0%', '100%'],
                }),
                backgroundColor: getMasteryColor(mastery.mastery_level),
              },
            ]}
          />
        </View>
        <Text style={styles.progressText}>
          {Math.round(mastery.mastery_percentage)}%
        </Text>
      </View>

      <View style={styles.masteryStats}>
        <View style={styles.masteryStat}>
          <Text style={styles.statNumber}>{mastery.activities_completed}</Text>
          <Text style={styles.statCaption}>Activities</Text>
        </View>
        <View style={styles.masteryStat}>
          <Text style={styles.statNumber}>
            {Math.round(mastery.quiz_average)}%
          </Text>
          <Text style={styles.statCaption}>Quiz Avg</Text>
        </View>
        <View style={styles.masteryStat}>
          <Text style={styles.statNumber}>
            {mastery.problems_correct}/{mastery.problems_attempted}
          </Text>
          <Text style={styles.statCaption}>Problems</Text>
        </View>
      </View>
    </View>
  );
};

// ============================================================================
// Leaderboard Widget
// ============================================================================

export const LeaderboardWidget = ({ scope = 'global', limit = 5 }) => {
  const [leaderboard, setLeaderboard] = useState([]);
  const [loading, setLoading] = useState(true);
  const api = useWave3API();

  useEffect(() => {
    loadLeaderboard();
  }, [scope, limit]);

  const loadLeaderboard = async () => {
    try {
      const data = await api.getLeaderboard(scope, limit);
      setLeaderboard(data.leaderboard || []);
    } catch (error) {
      console.error('Failed to load leaderboard:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <View style={styles.widgetContainer}>
        <ActivityIndicator size="small" color="#3498db" />
      </View>
    );
  }

  const getRankBadge = (rank) => {
    if (rank === 1) return '🥇';
    if (rank === 2) return '🥈';
    if (rank === 3) return '🥉';
    return `#${rank}`;
  };

  return (
    <View style={styles.leaderboardWidget}>
      <Text style={styles.widgetTitle}>🏆 Leaderboard</Text>
      {leaderboard.map((entry, index) => (
        <View key={entry.student_id} style={styles.leaderboardEntry}>
          <Text style={styles.leaderboardRank}>{getRankBadge(entry.rank)}</Text>
          <View style={styles.leaderboardInfo}>
            <Text style={styles.leaderboardName}>{entry.student_name}</Text>
            <Text style={styles.leaderboardMeta}>
              Level {entry.level} • {entry.points} pts
            </Text>
          </View>
          <Text style={styles.leaderboardStreak}>🔥 {entry.streak}</Text>
        </View>
      ))}
    </View>
  );
};

// ============================================================================
// Real-time Dashboard Component
// ============================================================================

export const RealtimeDashboard = ({ studentId }) => {
  const [showAchievement, setShowAchievement] = useState(false);
  const [currentAchievement, setCurrentAchievement] = useState(null);

  useWave3WebSocket(
    studentId,
    (data) => {
      if (data.type === 'achievement_unlocked') {
        setCurrentAchievement(data.achievement);
        setShowAchievement(true);
      }
    },
    true
  );

  return (
    <ScrollView style={styles.dashboard}>
      <StudentStatsWidget studentId={studentId} />
      <MasteryProgressBar studentId={studentId} lessonId="current_lesson_id" />
      <LeaderboardWidget scope="global" limit={5} />
      
      <AchievementNotification
        achievement={currentAchievement}
        visible={showAchievement}
        onClose={() => setShowAchievement(false)}
      />
    </ScrollView>
  );
};

// ============================================================================
// Styles
// ============================================================================

const styles = StyleSheet.create({
  widgetContainer: {
    padding: 20,
    backgroundColor: '#fff',
    borderRadius: 10,
    marginBottom: 15,
  },
  
  // Stats Widget
  statsWidget: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    backgroundColor: '#fff',
    padding: 20,
    borderRadius: 10,
    marginBottom: 15,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  statItem: {
    alignItems: 'center',
  },
  statValue: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#3498db',
  },
  statLabel: {
    fontSize: 12,
    color: '#666',
    marginTop: 4,
  },

  // Achievement Notification
  achievementNotification: {
    position: 'absolute',
    top: 50,
    left: 20,
    right: 20,
    flexDirection: 'row',
    padding: 15,
    borderRadius: 10,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.3,
    shadowRadius: 8,
    elevation: 8,
    zIndex: 1000,
  },
  achievementIcon: {
    fontSize: 40,
    marginRight: 15,
  },
  achievementContent: {
    flex: 1,
  },
  achievementTitle: {
    color: '#fff',
    fontSize: 12,
    fontWeight: '600',
    marginBottom: 2,
  },
  achievementName: {
    color: '#fff',
    fontSize: 16,
    fontWeight: 'bold',
    marginBottom: 4,
  },
  achievementDescription: {
    color: '#fff',
    fontSize: 12,
    opacity: 0.9,
  },

  // Mastery Progress
  masteryContainer: {
    backgroundColor: '#fff',
    padding: 20,
    borderRadius: 10,
    marginBottom: 15,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  masteryHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 15,
  },
  masteryTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#333',
  },
  masteryLevel: {
    fontSize: 14,
    fontWeight: 'bold',
  },
  progressBarContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 15,
  },
  progressBarBackground: {
    flex: 1,
    height: 10,
    backgroundColor: '#e0e0e0',
    borderRadius: 5,
    overflow: 'hidden',
    marginRight: 10,
  },
  progressBarFill: {
    height: '100%',
    borderRadius: 5,
  },
  progressText: {
    fontSize: 14,
    fontWeight: '600',
    color: '#666',
    minWidth: 45,
  },
  masteryStats: {
    flexDirection: 'row',
    justifyContent: 'space-around',
  },
  masteryStat: {
    alignItems: 'center',
  },
  statNumber: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#333',
  },
  statCaption: {
    fontSize: 11,
    color: '#999',
    marginTop: 2,
  },

  // Leaderboard Widget
  leaderboardWidget: {
    backgroundColor: '#fff',
    padding: 20,
    borderRadius: 10,
    marginBottom: 15,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  widgetTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 15,
  },
  leaderboardEntry: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: 12,
    borderBottomWidth: 1,
    borderBottomColor: '#f0f0f0',
  },
  leaderboardRank: {
    fontSize: 20,
    fontWeight: 'bold',
    marginRight: 15,
    minWidth: 40,
  },
  leaderboardInfo: {
    flex: 1,
  },
  leaderboardName: {
    fontSize: 16,
    fontWeight: '600',
    color: '#333',
  },
  leaderboardMeta: {
    fontSize: 12,
    color: '#999',
    marginTop: 2,
  },
  leaderboardStreak: {
    fontSize: 14,
    fontWeight: '600',
  },

  // Dashboard
  dashboard: {
    flex: 1,
    backgroundColor: '#f5f5f5',
    padding: 15,
  },
});

export default {
  useWave3API,
  useWave3WebSocket,
  AchievementNotification,
  StudentStatsWidget,
  MasteryProgressBar,
  LeaderboardWidget,
  RealtimeDashboard,
};
