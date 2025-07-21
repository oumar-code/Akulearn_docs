import React, { useEffect, useState } from 'react';
import { View, Text, StyleSheet, ActivityIndicator } from 'react-native';
import { Ionicons } from '@expo/vector-icons';

export default function StudentProgressViewScreen({ route }) {
  const { studentId } = route.params;
  const [progress, setProgress] = useState(null);
  const [examResults, setExamResults] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchData() {
      try {
        const progressRes = await fetch(`https://your-backend-api/user/progress/${studentId}`);
        const progressData = await progressRes.json();
        const examRes = await fetch(`https://your-backend-api/user/exam_results/${studentId}`);
        const examData = await examRes.json();
        setProgress(progressData);
        setExamResults(examData);
      } catch (error) {
        // Handle error
      } finally {
        setLoading(false);
      }
    }
    fetchData();
  }, [studentId]);

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Student Progress</Text>
      {loading ? <ActivityIndicator size="large" /> : (
        <>
          {progress && (
            <View style={styles.progressWidget}>
              <Text>Total Topics Completed: {progress.total_topics_completed}</Text>
              <Text>Total Modules Completed: {progress.total_modules_completed}</Text>
              <View style={styles.progressBarContainer}>
                <View style={{...styles.progressBar, width: `${progress.percent_complete || 0}%`}} />
              </View>
              <Text>Overall Progress: {progress.percent_complete || 0}%</Text>
            </View>
          )}
          {examResults && (
            <View style={styles.examWidget}>
              <Text style={styles.sectionTitle}>Exam Results</Text>
              {examResults.results.map((result, idx) => (
                <Text key={idx}>{result.exam_name}: {result.score}%</Text>
              ))}
            </View>
          )}
        </>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 20 },
  title: { fontSize: 22, fontWeight: 'bold', marginBottom: 20 },
  progressWidget: { padding: 10, borderWidth: 1, borderColor: '#ccc', borderRadius: 5, marginBottom: 20 },
  progressBarContainer: { height: 10, backgroundColor: '#eee', borderRadius: 5, overflow: 'hidden', marginVertical: 10 },
  progressBar: { height: 10, backgroundColor: '#007bff', borderRadius: 5 },
  examWidget: { padding: 10, borderWidth: 1, borderColor: '#ccc', borderRadius: 5, marginBottom: 20 },
  sectionTitle: { fontSize: 18, fontWeight: 'bold', marginBottom: 10 },
});
