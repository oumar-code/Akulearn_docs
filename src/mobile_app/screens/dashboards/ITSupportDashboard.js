import React from 'react';
import { View, Text, Button, StyleSheet } from 'react-native';

export default function ITSupportDashboard({ navigation, route }) {
  const { firstName, role } = route.params || {};
  return (
    <View style={styles.container}>
      <Text style={styles.title}>Welcome, IT Support {firstName || 'User'}!</Text>
      <Text style={styles.sectionTitle}>Projector Hubs Health</Text>
      <Text>Online: 8, Offline: 2, Needs Attention: 1</Text>
      <Text style={styles.sectionTitle}>Recent Heartbeats</Text>
      <Text>Hub-01: OK, Hub-02: OK, Hub-03: Needs Attention</Text>
      <Text style={styles.sectionTitle}>Software Version Distribution</Text>
      <Text>v1.0: 6 hubs, v1.1: 5 hubs</Text>
      <Text style={styles.sectionTitle}>Manage Hubs</Text>
      <Text>Hub Management (coming soon)</Text>
      <Button title="Troubleshooting Guides" onPress={() => {}} />
      <Button title="Logout" onPress={() => navigation.navigate('LoginScreen')} color="#d9534f" />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 20 },
  title: { fontSize: 24, fontWeight: 'bold', marginBottom: 20 },
  sectionTitle: { fontSize: 18, fontWeight: 'bold', marginTop: 20, marginBottom: 10 },
});
