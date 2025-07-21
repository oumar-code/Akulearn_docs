import React, { useEffect, useState } from 'react';
import { View, Text, FlatList, TouchableOpacity, StyleSheet, ActivityIndicator, Button } from 'react-native';

export default function GuardianDashboard({ navigation, route }) {
  const { firstName, role, userId } = route.params || {};
  const [students, setStudents] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchStudents() {
      try {
        // Replace with actual backend API URL
        const response = await fetch(`https://your-backend-api/guardian/students?guardian_id=${userId}`);
        const data = await response.json();
        if (response.ok) setStudents(data);
      } catch (error) {
        // Handle error
      } finally {
        setLoading(false);
      }
    }
    if (userId) fetchStudents();
  }, [userId]);

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Guardian Portal</Text>
      <Text style={styles.welcome}>Welcome, {firstName || 'User'}! You are logged in as a {role || 'guardian'}.</Text>
      <Text style={styles.sectionTitle}>Linked Students</Text>
      {loading ? <ActivityIndicator size="large" /> : (
        <FlatList
          data={students}
          keyExtractor={(item) => item.user_id}
          renderItem={({ item }) => (
            <TouchableOpacity style={styles.studentItem} onPress={() => navigation.navigate('StudentProgressViewScreen', { studentId: item.user_id })}>
              <Text>{item.first_name} {item.last_name}</Text>
            </TouchableOpacity>
          )}
          ListEmptyComponent={<Text>No linked students found.</Text>}
        />
      )}
      <Button title="Logout" onPress={() => navigation.navigate('LoginScreen')} color="#d9534f" />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 20 },
  title: { fontSize: 24, fontWeight: 'bold', marginBottom: 20 },
  welcome: { fontSize: 18, marginBottom: 20 },
  sectionTitle: { fontSize: 18, fontWeight: 'bold', marginBottom: 10 },
  studentItem: { padding: 10, borderWidth: 1, borderColor: '#ccc', borderRadius: 5, marginBottom: 10 },
});
