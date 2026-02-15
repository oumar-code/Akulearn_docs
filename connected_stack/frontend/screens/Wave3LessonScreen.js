import React, { useState, useContext, useEffect } from 'react';
import {
  View,
  Text,
  TouchableOpacity,
  StyleSheet,
  ActivityIndicator,
  SafeAreaView,
  ScrollView,
} from 'react-native';
import { UserContext } from '../UserContext';
import {
  getWave3Lesson,
  recordWave3Activity,
  getWave3Mastery,
  recordWave3Interaction,
  createWave3WebSocket,
} from '../api';

export default function Wave3LessonScreen({ route, navigation }) {
  const { lessonId } = route.params;
  const { user } = useContext(UserContext);
  const [lesson, setLesson] = useState(null);
  const [mastery, setMastery] = useState(null);
  const [loading, setLoading] = useState(true);
  const [activeSection, setActiveSection] = useState('overview');
  const [startTime] = useState(Date.now());
  const [webSocket, setWebSocket] = useState(null);

  useEffect(() => {
    loadLesson();
    loadMastery();
    setupWebSocket();

    return () => {
      // Record activity when leaving
      recordActivity();
      if (webSocket) {
        webSocket.close();
      }
    };
  }, []);

  const setupWebSocket = () => {
    const studentId = user?.id || 'student_001';
    const ws = createWave3WebSocket(
      studentId,
      handleWebSocketMessage,
      (error) => console.error('WebSocket error:', error)
    );
    setWebSocket(ws);
  };

  const handleWebSocketMessage = (data) => {
    if (data.type === 'mastery_update' && data.lesson_id === lessonId) {
      setMastery(data.mastery_data);
    }
  };

  const loadLesson = async () => {
    try {
      const data = await getWave3Lesson(lessonId, user?.token);
      setLesson(data);
      
      // Record view interaction
      const studentId = user?.id || 'student_001';
      await recordWave3Interaction(
        studentId,
        lessonId,
        'view',
        { source: 'lesson_detail' },
        user?.token
      );
    } catch (err) {
      console.error('Failed to load lesson:', err);
    } finally {
      setLoading(false);
    }
  };

  const loadMastery = async () => {
    try {
      const studentId = user?.id || 'student_001';
      const masteryData = await getWave3Mastery(studentId, lessonId, user?.token);
      setMastery(masteryData);
    } catch (err) {
      console.error('Failed to load mastery:', err);
    }
  };

  const recordActivity = async () => {
    try {
      const studentId = user?.id || 'student_001';
      const duration = Math.floor((Date.now() - startTime) / 1000);
      
      await recordWave3Activity(
        {
          student_id: studentId,
          lesson_id: lessonId,
          activity_type: 'study',
          duration_seconds: duration,
          metadata: { section: activeSection },
        },
        user?.token
      );
    } catch (err) {
      console.error('Failed to record activity:', err);
    }
  };

  const handleStartQuiz = () => {
    navigation.navigate('Wave3Quiz', { lessonId });
  };

  if (loading) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color="#3498db" />
        <Text style={styles.loadingText}>Loading lesson...</Text>
      </View>
    );
  }

  if (!lesson) {
    return (
      <View style={styles.errorContainer}>
        <Text style={styles.errorText}>Lesson not found</Text>
        <TouchableOpacity style={styles.button} onPress={() => navigation.goBack()}>
          <Text style={styles.buttonText}>Go Back</Text>
        </TouchableOpacity>
      </View>
    );
  }

  return (
    <SafeAreaView style={styles.container}>
      {/* Header */}
      <View style={styles.header}>
        <Text style={styles.headerSubject}>{lesson.subject}</Text>
        <Text style={styles.headerTitle}>{lesson.title}</Text>
        <View style={styles.headerMeta}>
          <Text style={styles.metaText}>⏱️ {lesson.duration_minutes} min</Text>
          <Text style={styles.metaText}>📊 {lesson.difficulty_level}</Text>
        </View>
      </View>

      {/* Mastery Progress */}
      {mastery && (
        <View style={styles.masteryContainer}>
          <View style={styles.masteryHeader}>
            <Text style={styles.masteryTitle}>Your Progress</Text>
            <Text style={styles.masteryLevel}>{mastery.mastery_level}</Text>
          </View>
          <View style={styles.masteryBar}>
            <View
              style={[
                styles.masteryFill,
                { width: `${mastery.mastery_percentage}%` },
              ]}
            />
          </View>
          <Text style={styles.masteryText}>
            {Math.round(mastery.mastery_percentage)}% Mastery
          </Text>
        </View>
      )}

      {/* Tab Navigation */}
      <View style={styles.tabContainer}>
        {['overview', 'content', 'examples', 'practice'].map((tab) => (
          <TouchableOpacity
            key={tab}
            style={[styles.tab, activeSection === tab && styles.tabActive]}
            onPress={() => setActiveSection(tab)}
          >
            <Text
              style={[
                styles.tabText,
                activeSection === tab && styles.tabTextActive,
              ]}
            >
              {tab.charAt(0).toUpperCase() + tab.slice(1)}
            </Text>
          </TouchableOpacity>
        ))}
      </View>

      <ScrollView style={styles.scrollView}>
        {/* Overview Tab */}
        {activeSection === 'overview' && (
          <View style={styles.section}>
            <Text style={styles.sectionTitle}>Description</Text>
            <Text style={styles.description}>{lesson.description}</Text>

            <Text style={styles.sectionTitle}>Learning Objectives</Text>
            {lesson.learning_objectives?.map((objective, index) => (
              <View key={index} style={styles.listItem}>
                <Text style={styles.listBullet}>•</Text>
                <Text style={styles.listText}>{objective}</Text>
              </View>
            ))}

            <Text style={styles.sectionTitle}>NERDC Codes</Text>
            <View style={styles.tags}>
              {lesson.nerdc_codes?.map((code, index) => (
                <View key={index} style={styles.tag}>
                  <Text style={styles.tagText}>{code}</Text>
                </View>
              ))}
            </View>

            <Text style={styles.sectionTitle}>Keywords</Text>
            <View style={styles.tags}>
              {lesson.keywords?.map((keyword, index) => (
                <View key={index} style={[styles.tag, styles.keywordTag]}>
                  <Text style={styles.keywordText}>{keyword}</Text>
                </View>
              ))}
            </View>
          </View>
        )}

        {/* Content Tab */}
        {activeSection === 'content' && (
          <View style={styles.section}>
            {lesson.content_sections?.map((section, index) => (
              <View key={index} style={styles.contentSection}>
                <Text style={styles.contentTitle}>{section.title}</Text>
                <Text style={styles.contentBody}>{section.content}</Text>
              </View>
            ))}
          </View>
        )}

        {/* Examples Tab */}
        {activeSection === 'examples' && (
          <View style={styles.section}>
            {lesson.worked_examples?.map((example, index) => (
              <View key={index} style={styles.exampleCard}>
                <Text style={styles.exampleTitle}>Example {index + 1}</Text>
                <Text style={styles.exampleProblem}>{example.problem}</Text>
                <Text style={styles.exampleLabel}>Solution:</Text>
                <Text style={styles.exampleSolution}>{example.solution}</Text>
                {example.explanation && (
                  <>
                    <Text style={styles.exampleLabel}>Explanation:</Text>
                    <Text style={styles.exampleExplanation}>
                      {example.explanation}
                    </Text>
                  </>
                )}
              </View>
            ))}
          </View>
        )}

        {/* Practice Tab */}
        {activeSection === 'practice' && (
          <View style={styles.section}>
            <Text style={styles.practiceInfo}>
              Test your understanding with {lesson.practice_problems?.length || 0}{' '}
              practice questions
            </Text>
            <TouchableOpacity
              style={styles.startQuizButton}
              onPress={handleStartQuiz}
            >
              <Text style={styles.startQuizText}>Start Practice Quiz</Text>
            </TouchableOpacity>

            <Text style={styles.sectionTitle}>Problem Types</Text>
            {lesson.practice_problems?.slice(0, 3).map((problem, index) => (
              <View key={index} style={styles.problemPreview}>
                <Text style={styles.problemText} numberOfLines={2}>
                  {index + 1}. {problem.question}
                </Text>
              </View>
            ))}
          </View>
        )}
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  loadingText: {
    marginTop: 10,
    fontSize: 16,
    color: '#666',
  },
  errorContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 20,
  },
  errorText: {
    fontSize: 16,
    color: '#e74c3c',
    textAlign: 'center',
    marginBottom: 20,
  },
  header: {
    backgroundColor: '#3498db',
    padding: 20,
  },
  headerSubject: {
    fontSize: 14,
    color: '#fff',
    opacity: 0.9,
  },
  headerTitle: {
    fontSize: 22,
    fontWeight: 'bold',
    color: '#fff',
    marginTop: 5,
  },
  headerMeta: {
    flexDirection: 'row',
    marginTop: 10,
  },
  metaText: {
    fontSize: 14,
    color: '#fff',
    marginRight: 15,
  },
  masteryContainer: {
    backgroundColor: '#fff',
    padding: 15,
    borderBottomWidth: 1,
    borderBottomColor: '#e0e0e0',
  },
  masteryHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 10,
  },
  masteryTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: '#333',
  },
  masteryLevel: {
    fontSize: 14,
    fontWeight: 'bold',
    color: '#4CAF50',
    backgroundColor: '#E8F5E9',
    paddingHorizontal: 10,
    paddingVertical: 4,
    borderRadius: 4,
  },
  masteryBar: {
    height: 8,
    backgroundColor: '#e0e0e0',
    borderRadius: 4,
    overflow: 'hidden',
    marginBottom: 5,
  },
  masteryFill: {
    height: '100%',
    backgroundColor: '#4CAF50',
  },
  masteryText: {
    fontSize: 12,
    color: '#666',
    textAlign: 'center',
  },
  tabContainer: {
    flexDirection: 'row',
    backgroundColor: '#fff',
    borderBottomWidth: 1,
    borderBottomColor: '#e0e0e0',
  },
  tab: {
    flex: 1,
    padding: 15,
    alignItems: 'center',
  },
  tabActive: {
    borderBottomWidth: 3,
    borderBottomColor: '#3498db',
  },
  tabText: {
    fontSize: 14,
    color: '#666',
  },
  tabTextActive: {
    color: '#3498db',
    fontWeight: '600',
  },
  scrollView: {
    flex: 1,
  },
  section: {
    padding: 20,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#333',
    marginTop: 20,
    marginBottom: 10,
  },
  description: {
    fontSize: 16,
    color: '#666',
    lineHeight: 24,
  },
  listItem: {
    flexDirection: 'row',
    marginBottom: 8,
  },
  listBullet: {
    fontSize: 16,
    color: '#3498db',
    marginRight: 10,
  },
  listText: {
    flex: 1,
    fontSize: 16,
    color: '#666',
    lineHeight: 22,
  },
  tags: {
    flexDirection: 'row',
    flexWrap: 'wrap',
  },
  tag: {
    backgroundColor: '#e3f2fd',
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 4,
    marginRight: 8,
    marginBottom: 8,
  },
  tagText: {
    fontSize: 13,
    color: '#1976d2',
  },
  keywordTag: {
    backgroundColor: '#f3e5f5',
  },
  keywordText: {
    fontSize: 13,
    color: '#7b1fa2',
  },
  contentSection: {
    marginBottom: 25,
  },
  contentTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 10,
  },
  contentBody: {
    fontSize: 16,
    color: '#666',
    lineHeight: 24,
  },
  exampleCard: {
    backgroundColor: '#fff',
    padding: 15,
    borderRadius: 8,
    marginBottom: 15,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  exampleTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#3498db',
    marginBottom: 10,
  },
  exampleProblem: {
    fontSize: 16,
    color: '#333',
    marginBottom: 10,
  },
  exampleLabel: {
    fontSize: 14,
    fontWeight: '600',
    color: '#666',
    marginTop: 10,
    marginBottom: 5,
  },
  exampleSolution: {
    fontSize: 15,
    color: '#4CAF50',
    lineHeight: 22,
  },
  exampleExplanation: {
    fontSize: 15,
    color: '#666',
    lineHeight: 22,
  },
  practiceInfo: {
    fontSize: 16,
    color: '#666',
    textAlign: 'center',
    marginBottom: 20,
  },
  startQuizButton: {
    backgroundColor: '#4CAF50',
    padding: 18,
    borderRadius: 10,
    alignItems: 'center',
    marginBottom: 20,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.2,
    shadowRadius: 4,
    elevation: 5,
  },
  startQuizText: {
    color: '#fff',
    fontSize: 18,
    fontWeight: 'bold',
  },
  problemPreview: {
    backgroundColor: '#f8f9fa',
    padding: 12,
    borderRadius: 6,
    marginBottom: 10,
  },
  problemText: {
    fontSize: 14,
    color: '#666',
  },
  button: {
    backgroundColor: '#3498db',
    padding: 15,
    borderRadius: 8,
    alignItems: 'center',
  },
  buttonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
  },
});
