import React from 'react';
import { View, Text, Button, StyleSheet, TouchableOpacity, ActivityIndicator, Dimensions, ScrollView } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import * as Progress from 'react-native-progress';
import { BarChart } from 'react-native-chart-kit';
import { useFetch } from '../../hooks/useFetch';

export default function StudentDashboard({ navigation, route }) {
  const { firstName, role, userId } = route.params || {};
  const { data: progress, loading: loadingProgress, error: errorProgress } = useFetch(userId ? `https://your-backend-api/user/progress/${userId}` : null, {}, !!userId);
  const { data: lastTopic, loading: loadingTopic, error: errorTopic } = useFetch(userId ? `https://your-backend-api/user/last_accessed_topic?user_id=${userId}` : null, {}, !!userId);

  // Dummy data for 'Topics Completed This Week' bar chart
  const weeklyTopicsData = {
    labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
    datasets: [
      {
        data: [2, 1, 3, 0, 2, 1, 2], // Example: topics completed per day
      },
    ],
  };
  const screenWidth = Dimensions.get('window').width - 40;

  return (
    <ScrollView contentContainerStyle={styles.container}>
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
      {(errorProgress || errorTopic) && <Text style={styles.errorText}>{errorProgress || errorTopic}</Text>}
      {(loadingProgress || loadingTopic) ? <ActivityIndicator size="large" /> : progress && (
        <View style={styles.progressWidget}>
          <Text style={styles.sectionTitle}>Your Progress</Text>
          <View style={{alignItems: 'center', marginVertical: 10}}>
            <Progress.Circle
              size={90}
              progress={(progress.percent_complete || 0) / 100}
              showsText={true}
              formatText={() => `${progress.percent_complete || 0}%`}
              color="#007bff"
              thickness={8}
            />
          </View>
          <Text>Total Topics Completed: {progress.total_topics_completed}</Text>
          <Text>Total Modules Completed: {progress.total_modules_completed}</Text>
        </View>
      )}
      <View style={styles.chartWidget}>
        <Text style={styles.sectionTitle}>Topics Completed This Week</Text>
        <BarChart
          data={weeklyTopicsData}
          width={screenWidth}
          height={180}
          yAxisLabel=""
          chartConfig={{
            backgroundColor: '#fff',
            backgroundGradientFrom: '#fff',
            backgroundGradientTo: '#fff',
            decimalPlaces: 0,
            color: (opacity = 1) => `rgba(0, 123, 255, ${opacity})`,
            labelColor: (opacity = 1) => `rgba(0,0,0,${opacity})`,
            style: { borderRadius: 8 },
            propsForDots: { r: '6', strokeWidth: '2', stroke: '#007bff' },
          }}
          style={{ borderRadius: 8 }}
          fromZero
          showValuesOnTopOfBars
        />
      </View>
      {lastTopic && (
        <View style={styles.nextLessonWidget}>
          <Text style={styles.sectionTitle}>Continue Learning</Text>
          <Text>Last Accessed Topic: {lastTopic.topic_name}</Text>
          <Button title="Resume" onPress={() => {}} />
        </View>
      )}
      <Button title="Logout" onPress={() => navigation.navigate('LoginScreen')} color="#d9534f" />
    </ScrollView>
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

  chartWidget: { padding: 10, borderWidth: 1, borderColor: '#e3e3e3', borderRadius: 5, marginBottom: 20, backgroundColor: '#fafbff' },
  errorText: { color: '#d9534f', fontSize: 16, marginBottom: 10 },
  nextLessonWidget: { padding: 10, borderWidth: 1, borderColor: '#ccc', borderRadius: 5, marginBottom: 20 },
  sectionTitle: { fontSize: 18, fontWeight: 'bold', marginBottom: 10 },
});
