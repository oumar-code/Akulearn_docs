import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity, Alert } from 'react-native';

export default function SubscriptionOptionsScreen({ navigation }) {
  function handleSubscribe(tier) {
    Alert.alert('Payment integration coming soon!', 'We accept card, bank transfer, and mobile money.');
  }
  return (
    <View style={styles.container}>
      <Text style={styles.title}>Choose Your Plan</Text>
      <View style={styles.tierBox}>
        <Text style={styles.tierTitle}>Premium <Text style={styles.tierPrice}>₦3,500/month</Text></Text>
        <View style={styles.bullets}>
          <Text style={styles.bullet}>• Access all premium content</Text>
          <Text style={styles.bullet}>• Practice exams & analytics</Text>
          <Text style={styles.bullet}>• Priority AI Tutor support</Text>
        </View>
        <TouchableOpacity style={styles.subscribeBtn} onPress={() => handleSubscribe('premium')}>
          <Text style={styles.subscribeText}>Subscribe Now</Text>
        </TouchableOpacity>
      </View>
      <View style={styles.tierBox}>
        <Text style={styles.tierTitle}>Family <Text style={styles.tierPrice}>₦8,000/month</Text></Text>
        <View style={styles.bullets}>
          <Text style={styles.bullet}>• Up to 5 users</Text>
          <Text style={styles.bullet}>• All Premium features</Text>
          <Text style={styles.bullet}>• Family progress dashboard</Text>
        </View>
        <TouchableOpacity style={[styles.subscribeBtn, { backgroundColor: '#28a745' }]} onPress={() => handleSubscribe('family')}>
          <Text style={[styles.subscribeText, { color: '#fff' }]}>Subscribe Now</Text>
        </TouchableOpacity>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 20, backgroundColor: '#f7faff' },
  title: { fontSize: 24, fontWeight: 'bold', marginBottom: 24, textAlign: 'center' },
  tierBox: { backgroundColor: '#fff', borderRadius: 10, padding: 24, marginBottom: 20, elevation: 2 },
  tierTitle: { fontSize: 20, fontWeight: 'bold', marginBottom: 8 },
  tierPrice: { fontSize: 18, color: '#007bff', fontWeight: 'bold' },
  bullets: { marginBottom: 12 },
  bullet: { fontSize: 15, color: '#333', marginBottom: 2 },
  subscribeBtn: { backgroundColor: '#007bff', padding: 12, borderRadius: 6, alignItems: 'center' },
  subscribeText: { color: '#fff', fontSize: 16, fontWeight: 'bold' },
});
