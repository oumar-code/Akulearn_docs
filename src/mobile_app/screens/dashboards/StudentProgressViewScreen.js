import React from 'react';
import { View, Text, StyleSheet, ActivityIndicator, ScrollView } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import * as Progress from 'react-native-progress';
import { useFetch } from '../../hooks/useFetch';

  const { studentId } = route.params;
  const { data: progress, loading: loadingProgress, error: errorProgress } = useFetch(studentId ? `https://your-backend-api/user/progress/${studentId}` : null, null, !!studentId);
  const { data: examResults, loading: loadingExam, error: errorExam } = useFetch(studentId ? `https://your-backend-api/user/exam_results/${studentId}` : null, null, !!studentId);

  const loading = loadingProgress || loadingExam;
  const error = errorProgress || errorExam;

  return (
    <ScrollView contentContainerStyle={styles.container}>
      <Text style={styles.title}>Student Progress</Text>
      {error && <Text style={styles.errorText}>{error}</Text>}
      {loading ? <ActivityIndicator size="large" /> : (
        <>
          {progress && (
            <View style={styles.progressWidget}>
              <Text style={styles.sectionTitle}>Progress Overview</Text>
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
          {examResults && (
            <View style={styles.examWidget}>
              <Text style={styles.sectionTitle}>Exam Results</Text>
              <View style={styles.examTableHeader}>
                <Text style={[styles.examCell, styles.examHeader]}>Exam</Text>
                <Text style={[styles.examCell, styles.examHeader]}>Score</Text>
              </View>
              {examResults.results && examResults.results.map((result, idx) => (
                <View key={idx} style={styles.examTableRow}>
                  <Text style={styles.examCell}>{result.exam_name}</Text>
                  <Text style={styles.examCell}>{result.score}%</Text>
                </View>
              ))}
            </View>
          )}
        </>
      )}
    </ScrollView>
  );


const styles = StyleSheet.create({
  container: { flex: 1, padding: 20 },
  title: { fontSize: 22, fontWeight: 'bold', marginBottom: 20 },
  progressWidget: { padding: 10, borderWidth: 1, borderColor: '#ccc', borderRadius: 5, marginBottom: 20 },
  progressBarContainer: { height: 10, backgroundColor: '#eee', borderRadius: 5, overflow: 'hidden', marginVertical: 10 },
  progressBar: { height: 10, backgroundColor: '#007bff', borderRadius: 5 },

  examWidget: { padding: 10, borderWidth: 1, borderColor: '#ccc', borderRadius: 5, marginBottom: 20 },
  examTableHeader: { flexDirection: 'row', borderBottomWidth: 1, borderColor: '#e3e3e3', paddingBottom: 4, marginBottom: 4 },
  examTableRow: { flexDirection: 'row', borderBottomWidth: 0.5, borderColor: '#f0f0f0', paddingVertical: 2 },
  examCell: { flex: 1, fontSize: 15 },
  examHeader: { fontWeight: 'bold' },
  sectionTitle: { fontSize: 18, fontWeight: 'bold', marginBottom: 10 },
});
