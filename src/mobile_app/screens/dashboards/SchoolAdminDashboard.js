import React, { useEffect, useState } from 'react';
import { View, Text, Button, StyleSheet, FlatList, ActivityIndicator } from 'react-native';
import * as Progress from 'react-native-progress';
import { Ionicons } from '@expo/vector-icons';

export default function SchoolAdminDashboard({ navigation, route }) {
  const { firstName, role, schoolId } = route.params || {};
  const [school, setSchool] = useState(null);
  const [loading, setLoading] = useState(true);
  // Placeholder for teachers/students
  const [teachers, setTeachers] = useState([]);
  const [students, setStudents] = useState([]);

  useEffect(() => {
    async function fetchSchool() {
      try {
        // Replace with actual backend API URL
        const response = await fetch(`https://your-backend-api/schools/${schoolId}`);
        const data = await response.json();
        if (response.ok) setSchool(data);
      } catch (error) {
        // Handle error
      } finally {
        setLoading(false);
      }
    }
    if (schoolId) fetchSchool();
  }, [schoolId]);

  // Dummy data
  const totalStudents = 420;
  const activeUsers = 390;
  const completionPercent = 0.76; // 76%
  const projectorHubs = [
    { id: 1, name: 'Hub A', status: 'online' },
    { id: 2, name: 'Hub B', status: 'offline' },
    { id: 3, name: 'Hub C', status: 'online' },
  ];

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Welcome, School Admin {firstName || 'User'}!</Text>
      {/* Enrollment Overview */}
      <Text style={styles.sectionTitle}>Enrollment Overview</Text>
      <View style={styles.metricsRow}>
        <View style={styles.metricBox}>
          <Ionicons name="people" size={32} color="#007bff" />
          <Text style={styles.metricNumber}>{totalStudents}</Text>
          <Text style={styles.metricLabel}>Total Students</Text>
        </View>
        <View style={styles.metricBox}>
          <Ionicons name="person" size={32} color="#28a745" />
          <Text style={styles.metricNumber}>{activeUsers}</Text>
          <Text style={styles.metricLabel}>Active Users</Text>
        </View>
      </View>
      {/* Learning Progress */}
      <Text style={styles.sectionTitle}>Learning Progress (School-wide)</Text>
      <View style={styles.progressBarSection}>
        <Text style={styles.progressLabel}>School Completion</Text>
        <Progress.Bar
          progress={completionPercent}
          width={null}
          height={18}
          color="#007bff"
          borderRadius={9}
          unfilledColor="#e3e3e3"
          style={{ marginVertical: 8 }}
        />
        <Text style={styles.progressPercent}>{Math.round(completionPercent * 100)}%</Text>
      </View>
      {/* Projector Hubs */}
      <Text style={styles.sectionTitle}>Projector Hubs in Your School</Text>
      <View style={styles.hubList}>
        {projectorHubs.map(hub => (
          <View key={hub.id} style={styles.hubRow}>
            <Ionicons
              name={hub.status === 'online' ? 'wifi' : 'close-circle'}
              size={22}
              color={hub.status === 'online' ? '#28a745' : '#d9534f'}
              style={{ marginRight: 8 }}
            />
            <Text style={styles.hubName}>{hub.name}</Text>
            <Text style={[styles.hubStatus, { color: hub.status === 'online' ? '#28a745' : '#d9534f' }]}>
              {hub.status.charAt(0).toUpperCase() + hub.status.slice(1)}
            </Text>
          </View>
        ))}
      </View>
      {/* Teacher Management Placeholder */}
      <Text style={styles.sectionTitle}>Teacher Management</Text>
      <Text>Manage Teachers (coming soon)</Text>
      <Button title="Go to Teacher Management" onPress={() => {}} />
      <Button title="View School Details" onPress={() => {}} />
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
  metricNumber: { fontSize: 32, fontWeight: 'bold', color: '#007bff', marginTop: 4 },
  metricLabel: { fontSize: 14, color: '#555' },
  progressBarSection: { marginBottom: 20, alignItems: 'center' },
  progressLabel: { fontSize: 15, color: '#333' },
  progressPercent: { fontSize: 18, fontWeight: 'bold', color: '#007bff', marginTop: 4 },
  hubList: { marginBottom: 20 },
  hubRow: { flexDirection: 'row', alignItems: 'center', marginBottom: 6 },
  hubName: { fontSize: 15, flex: 1 },
  hubStatus: { fontWeight: 'bold', marginLeft: 8 },
});
