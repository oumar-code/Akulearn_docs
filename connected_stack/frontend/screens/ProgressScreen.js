import React, { useState, useEffect, useContext } from 'react';
import {
  View,
  Text,
  ScrollView,
  StyleSheet,
  SafeAreaView,
  ActivityIndicator,
  Alert
} from 'react-native';
import { UserContext } from '../UserContext';
import { getUserProgress } from '../api';

export default function ProgressScreen({ navigation }) {
  const { token } = useContext(UserContext);
  const [progressData, setProgressData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadProgress();
  }, []);

  const loadProgress = async () => {
    try {
      const data = await getUserProgress(token);
      setProgressData(data);
    } catch (error) {
      Alert.alert('Error', 'Failed to load progress data');
    } finally {
      setLoading(false);
    }
  };

  const renderSubjectProgress = () => {
    if (!progressData?.by_subject) return null;

    return Object.entries(progressData.by_subject).map(([subject, stats]) => (
      <View key={subject} style={styles.subjectCard}>
        <View style={styles.subjectHeader}>
          <Text style={styles.subjectName}>{subject}</Text>
          <Text style={styles.subjectAccuracy}>{stats.accuracy_percent.toFixed(1)}%</Text>
        </View>
        <View style={styles.progressBar}>
          <View
            style={[
              styles.progressFill,
              { width: `${stats.accuracy_percent}%` },
              { backgroundColor: getAccuracyColor(stats.accuracy_percent) }
            ]}
          />
        </View>
        <Text style={styles.subjectStats}>
          {stats.correct}/{stats.attempted} correct
        </Text>
      </View>
    ));
  };

  const renderExamBoardProgress = () => {
    if (!progressData?.by_exam_board) return null;

    return Object.entries(progressData.by_exam_board).map(([board, stats]) => (
      <View key={board} style={styles.boardCard}>
        <Text style={styles.boardName}>{board}</Text>
        <Text style={styles.boardStats}>
          {stats.correct}/{stats.attempted} ({stats.accuracy_percent.toFixed(1)}%)
        </Text>
      </View>
    ));
  };

  const renderWeakTopics = () => {
    if (!progressData?.weak_topics || progressData.weak_topics.length === 0) return null;

    return (
      <View style={styles.weakTopicsCard}>
        <Text style={styles.sectionTitle}>Topics Needing Improvement</Text>
        {progressData.weak_topics.map((topic, index) => (
          <View key={index} style={styles.weakTopicItem}>
            <Text style={styles.weakTopicName}>{topic.topic}</Text>
            <Text style={styles.weakTopicAccuracy}>
              {topic.accuracy_percent.toFixed(1)}% ({topic.questions_attempted} attempts)
            </Text>
          </View>
        ))}
      </View>
    );
  };

  const getAccuracyColor = (percentage) => {
    if (percentage >= 80) return '#27ae60';
    if (percentage >= 60) return '#f39c12';
    return '#e74c3c';
  };

  if (loading) {
    return (
      <SafeAreaView style={styles.container}>
        <View style={styles.loadingContainer}>
          <ActivityIndicator size="large" color="#3498db" />
          <Text style={styles.loadingText}>Loading your progress...</Text>
        </View>
      </SafeAreaView>
    );
  }

  if (!progressData) {
    return (
      <SafeAreaView style={styles.container}>
        <View style={styles.loadingContainer}>
          <Text style={styles.loadingText}>No progress data available</Text>
        </View>
      </SafeAreaView>
    );
  }

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView style={styles.scrollView} showsVerticalScrollIndicator={false}>
        <Text style={styles.title}>Your Progress</Text>

        {/* Overall Stats */}
        <View style={styles.overallCard}>
          <Text style={styles.overallAccuracy}>
            {progressData.accuracy_percent.toFixed(1)}%
          </Text>
          <Text style={styles.overallLabel}>Overall Accuracy</Text>
          <Text style={styles.overallStats}>
            {progressData.total_correct}/{progressData.total_questions_attempted} questions correct
          </Text>
          {progressData.streak_days > 0 && (
            <Text style={styles.streakText}>
              🔥 {progressData.streak_days} day streak!
            </Text>
          )}
        </View>

        {/* Exam Board Progress */}
        <View style={styles.sectionCard}>
          <Text style={styles.sectionTitle}>By Exam Board</Text>
          {renderExamBoardProgress()}
        </View>

        {/* Subject Progress */}
        <View style={styles.sectionCard}>
          <Text style={styles.sectionTitle}>By Subject</Text>
          {renderSubjectProgress()}
        </View>

        {/* Weak Topics */}
        {renderWeakTopics()}

        {/* Action Buttons */}
        <View style={styles.actionsCard}>
          <Text style={styles.sectionTitle}>Continue Learning</Text>
          <View style={styles.buttonRow}>
            <TouchableOpacity
              style={styles.actionButton}
              onPress={() => navigation.navigate('Search')}
            >
              <Text style={styles.actionButtonText}>Practice Questions</Text>
            </TouchableOpacity>
            <TouchableOpacity
              style={[styles.actionButton, styles.quizButton]}
              onPress={() => navigation.navigate('Quiz', { mode: 'quiz', count: 15 })}
            >
              <Text style={styles.quizButtonText}>Take Quiz</Text>
            </TouchableOpacity>
          </View>
        </View>
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
    padding: 15,
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  loadingText: {
    fontSize: 16,
    color: '#666',
    marginTop: 10,
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 20,
    textAlign: 'center',
  },
  overallCard: {
    backgroundColor: '#fff',
    borderRadius: 12,
    padding: 20,
    alignItems: 'center',
    marginBottom: 20,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  overallAccuracy: {
    fontSize: 48,
    fontWeight: 'bold',
    color: '#3498db',
    marginBottom: 5,
  },
  overallLabel: {
    fontSize: 16,
    color: '#666',
    marginBottom: 10,
  },
  overallStats: {
    fontSize: 14,
    color: '#666',
    textAlign: 'center',
  },
  streakText: {
    fontSize: 16,
    color: '#e74c3c',
    fontWeight: 'bold',
    marginTop: 10,
  },
  sectionCard: {
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
  sectionTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 15,
  },
  boardCard: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingVertical: 10,
    borderBottomWidth: 1,
    borderBottomColor: '#f0f0f0',
  },
  boardName: {
    fontSize: 16,
    fontWeight: '600',
    color: '#333',
  },
  boardStats: {
    fontSize: 14,
    color: '#666',
  },
  subjectCard: {
    marginBottom: 15,
    padding: 15,
    backgroundColor: '#f9f9f9',
    borderRadius: 8,
  },
  subjectHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 8,
  },
  subjectName: {
    fontSize: 16,
    fontWeight: '600',
    color: '#333',
    flex: 1,
  },
  subjectAccuracy: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#3498db',
  },
  progressBar: {
    height: 8,
    backgroundColor: '#e0e0e0',
    borderRadius: 4,
    marginBottom: 8,
  },
  progressFill: {
    height: '100%',
    borderRadius: 4,
  },
  subjectStats: {
    fontSize: 12,
    color: '#666',
    textAlign: 'right',
  },
  weakTopicsCard: {
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
  weakTopicItem: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingVertical: 8,
    borderBottomWidth: 1,
    borderBottomColor: '#f0f0f0',
  },
  weakTopicName: {
    fontSize: 16,
    color: '#333',
    flex: 1,
  },
  weakTopicAccuracy: {
    fontSize: 14,
    color: '#e74c3c',
    fontWeight: '600',
  },
  actionsCard: {
    backgroundColor: '#fff',
    borderRadius: 12,
    padding: 20,
    marginBottom: 30,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  buttonRow: {
    flexDirection: 'row',
    gap: 10,
  },
  actionButton: {
    flex: 1,
    backgroundColor: '#3498db',
    padding: 12,
    borderRadius: 6,
    alignItems: 'center',
  },
  actionButtonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
  },
  quizButton: {
    backgroundColor: '#27ae60',
  },
  quizButtonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
  },
});