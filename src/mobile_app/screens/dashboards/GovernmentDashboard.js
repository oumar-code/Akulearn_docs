import React from 'react';
import { View, Text, StyleSheet, Button } from 'react-native';

export default function GovernmentDashboard({ navigation, route }) {
  const { firstName, role } = route.params || {};
  return (
    <View style={styles.container}>
      <Text style={styles.title}>Welcome, Government Partner!</Text>
      <Text style={styles.sectionTitle}>Macro Impact</Text>
      <Text>Total Students Reached: 120,000</Text>
      <Text>Overall Exam Pass Rate Improvement: 18%</Text>
      <Text>Schools Impacted: 320</Text>
      <Text>Anonymized Learning Trends for Lagos State</Text>
      <Text>Data Licensing (coming soon)</Text>
      <Button title="Logout" onPress={() => navigation.navigate('LoginScreen')} color="#d9534f" />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 20 },
  title: { fontSize: 24, fontWeight: 'bold', marginBottom: 20 },
  sectionTitle: { fontSize: 18, fontWeight: 'bold', marginTop: 20, marginBottom: 10 },
});
