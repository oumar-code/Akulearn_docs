
import React from 'react';
import { View, Text, Button, StyleSheet, ActivityIndicator, ScrollView } from 'react-native';
import { Ionicons, MaterialCommunityIcons } from '@expo/vector-icons';
import { useFetch } from '../../hooks/useFetch';


export default function ITSupportDashboard({ navigation, route }) {
  const { firstName, role } = route.params || {};
  // Simulate fetch for demo (replace with real endpoint if available)
  const { data, loading, error, refetch } = useFetch('https://demo.akulearn/api/it-hubs', {}, false); // disabled for now
  // Demo data
  const hubs = [
    { name: 'Hub-01', status: 'ok', version: 'v1.0' },
    { name: 'Hub-02', status: 'ok', version: 'v1.1' },
    { name: 'Hub-03', status: 'needs_attention', version: 'v1.0' },
  ];
  const online = 8, offline = 2, needsAttention = 1;
  const versionDist = { 'v1.0': 6, 'v1.1': 5 };

  return (
    <ScrollView contentContainerStyle={styles.container}>
      <Text style={styles.title}>
        <MaterialCommunityIcons name="account-hard-hat" size={28} color="#007bff" />
        {' '}Welcome, IT Support {firstName || 'User'}!
      </Text>
      {loading && <ActivityIndicator size="large" color="#007bff" style={{ marginVertical: 20 }} />}
      {error && (
        <View style={styles.errorBox}>
          <Ionicons name="alert-circle" size={20} color="#d9534f" />
          <Text style={styles.errorText}>{error}</Text>
          <Button title="Retry" onPress={refetch} color="#007bff" />
        </View>
      )}
      <Text style={styles.sectionTitle}>Projector Hubs Health</Text>
      <View style={styles.metricsRow}>
        <View style={[styles.metricBox, { backgroundColor: '#e6f9f0' }]}> 
          <Ionicons name="wifi" size={28} color="#28a745" />
          <Text style={styles.metricNumber}>{online}</Text>
          <Text style={styles.metricLabel}>Online</Text>
        </View>
        <View style={[styles.metricBox, { backgroundColor: '#fff3cd' }]}> 
          <Ionicons name="cloud-offline" size={28} color="#ffc107" />
          <Text style={styles.metricNumber}>{offline}</Text>
          <Text style={styles.metricLabel}>Offline</Text>
        </View>
        <View style={[styles.metricBox, { backgroundColor: '#f8d7da' }]}> 
          <Ionicons name="alert" size={28} color="#d9534f" />
          <Text style={styles.metricNumber}>{needsAttention}</Text>
          <Text style={styles.metricLabel}>Needs Attention</Text>
        </View>
      </View>
      <Text style={styles.sectionTitle}>Recent Heartbeats</Text>
      <View style={styles.heartbeatList}>
        {hubs.map(hub => (
          <View key={hub.name} style={styles.heartbeatItem}>
            <Ionicons name="hardware-chip" size={20} color="#007bff" />
            <Text style={{ marginLeft: 8 }}>{hub.name}:</Text>
            <Text style={{ marginLeft: 4, color: hub.status === 'ok' ? '#28a745' : '#d9534f', fontWeight: 'bold' }}>
              {hub.status === 'ok' ? 'OK' : 'Needs Attention'}
            </Text>
          </View>
        ))}
      </View>
      <Text style={styles.sectionTitle}>Software Version Distribution</Text>
      <View style={styles.versionRow}>
        {Object.entries(versionDist).map(([ver, count]) => (
          <View key={ver} style={styles.versionBox}>
            <MaterialCommunityIcons name="update" size={20} color="#007bff" />
            <Text style={{ marginLeft: 6 }}>{ver}: {count} hubs</Text>
          </View>
        ))}
      </View>
      <Text style={styles.sectionTitle}>Manage Hubs</Text>
      <Text style={{ color: '#888', marginBottom: 10 }}>Hub Management (coming soon)</Text>
      <Button title="Troubleshooting Guides" onPress={() => {}} color="#007bff" />
      <Button title="Logout" onPress={() => navigation.navigate('LoginScreen')} color="#d9534f" style={{ marginTop: 10 }} />
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { flexGrow: 1, padding: 20, backgroundColor: '#f9fafe' },
  title: { fontSize: 24, fontWeight: 'bold', marginBottom: 20, color: '#007bff', flexDirection: 'row', alignItems: 'center' },
  sectionTitle: { fontSize: 18, fontWeight: 'bold', marginTop: 24, marginBottom: 10, color: '#333' },
  metricsRow: { flexDirection: 'row', justifyContent: 'space-between', marginBottom: 20 },
  metricBox: { alignItems: 'center', flex: 1, marginHorizontal: 8, padding: 12, borderRadius: 8, elevation: 1 },
  metricNumber: { fontSize: 22, fontWeight: 'bold', marginTop: 4 },
  metricLabel: { fontSize: 13, color: '#555', textAlign: 'center' },
  heartbeatList: { marginBottom: 10 },
  heartbeatItem: { flexDirection: 'row', alignItems: 'center', marginBottom: 6 },
  versionRow: { flexDirection: 'row', marginBottom: 10 },
  versionBox: { flexDirection: 'row', alignItems: 'center', marginRight: 16, backgroundColor: '#e9ecef', borderRadius: 6, padding: 6, marginBottom: 4 },
  errorBox: { backgroundColor: '#f8d7da', padding: 10, borderRadius: 8, marginBottom: 10, flexDirection: 'row', alignItems: 'center' },
  errorText: { color: '#d9534f', marginLeft: 8, flex: 1 },
});
