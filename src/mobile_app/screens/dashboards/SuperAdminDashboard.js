import React, { useEffect, useState } from 'react';
import { View, Text, Button, StyleSheet, FlatList, ActivityIndicator } from 'react-native';

export default function SuperAdminDashboard({ navigation, route }) {
  const { firstName, role } = route.params || {};
  const [schools, setSchools] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchSchools() {
      try {
        // Replace with actual backend API URL
        const response = await fetch('https://your-backend-api/admin/schools');
        const data = await response.json();
        if (response.ok) setSchools(data);
      } catch (error) {
        // Handle error
      } finally {
        setLoading(false);
      }
    }
    fetchSchools();
  }, []);

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Super Admin Portal</Text>
      <Text style={styles.welcome}>Welcome, {firstName || 'User'}! You are logged in as a {role || 'super_admin'}.</Text>
      <Button title="Create New School" onPress={() => navigation.navigate('CreateSchoolScreen')} />
      <Text style={styles.listTitle}>Schools</Text>
      {loading ? <ActivityIndicator size="large" /> : (
        <FlatList
          data={schools}
          keyExtractor={(item) => item.school_id}
          renderItem={({ item }) => (
            <View style={styles.schoolItem}>
              <Text style={styles.schoolName}>{item.name}</Text>
              <Text>{item.city} - {item.state}</Text>
              <Text>Status: {item.is_active ? 'Active' : 'Inactive'}</Text>
              <Button title="View Details" onPress={() => {}} />
            </View>
          )}
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
  listTitle: { fontSize: 20, fontWeight: 'bold', marginTop: 20, marginBottom: 10 },
  schoolItem: { padding: 10, borderWidth: 1, borderColor: '#ccc', borderRadius: 5, marginBottom: 10 },
  schoolName: { fontSize: 16, fontWeight: 'bold' },
});
