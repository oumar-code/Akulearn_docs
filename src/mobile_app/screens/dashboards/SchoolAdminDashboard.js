import React, { useEffect, useState } from 'react';
import { View, Text, Button, StyleSheet, FlatList, ActivityIndicator } from 'react-native';

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

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Welcome, School Admin {firstName || 'User'}!</Text>
      <Text style={styles.sectionTitle}>Enrollment Overview</Text>
      <Text>Total Students: 420</Text>
      <Text>Active Users: 390</Text>
      <Text style={styles.sectionTitle}>Teacher Management</Text>
      <Text>Manage Teachers (coming soon)</Text>
      <Button title="Go to Teacher Management" onPress={() => {}} />
      <Text style={styles.sectionTitle}>Learning Progress (School-wide)</Text>
      <Text>Average Topics Completed: 18</Text>
      <Text>Exam Pass Rate: 82%</Text>
      <Text style={styles.sectionTitle}>Projector Hubs in Your School</Text>
      <Text>Hub Status (coming soon)</Text>
      <Button title="View School Details" onPress={() => {}} />
      <Button title="Logout" onPress={() => navigation.navigate('LoginScreen')} color="#d9534f" />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 20 },
  title: { fontSize: 24, fontWeight: 'bold', marginBottom: 20 },
  sectionTitle: { fontSize: 18, fontWeight: 'bold', marginTop: 20, marginBottom: 10 },
});
