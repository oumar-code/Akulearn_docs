import React, { useEffect, useState } from 'react';
import { View, Text, Button, StyleSheet, TouchableOpacity, ActivityIndicator } from 'react-native';
import { Ionicons } from '@expo/vector-icons';

export default function StudentDashboard({ navigation, route }) {
  const { firstName, role, userId } = route.params || {};
  const [progress, setProgress] = useState(null);
  const [lastTopic, setLastTopic] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchProgress() {
      try {
        // Replace with actual backend API URLs
        const progressRes = await fetch(`https://your-backend-api/user/progress/${userId}`);
        const progressData = await progressRes.json();
        const topicRes = await fetch(`https://your-backend-api/user/last_accessed_topic?user_id=${userId}`);
        const topicData = await topicRes.json();
        setProgress(progressData);
        setLastTopic(topicData);
      } catch (error) {
        // Handle error
      } finally {
        setLoading(false);
      }
    }
    if (userId) fetchProgress();
  }, [userId]);

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Student Portal</Text>
      <Text style={styles.welcome}>Welcome, {firstName || 'User'}! You are logged in as a {role || 'student'}.</Text>
      <View style={styles.navRow}>
        <TouchableOpacity style={styles.navButton} onPress={() => navigation.navigate('LearningModulesScreen')}>
          <Ionicons name="book" size={32} color="#007bff" />
          <Text>My Learning Modules</Text>
        </TouchableOpacity>
        <TouchableOpacity style={styles.navButton} onPress={() => navigation.navigate('AITutorChatScreen')}>
          <Ionicons name="chatbubbles" size={32} color="#28a745" />
          <Text>AI Tutor Chat</Text>
        </TouchableOpacity>
      </View>
      <TouchableOpacity style={styles.progressButton} onPress={() => {}}>
        <Ionicons name="stats-chart" size={28} color="#ffc107" />
        <Text>My Progress</Text>
      </TouchableOpacity>
      {loading ? <ActivityIndicator size="large" /> : progress && (
        <View style={styles.progressWidget}>
          <Text>Total Topics Completed: {progress.total_topics_completed}</Text>
          <Text>Total Modules Completed: {progress.total_modules_completed}</Text>
          <View style={styles.progressBarContainer}>
            <View style={{...styles.progressBar, width: `${progress.percent_complete || 0}%`}} />
          </View>
          <Text>Overall Progress: {progress.percent_complete || 0}%</Text>
        </View>
      )}
      {lastTopic && (
        <View style={styles.nextLessonWidget}>
          <Text style={styles.sectionTitle}>Continue Learning</Text>
          <Text>Last Accessed Topic: {lastTopic.topic_name}</Text>
          <Button title="Resume" onPress={() => {}} />
        </View>
      )}
      <Button title="Logout" onPress={() => navigation.navigate('LoginScreen')} color="#d9534f" />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 20 },
  title: { fontSize: 24, fontWeight: 'bold', marginBottom: 20 },
  welcome: { fontSize: 18, marginBottom: 20 },
  navRow: { flexDirection: 'row', justifyContent: 'space-around', marginBottom: 20 },
  navButton: { alignItems: 'center', padding: 10 },
  progressButton: { alignItems: 'center', marginBottom: 20 },
  progressWidget: { padding: 10, borderWidth: 1, borderColor: '#ccc', borderRadius: 5, marginBottom: 20 },
  progressBarContainer: { height: 10, backgroundColor: '#eee', borderRadius: 5, overflow: 'hidden', marginVertical: 10 },
  progressBar: { height: 10, backgroundColor: '#007bff', borderRadius: 5 },
  nextLessonWidget: { padding: 10, borderWidth: 1, borderColor: '#ccc', borderRadius: 5, marginBottom: 20 },
  sectionTitle: { fontSize: 18, fontWeight: 'bold', marginBottom: 10 },
});
