import React from 'react';
import { View, Text, StyleSheet, Button } from 'react-native';
import { Ionicons } from '@expo/vector-icons';

export default function CorporateDashboard({ navigation, route }) {
  const { firstName, role } = route.params || {};
  // Dummy data
  const totalStudents = 120000;
  const passRate = 18;
  const schools = 320;

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Welcome, Corporate Partner!</Text>
      <Text style={styles.sectionTitle}>CSR Impact Dashboard</Text>
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
      <Text>Program Reach & Effectiveness (coming soon)</Text>
      <Button title="Logout" onPress={() => navigation.navigate('LoginScreen')} color="#d9534f" />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 20 },
  title: { fontSize: 24, fontWeight: 'bold', marginBottom: 20 },

  sectionTitle: { fontSize: 18, fontWeight: 'bold', marginTop: 20, marginBottom: 10 },
  metricsRow: { flexDirection: 'row', justifyContent: 'space-between', marginBottom: 20 },
  metricBox: { alignItems: 'center', flex: 1, marginHorizontal: 8, padding: 12, backgroundColor: '#f7faff', borderRadius: 8, elevation: 1 },
  metricNumber: { fontSize: 28, fontWeight: 'bold', color: '#007bff', marginTop: 4 },
  metricLabel: { fontSize: 13, color: '#555', textAlign: 'center' },
});
