import React, { useState } from 'react';
import { View, Text, StyleSheet, TouchableOpacity, Modal } from 'react-native';
import { Ionicons } from '@expo/vector-icons';

// Dummy topic data for demonstration
const topic = {
  title: 'Quadratic Equations',
  description: 'Learn how to solve quadratic equations.',
  premium_only: true,
};

export default function TopicDetailScreen({ navigation, route }) {
  const [showPremiumModal, setShowPremiumModal] = useState(false);
  // Assume user is free tier for demo
  const isFreeUser = true;

  function handlePressContent() {
    if (topic.premium_only && isFreeUser) {
      setShowPremiumModal(true);
    } else {
      // Navigate to content
    }
  }

  return (
    <View style={styles.container}>
      <Text style={styles.title}>{topic.title}</Text>
      <Text style={styles.desc}>{topic.description}</Text>
      <TouchableOpacity
        style={[styles.contentBox, topic.premium_only ? styles.premiumBox : null]}
        onPress={handlePressContent}
        disabled={topic.premium_only && isFreeUser}
      >
        <Text style={styles.contentText}>Start Topic</Text>
        {topic.premium_only && (
          <Ionicons name="lock-closed" size={20} color="#d9534f" style={{ marginLeft: 8 }} />
        )}
      </TouchableOpacity>
      <Modal visible={showPremiumModal} transparent animationType="slide">
        <View style={styles.modalOverlay}>
          <View style={styles.modalBox}>
            <Text style={styles.modalTitle}>Premium Feature</Text>
            <Text style={styles.modalText}>This topic is available to Premium users only.</Text>
            <TouchableOpacity style={styles.upgradeBtn} onPress={() => { setShowPremiumModal(false); navigation.navigate('SubscriptionOptionsScreen'); }}>
              <Text style={styles.upgradeText}>Upgrade to Premium to Unlock</Text>
            </TouchableOpacity>
            <TouchableOpacity style={styles.closeBtn} onPress={() => setShowPremiumModal(false)}>
              <Text style={styles.closeText}>Close</Text>
            </TouchableOpacity>
          </View>
        </View>
      </Modal>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 20, justifyContent: 'center', alignItems: 'center' },
  title: { fontSize: 22, fontWeight: 'bold', marginBottom: 10 },
  desc: { fontSize: 16, color: '#555', marginBottom: 20 },
  contentBox: { flexDirection: 'row', alignItems: 'center', backgroundColor: '#f7faff', padding: 16, borderRadius: 8, marginBottom: 20 },
  premiumBox: { backgroundColor: '#fbeaea', borderColor: '#d9534f', borderWidth: 1 },
  contentText: { fontSize: 18, fontWeight: 'bold', color: '#007bff' },
  modalOverlay: { flex: 1, backgroundColor: 'rgba(0,0,0,0.3)', justifyContent: 'center', alignItems: 'center' },
  modalBox: { backgroundColor: '#fff', borderRadius: 10, padding: 30, alignItems: 'center', minWidth: 280 },
  modalTitle: { fontSize: 20, fontWeight: 'bold', color: '#d9534f', marginBottom: 8 },
  modalText: { fontSize: 16, color: '#333', textAlign: 'center', marginBottom: 16 },
  upgradeBtn: { backgroundColor: '#007bff', padding: 10, borderRadius: 6, marginBottom: 8 },
  upgradeText: { color: '#fff', fontSize: 15, fontWeight: 'bold' },
  closeBtn: { padding: 8 },
  closeText: { color: '#007bff', fontSize: 15 },
});
