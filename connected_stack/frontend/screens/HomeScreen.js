import React, { useContext, useEffect, useState } from 'react';
import {
  View,
  Text,
  TouchableOpacity,
  ScrollView,
  StyleSheet,
  SafeAreaView,
  Alert
} from 'react-native';
import { UserContext } from '../UserContext';
import { getUserProgress } from '../api';

export default function HomeScreen({ navigation }) {
  const { user, logout } = useContext(UserContext);
  const [progressData, setProgressData] = useState(null);

  useEffect(() => {
    loadProgress();
  }, []);

  const loadProgress = async () => {
    try {
      const data = await getUserProgress(user?.token);
      setProgressData(data);
    } catch (error) {
      console.error('Failed to load progress:', error);
    }
  };

  const handleLogout = () => {
    Alert.alert(
      'Logout',
      'Are you sure you want to logout?',
      [
        { text: 'Cancel', style: 'cancel' },
        { text: 'Logout', onPress: logout }
      ]
    );
  };

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView style={styles.scrollView}>
        <View style={styles.header}>
          <Text style={styles.welcomeText}>Welcome back,</Text>
          <Text style={styles.userName}>{user?.email || 'Student'}</Text>
        </View>

        <View style={styles.quickStats}>
          <View style={styles.statCard}>
            <Text style={styles.statNumber}>
              {progressData?.total_questions_attempted || 0}
            </Text>
            <Text style={styles.statLabel}>Questions Attempted</Text>
          </View>
          <View style={styles.statCard}>
            <Text style={styles.statNumber}>
              {progressData ? `${progressData.accuracy_percent.toFixed(0)}%` : '0%'}
            </Text>
            <Text style={styles.statLabel}>Accuracy</Text>
          </View>
          <View style={styles.statCard}>
            <Text style={styles.statNumber}>
              {progressData?.streak_days || 0}
            </Text>
            <Text style={styles.statLabel}>Day Streak</Text>
          </View>
        </View>

        <View style={styles.quickActions}>
          <Text style={styles.sectionTitle}>Quick Actions</Text>

          <TouchableOpacity
            style={styles.actionButton}
            onPress={() => navigation.navigate('Search')}
          >
            <Text style={styles.actionIcon}>🔍</Text>
            <Text style={styles.actionText}>Search Questions</Text>
          </TouchableOpacity>

          <TouchableOpacity
            style={styles.actionButton}
            onPress={() => navigation.navigate('Quiz', { mode: 'quiz', count: 15 })}
          >
            <Text style={styles.actionIcon}>📝</Text>
            <Text style={styles.actionText}>Take Quiz</Text>
          </TouchableOpacity>

          <TouchableOpacity
            style={styles.actionButton}
            onPress={() => navigation.navigate('Progress')}
          >
            <Text style={styles.actionIcon}>📊</Text>
            <Text style={styles.actionText}>View Progress</Text>
          </TouchableOpacity>
        </View>

        {progressData?.weak_topics && progressData.weak_topics.length > 0 && (
          <View style={styles.weakTopicsSection}>
            <Text style={styles.sectionTitle}>Focus Areas</Text>
            {progressData.weak_topics.slice(0, 3).map((topic, index) => (
              <View key={index} style={styles.weakTopicCard}>
                <Text style={styles.weakTopicName}>{topic.topic}</Text>
                <Text style={styles.weakTopicAccuracy}>
                  {topic.accuracy_percent.toFixed(1)}%
                </Text>
              </View>
            ))}
          </View>
        )}

        <TouchableOpacity
          style={styles.logoutButton}
          onPress={handleLogout}
        >
          <Text style={styles.logoutText}>Logout</Text>
        </TouchableOpacity>
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  scrollView: {
    flex: 1,
    padding: 20,
  },
  header: {
    marginBottom: 30,
  },
  welcomeText: {
    fontSize: 16,
    color: '#666',
  },
  userName: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#333',
    marginTop: 5,
  },
  quickStats: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 30,
  },
  statCard: {
    flex: 1,
    backgroundColor: '#fff',
    borderRadius: 12,
    padding: 20,
    marginHorizontal: 5,
    alignItems: 'center',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  statNumber: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#3498db',
    marginBottom: 5,
  },
  statLabel: {
    fontSize: 12,
    color: '#666',
    textAlign: 'center',
  },
  quickActions: {
    marginBottom: 30,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 15,
  },
  actionButton: {
    backgroundColor: '#fff',
    borderRadius: 12,
    padding: 20,
    marginBottom: 10,
    flexDirection: 'row',
    alignItems: 'center',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  actionIcon: {
    fontSize: 24,
    marginRight: 15,
  },
  actionText: {
    fontSize: 16,
    fontWeight: '600',
    color: '#333',
  },
  weakTopicsSection: {
    marginBottom: 30,
  },
  weakTopicCard: {
    backgroundColor: '#fff',
    borderRadius: 8,
    padding: 15,
    marginBottom: 8,
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    borderLeftWidth: 4,
    borderLeftColor: '#e74c3c',
  },
  weakTopicName: {
    fontSize: 16,
    color: '#333',
    flex: 1,
  },
  weakTopicAccuracy: {
    fontSize: 16,
    color: '#e74c3c',
    fontWeight: 'bold',
  },
  logoutButton: {
    backgroundColor: '#e74c3c',
    borderRadius: 8,
    padding: 15,
    alignItems: 'center',
    marginTop: 20,
  },
  logoutText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
  },
});
