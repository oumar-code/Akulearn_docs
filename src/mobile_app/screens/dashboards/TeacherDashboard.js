import React from 'react';
import { View, Text, StyleSheet, Button, ScrollView } from 'react-native';

export default function TeacherDashboard({ navigation, route }) {
  const { firstName, role } = route.params || {};
  return (
    <ScrollView contentContainerStyle={styles.container}>
      <Text style={styles.title}>Welcome, Teacher {firstName || ''}!</Text>
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>My Classes</Text>
        <Text style={styles.metric}>- JSS1A Mathematics</Text>
        <Text style={styles.metric}>- SSS2 Biology</Text>
        <Text style={styles.metric}>- JSS3 English</Text>
      </View>
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Student Performance (Overall)</Text>
        <Text style={styles.metric}>Class Avg Score: <Text style={styles.bigNumber}>76%</Text></Text>
      </View>
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Challenging Topics for Your Students</Text>
        <Text style={styles.metric}>- Quadratic Equations</Text>
        <Text style={styles.metric}>- Photosynthesis</Text>
        <Text style={styles.metric}>- English Comprehension</Text>
      </View>
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Assign Content</Text>
        <Button title="Assign Lessons (Coming Soon)" onPress={() => {}} />
      </View>
      <Button title="Support Resources" onPress={() => {}} />
      <Button title="Logout" onPress={() => navigation.navigate('LoginScreen')} color="#d9534f" />
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { padding: 20 },
  title: { fontSize: 24, fontWeight: 'bold', marginBottom: 20, textAlign: 'center' },
  section: { marginBottom: 24, backgroundColor: '#f9f9f9', borderRadius: 8, padding: 16 },
  sectionTitle: { fontSize: 18, fontWeight: 'bold', marginBottom: 8 },
  metric: { fontSize: 16, marginBottom: 4 },
  bigNumber: { fontSize: 22, fontWeight: 'bold', color: '#007bff' },
});


