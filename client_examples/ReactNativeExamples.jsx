/**
 * React Native Integration Examples
 * Complete examples for integrating Wave 3 features in React Native apps
 */

import React, { useState, useEffect, useContext } from 'react';
import {
  View,
  Text,
  FlatList,
  TouchableOpacity,
  StyleSheet,
  ActivityIndicator,
  Alert,
} from 'react-native';

// ============================================================================
// Example 1: React Native WebSocket Hook
// ============================================================================

export function useWave3WebSocket(studentId, apiUrl = 'ws://localhost:8000/ws') {
  const [isConnected, setIsConnected] = useState(false);
  const [lastMessage, setLastMessage] = useState(null);
  const [ws, setWs] = useState(null);

  useEffect(() => {
    if (!studentId) return;

    const websocket = new WebSocket(`${apiUrl}/${studentId}`);

    websocket.onopen = () => {
      console.log('WebSocket connected');
      setIsConnected(true);
    };

    websocket.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        setLastMessage(data);
      } catch (error) {
        console.error('Failed to parse WebSocket message:', error);
      }
    };

    websocket.onerror = (error) => {
      console.error('WebSocket error:', error);
    };

    websocket.onclose = () => {
      console.log('WebSocket closed');
      setIsConnected(false);
    };

    setWs(websocket);

    return () => {
      if (websocket) {
        websocket.close();
      }
    };
  }, [studentId, apiUrl]);

  const send = (type, data = {}) => {
    if (ws && isConnected) {
      ws.send(JSON.stringify({ type, ...data }));
    }
  };

  return { isConnected, lastMessage, send };
}

// ============================================================================
// Example 2: Recommendations Screen Component
// ============================================================================

export function RecommendationsScreen({ navigation, studentId, token }) {
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [method, setMethod] = useState('hybrid');

  useEffect(() => {
    fetchRecommendations();
  }, [method]);

  const fetchRecommendations = async () => {
    setLoading(true);
    try {
      const response = await fetch(
        `http://localhost:8000/api/v3/recommendations/${studentId}?method=${method}&limit=5`,
        {
          headers: token ? { Authorization: `Bearer ${token}` } : {},
        }
      );
      const data = await response.json();
      setRecommendations(data.recommendations || []);
    } catch (error) {
      console.error('Failed to fetch recommendations:', error);
      Alert.alert('Error', 'Failed to load recommendations');
    } finally {
      setLoading(false);
    }
  };

  const handleLessonPress = (lesson) => {
    navigation.navigate('LessonDetail', { lessonId: lesson.id });
  };

  const renderRecommendation = ({ item, index }) => (
    <TouchableOpacity
      style={styles.card}
      onPress={() => handleLessonPress(item.lesson)}
    >
      <View style={styles.cardHeader}>
        <Text style={styles.rank}>#{index + 1}</Text>
        <View style={styles.cardContent}>
          <Text style={styles.title}>{item.lesson.title}</Text>
          <Text style={styles.subject}>{item.lesson.subject}</Text>
          <Text style={styles.description} numberOfLines={2}>
            {item.lesson.description}
          </Text>
          <View style={styles.scoreContainer}>
            <View style={styles.scoreBar}>
              <View
                style={[styles.scoreFill, { width: `${item.score * 100}%` }]}
              />
            </View>
            <Text style={styles.scoreText}>{Math.round(item.score * 100)}%</Text>
          </View>
        </View>
      </View>
    </TouchableOpacity>
  );

  return (
    <View style={styles.container}>
      <View style={styles.methodSelector}>
        {['content', 'collaborative', 'hybrid'].map((m) => (
          <TouchableOpacity
            key={m}
            style={[styles.methodButton, method === m && styles.methodButtonActive]}
            onPress={() => setMethod(m)}
          >
            <Text
              style={[
                styles.methodButtonText,
                method === m && styles.methodButtonTextActive,
              ]}
            >
              {m.charAt(0).toUpperCase() + m.slice(1)}
            </Text>
          </TouchableOpacity>
        ))}
      </View>

      {loading ? (
        <View style={styles.loading}>
          <ActivityIndicator size="large" color="#3498db" />
        </View>
      ) : (
        <FlatList
          data={recommendations}
          renderItem={renderRecommendation}
          keyExtractor={(item, index) => `${item.lesson.id}-${index}`}
          contentContainerStyle={styles.list}
        />
      )}
    </View>
  );
}

// ============================================================================
// Example 3: Live Progress Component with WebSocket
// ============================================================================

