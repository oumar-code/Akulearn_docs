import React from 'react';
import { View, Text, Button, StyleSheet } from 'react-native';

export default function TeacherDashboard({ navigation, route }) {
  const { firstName, role } = route.params || {};
  return (
    <View style={styles.container}>
      <Text style={styles.title}>Welcome, Teacher {firstName || 'User'}!</Text>
      
      <Text style={styles.sectionTitle}>My Classes</Text>
      <Text>Math 101, Science 201, English 301</Text>
      
      <Text style={styles.sectionTitle}>Student Performance (Overall)</Text>
      <Text>Class Avg Score: 76%</Text>
      
      <Text style={styles.sectionTitle}>Challenging Topics for Your Students</Text>
      <Text>Algebra, Photosynthesis, Essay Writing</Text>
      
      <Text style={styles.sectionTitle}>Assign Content</Text>
      <Text>Assign Lessons (coming soon)</Text>
      
      <Button title="Support Resources" onPress={() => {}} />
      <Button title="Logout" onPress={() => navigation.navigate('LoginScreen')} color="#d9534f" />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 20 },
  title: { fontSize: 24, fontWeight: 'bold', marginBottom: 20 },
  sectionTitle: { fontSize: 18, fontWeight: 'bold', marginTop: 20, marginBottom: 10 },
});
