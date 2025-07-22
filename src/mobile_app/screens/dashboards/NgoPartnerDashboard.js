
import React from 'react';
import { View, Text, StyleSheet, Button, ActivityIndicator, ScrollView } from 'react-native';
import { Ionicons, MaterialCommunityIcons } from '@expo/vector-icons';
import { useFetch } from '../../hooks/useFetch';


export default function NgoPartnerDashboard({ navigation, route }) {
  const { firstName, role } = route.params || {};
  // Simulate fetch for demo (replace with real endpoint if available)
  const { data, loading, error, refetch } = useFetch('https://demo.akulearn/api/ngo-impact', {}, false); // disabled for now
  // Demo data
  const totalStudents = 120000;
  const passRate = 18;
  const schools = 320;

  return (
    <ScrollView contentContainerStyle={styles.container}>
      <Text style={styles.title}>
        <MaterialCommunityIcons name="hand-heart" size={28} color="#007bff" />
        {' '}Welcome, NGO Partner!
      </Text>
      {loading && <ActivityIndicator size="large" color="#007bff" style={{ marginVertical: 20 }} />}
      {error && (
        <View style={styles.errorBox}>
          <Ionicons name="alert-circle" size={20} color="#d9534f" />
          <Text style={styles.errorText}>{error}</Text>
          <Button title="Retry" onPress={refetch} color="#007bff" />
        </View>
      )}
      <Text style={styles.sectionTitle}>Program Reach & Effectiveness</Text>
      <View style={styles.metricsRow}>
        <View style={styles.metricBox}>
          <Ionicons name="people" size={32} color="#007bff" />
          <Text style={styles.metricNumber}>{totalStudents.toLocaleString()}</Text>
          <Text style={styles.metricLabel}>Total Students Reached</Text>
        </View>
        <View style={styles.metricBox}>
          <Ionicons name="school" size={32} color="#28a745" />
          <Text style={styles.metricNumber}>{schools}</Text>
          <Text style={styles.metricLabel}>Schools Impacted</Text>
        </View>
        <View style={styles.metricBox}>
          <Ionicons name="trending-up" size={32} color="#ffc107" />
          <Text style={styles.metricNumber}>{passRate}%</Text>
          <Text style={styles.metricLabel}>Exam Pass Rate ↑</Text>
        </View>
      </View>
      <Text style={styles.sectionTitle}>Program Reach & Effectiveness</Text>
      <Text style={{ color: '#888', marginBottom: 10 }}>Program Reach & Effectiveness (coming soon)</Text>
      <Button title="Logout" onPress={() => navigation.navigate('LoginScreen')} color="#d9534f" />
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { flexGrow: 1, padding: 20, backgroundColor: '#f9fafe' },
  title: { fontSize: 24, fontWeight: 'bold', marginBottom: 20, color: '#007bff', flexDirection: 'row', alignItems: 'center' },
  sectionTitle: { fontSize: 18, fontWeight: 'bold', marginTop: 24, marginBottom: 10, color: '#333' },
  metricsRow: { flexDirection: 'row', justifyContent: 'space-between', marginBottom: 20 },
  metricBox: { alignItems: 'center', flex: 1, marginHorizontal: 8, padding: 12, backgroundColor: '#f7faff', borderRadius: 8, elevation: 1 },
  metricNumber: { fontSize: 28, fontWeight: 'bold', color: '#007bff', marginTop: 4 },
  metricLabel: { fontSize: 13, color: '#555', textAlign: 'center' },
  errorBox: { backgroundColor: '#f8d7da', padding: 10, borderRadius: 8, marginBottom: 10, flexDirection: 'row', alignItems: 'center' },
  errorText: { color: '#d9534f', marginLeft: 8, flex: 1 },
});
