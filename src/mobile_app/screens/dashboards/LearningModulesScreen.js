import React, { useState } from 'react';
import { View, Text, StyleSheet, FlatList, TouchableOpacity, Modal } from 'react-native';
import { Ionicons } from '@expo/vector-icons';

// Dummy modules data
const modules = [
  { id: '1', title: 'Algebra Basics', premium_only: false },
  { id: '2', title: 'Quadratic Equations', premium_only: true },
  { id: '3', title: 'English Grammar', premium_only: false },
  { id: '4', title: 'WAEC Past Questions', premium_only: true },
];

export default function LearningModulesScreen({ navigation }) {
  const [showPremiumModal, setShowPremiumModal] = useState(false);
  const [selectedModule, setSelectedModule] = useState(null);
  // Assume user is free tier for demo
  const isFreeUser = true;

  function handleModulePress(module) {
    if (module.premium_only && isFreeUser) {
      setSelectedModule(module);
      setShowPremiumModal(true);
    } else {
      // Navigate to topic detail
      navigation.navigate('TopicDetailScreen', { module });
    }
  }

  return (
    <View style={styles.container}>
      <Text style={styles.title}>My Learning Modules</Text>
      <FlatList
        data={modules}
        keyExtractor={item => item.id}
        renderItem={({ item }) => (
          <TouchableOpacity
            style={[styles.moduleBox, item.premium_only ? styles.premiumBox : null]}
            onPress={() => handleModulePress(item)}
            disabled={item.premium_only && isFreeUser}
          >
            <Text style={[styles.moduleTitle, item.premium_only ? styles.premiumTitle : null]}>{item.title}</Text>
            {item.premium_only && (
              <Ionicons name="lock-closed" size={18} color="#d9534f" style={{ marginLeft: 8 }} />
            )}
          </TouchableOpacity>
        )}
        style={{ width: '100%' }}
      />
      <Modal visible={showPremiumModal} transparent animationType="slide">
        <View style={styles.modalOverlay}>
          <View style={styles.modalBox}>
            <Text style={styles.modalTitle}>Premium Feature</Text>
            <Text style={styles.modalText}>This module is available to Premium users only.</Text>
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
  container: { flex: 1, alignItems: 'center', padding: 20, backgroundColor: '#f7faff' },
  title: { fontSize: 22, fontWeight: 'bold', marginBottom: 20 },
  moduleBox: { flexDirection: 'row', alignItems: 'center', backgroundColor: '#fff', padding: 16, borderRadius: 8, marginBottom: 12, width: '100%' },
  premiumBox: { backgroundColor: '#fbeaea', borderColor: '#d9534f', borderWidth: 1 },
  moduleTitle: { fontSize: 17, color: '#222', fontWeight: 'bold' },
  premiumTitle: { color: '#d9534f' },
  modalOverlay: { flex: 1, backgroundColor: 'rgba(0,0,0,0.3)', justifyContent: 'center', alignItems: 'center' },
  modalBox: { backgroundColor: '#fff', borderRadius: 10, padding: 30, alignItems: 'center', minWidth: 280 },
  modalTitle: { fontSize: 20, fontWeight: 'bold', color: '#d9534f', marginBottom: 8 },
  modalText: { fontSize: 16, color: '#333', textAlign: 'center', marginBottom: 16 },
  upgradeBtn: { backgroundColor: '#007bff', padding: 10, borderRadius: 6, marginBottom: 8 },
  upgradeText: { color: '#fff', fontSize: 15, fontWeight: 'bold' },
  closeBtn: { padding: 8 },
  closeText: { color: '#007bff', fontSize: 15 },
});