export function LiveProgressWidget({ studentId }) {
  const { isConnected, lastMessage } = useWave3WebSocket(studentId);
  const [stats, setStats] = useState({
    points: 0,
    level: 1,
    streak: 0,
  });

  useEffect(() => {
    if (lastMessage) {
      if (lastMessage.type === 'achievement_unlocked') {
        Alert.alert(
          '🎉 Achievement Unlocked!',
          lastMessage.achievement.name,
          [{ text: 'Awesome!' }]
        );
      }
      if (lastMessage.type === 'progress_update') {
        setStats((prev) => ({
          ...prev,
          points: prev.points + (lastMessage.points_earned || 0),
        }));
      }
    }
  }, [lastMessage]);

  return (
    <View style={styles.statsWidget}>
      <View style={styles.connectionStatus}>
        <View style={[styles.dot, isConnected && styles.dotConnected]} />
        <Text style={styles.statusText}>
          {isConnected ? 'Live' : 'Offline'}
        </Text>
      </View>

      <View style={styles.statsRow}>
        <View style={styles.statItem}>
          <Text style={styles.statValue}>{stats.points}</Text>
          <Text style={styles.statLabel}>Points</Text>
        </View>
        <View style={styles.statItem}>
          <Text style={styles.statValue}>Level {stats.level}</Text>
          <Text style={styles.statLabel}>Level</Text>
        </View>
        <View style={styles.statItem}>
          <Text style={styles.statValue}>{stats.streak}🔥</Text>
          <Text style={styles.statLabel}>Streak</Text>
        </View>
      </View>
    </View>
  );
}

// ============================================================================
// Example 4: Gamification Achievements Screen
// ============================================================================

export function AchievementsScreen({ studentId, token }) {
  const [achievements, setAchievements] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchAchievements();
  }, []);

  const fetchAchievements = async () => {
    try {
      const response = await fetch(
        `http://localhost:8000/api/v3/gamification/achievements/${studentId}`,
        {
          headers: token ? { Authorization: `Bearer ${token}` } : {},
        }
      );
      const data = await response.json();
      setAchievements(data.achievements || []);
    } catch (error) {
      console.error('Failed to fetch achievements:', error);
    } finally {
      setLoading(false);
    }
  };

  const renderAchievement = ({ item }) => {
    const badgeColors = {
      Bronze: '#CD7F32',
      Silver: '#C0C0C0',
      Gold: '#FFD700',
      Platinum: '#E5E4E2',
      Diamond: '#B9F2FF',
    };

    return (
      <View
        style={[
          styles.achievementCard,
          { borderColor: badgeColors[item.badge_level] || '#ccc' },
        ]}
      >
        <Text style={styles.achievementIcon}>{item.icon}</Text>
        <View style={styles.achievementContent}>
          <Text style={styles.achievementName}>{item.name}</Text>
          <Text style={styles.achievementDescription}>{item.description}</Text>
          <View
            style={[
              styles.badgeLevel,
              { backgroundColor: badgeColors[item.badge_level] || '#ccc' },
            ]}
          >
            <Text style={styles.badgeLevelText}>{item.badge_level}</Text>
          </View>
          {item.unlocked_at && (
            <Text style={styles.unlockedDate}>
              Unlocked: {new Date(item.unlocked_at).toLocaleDateString()}
            </Text>
          )}
        </View>
      </View>
    );
  };

  if (loading) {
    return (
      <View style={styles.loading}>
        <ActivityIndicator size="large" color="#3498db" />
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <Text style={styles.header}>
        🏆 Achievements ({achievements.filter((a) => a.unlocked).length}/
        {achievements.length})
      </Text>
      <FlatList
        data={achievements}
        renderItem={renderAchievement}
        keyExtractor={(item) => item.id}
        contentContainerStyle={styles.list}
      />
    </View>
  );
}

// ============================================================================
// Example 5: Analytics Dashboard Component
// ============================================================================

export function AnalyticsDashboard({ studentId, token }) {
  const [analytics, setAnalytics] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchAnalytics();
  }, []);

  const fetchAnalytics = async () => {
    try {
      const [velocity, studyRec, atRisk] = await Promise.all([
        fetch(
          `http://localhost:8000/api/v3/analytics/learning-velocity/${studentId}`,
          { headers: token ? { Authorization: `Bearer ${token}` } : {} }
        ).then((r) => r.json()),
        fetch(
          `http://localhost:8000/api/v3/analytics/study-recommendation/${studentId}`,
          { headers: token ? { Authorization: `Bearer ${token}` } : {} }
        ).then((r) => r.json()),
        fetch(
          `http://localhost:8000/api/v3/analytics/at-risk/${studentId}`,
          { headers: token ? { Authorization: `Bearer ${token}` } : {} }
        ).then((r) => r.json()),
      ]);

      setAnalytics({ velocity, studyRec, atRisk });
    } catch (error) {
      console.error('Failed to fetch analytics:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <View style={styles.loading}>
        <ActivityIndicator size="large" color="#3498db" />
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <Text style={styles.header}>📊 Your Learning Analytics</Text>

      {/* Learning Velocity */}
      <View style={styles.analyticsCard}>
        <Text style={styles.cardTitle}>Learning Velocity</Text>
        <Text style={styles.cardValue}>
          {analytics.velocity.velocity.toFixed(2)} lessons/week
        </Text>
        <Text style={styles.cardDescription}>
          Trend: {analytics.velocity.trend}
        </Text>
      </View>

      {/* Study Recommendation */}
      <View style={styles.analyticsCard}>
        <Text style={styles.cardTitle}>Best Study Time</Text>
        <Text style={styles.cardValue}>
          {analytics.studyRec.recommended_time}
        </Text>
        <Text style={styles.cardDescription}>
          Duration: {analytics.studyRec.recommended_duration} minutes
        </Text>
      </View>

      {/* At-Risk Status */}
      {analytics.atRisk.is_at_risk && (
        <View style={[styles.analyticsCard, styles.warningCard]}>
          <Text style={styles.cardTitle}>⚠️ Attention Needed</Text>
          <Text style={styles.cardDescription}>
            Risk Level: {analytics.atRisk.risk_level}
          </Text>
          {analytics.atRisk.recommendations.map((rec, i) => (
            <Text key={i} style={styles.recommendation}>
              • {rec}
            </Text>
          ))}
        </View>
      )}
    </View>
  );
}

// ============================================================================
// Styles
// ============================================================================

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  loading: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  header: {
    fontSize: 20,
    fontWeight: 'bold',
    padding: 16,
    backgroundColor: '#fff',
  },
  methodSelector: {
    flexDirection: 'row',
    padding: 16,
    backgroundColor: '#fff',
    gap: 8,
  },
  methodButton: {
    flex: 1,
    padding: 12,
    borderRadius: 8,
    backgroundColor: '#f0f0f0',
    alignItems: 'center',
  },
  methodButtonActive: {
    backgroundColor: '#3498db',
  },
  methodButtonText: {
    color: '#666',
    fontWeight: '600',
  },
  methodButtonTextActive: {
    color: '#fff',
  },
  list: {
    padding: 16,
  },
  card: {
    backgroundColor: '#fff',
    borderRadius: 10,
    padding: 16,
    marginBottom: 12,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  cardHeader: {
    flexDirection: 'row',
    gap: 12,
  },
  rank: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#3498db',
  },
  cardContent: {
    flex: 1,
  },
  title: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 4,
  },
  subject: {
    fontSize: 14,
    color: '#3498db',
    marginBottom: 4,
  },
  description: {
    fontSize: 14,
    color: '#666',
    marginBottom: 8,
  },
  scoreContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
  },
  scoreBar: {
    flex: 1,
    height: 6,
    backgroundColor: '#e0e0e0',
    borderRadius: 3,
    overflow: 'hidden',
  },
  scoreFill: {
    height: '100%',
    backgroundColor: '#4CAF50',
  },
  scoreText: {
    fontSize: 12,
    fontWeight: 'bold',
    color: '#4CAF50',
  },
  statsWidget: {
    backgroundColor: '#fff',
    padding: 16,
    borderRadius: 10,
    margin: 16,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  connectionStatus: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 12,
  },
  dot: {
    width: 8,
    height: 8,
    borderRadius: 4,
    backgroundColor: '#ccc',
    marginRight: 6,
  },
  dotConnected: {
    backgroundColor: '#4CAF50',
  },
  statusText: {
    fontSize: 12,
    color: '#666',
  },
  statsRow: {
    flexDirection: 'row',
    justifyContent: 'space-around',
  },
  statItem: {
    alignItems: 'center',
  },
  statValue: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#333',
  },
  statLabel: {
    fontSize: 12,
    color: '#999',
    marginTop: 4,
  },
  achievementCard: {
    flexDirection: 'row',
    backgroundColor: '#fff',
    borderRadius: 10,
    borderWidth: 2,
    padding: 16,
    marginBottom: 12,
  },
  achievementIcon: {
    fontSize: 40,
    marginRight: 12,
  },
  achievementContent: {
    flex: 1,
  },
  achievementName: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 4,
  },
  achievementDescription: {
    fontSize: 14,
    color: '#666',
    marginBottom: 8,
  },
  badgeLevel: {
    alignSelf: 'flex-start',
    paddingHorizontal: 12,
    paddingVertical: 4,
    borderRadius: 4,
    marginBottom: 4,
  },
  badgeLevelText: {
    color: '#fff',
    fontSize: 12,
    fontWeight: 'bold',
  },
  unlockedDate: {
    fontSize: 12,
    color: '#999',
  },
  analyticsCard: {
    backgroundColor: '#fff',
    borderRadius: 10,
    padding: 16,
    margin: 16,
    marginTop: 0,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  warningCard: {
    borderLeftWidth: 4,
    borderLeftColor: '#FF9800',
  },
  cardTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 8,
  },
  cardValue: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#3498db',
    marginBottom: 4,
  },
  cardDescription: {
    fontSize: 14,
    color: '#666',
  },
  recommendation: {
    fontSize: 14,
    color: '#666',
    marginTop: 4,
  },
});

export default {
  useWave3WebSocket,
  RecommendationsScreen,
  LiveProgressWidget,
  AchievementsScreen,
  AnalyticsDashboard,
};
