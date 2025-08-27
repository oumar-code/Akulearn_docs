import React, { useState } from 'react';
import { View, Text, TextInput, Button, StyleSheet, Alert, Modal, TouchableOpacity, ActivityIndicator } from 'react-native';
import jwtDecode from 'jwt-decode';
import AsyncStorage from '@react-native-async-storage/async-storage';

export default function RegisterScreen({ navigation }) {
  const [firstName, setFirstName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [showWelcome, setShowWelcome] = useState(false);
  const [showFreePrompt, setShowFreePrompt] = useState(false);

  async function handleRegister() {
    setLoading(true);
    try {
      // Replace with actual registration API call
      const response = await fetch('https://your-backend-api/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ first_name: firstName, email, password })
      });
      const data = await response.json();
      if (response.ok && data.token) {
        setShowWelcome(true);
        setLoading(false);
        await AsyncStorage.setItem('akulearn_token', data.token);
        const decoded = jwtDecode(data.token);
        const role = decoded.role;
        const userId = decoded.user_id || decoded.id;
        const firstNameDecoded = decoded.first_name || firstName;
        setTimeout(() => {
          setShowWelcome(false);
          // Role-based navigation
          switch (role) {
            case 'super_admin':
              navigation.replace('SuperAdminDashboard', { firstName: firstNameDecoded, role, userId });
              break;
            case 'school_admin':
              navigation.replace('SchoolAdminDashboard', { firstName: firstNameDecoded, role, userId });
              break;
            case 'teacher':
              navigation.replace('TeacherDashboard', { firstName: firstNameDecoded, role, userId });
              break;
            case 'student':
              navigation.replace('StudentDashboard', { firstName: firstNameDecoded, role, userId });
              break;
            case 'guardian':
              navigation.replace('GuardianDashboard', { firstName: firstNameDecoded, role, userId });
              break;
            case 'corporation':
              navigation.replace('CorporateDashboard', { firstName: firstNameDecoded, role, userId });
              break;
            case 'government':
              navigation.replace('GovernmentDashboard', { firstName: firstNameDecoded, role, userId });
              break;
            case 'ngo_partner':
              navigation.replace('NgoPartnerDashboard', { firstName: firstNameDecoded, role, userId });
              break;
            case 'it_support':
              navigation.replace('ITSupportDashboard', { firstName: firstNameDecoded, role, userId });
              break;
            default:
              Alert.alert('Unknown role', 'Your account role is not recognized.');
          }
        }, 1800); // Show welcome for 1.8 seconds
      } else {
        setLoading(false);
        Alert.alert('Registration Error', data.detail || 'Failed to register. Please try again.');
      }
    } catch (e) {
      Alert.alert('Registration failed', 'Please try again.');
      setLoading(false);
    }
  }

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Register for Akulearn</Text>
      <TextInput style={styles.input} placeholder="First Name" value={firstName} onChangeText={setFirstName} />
      <TextInput style={styles.input} placeholder="Email" value={email} onChangeText={setEmail} keyboardType="email-address" />
      <TextInput style={styles.input} placeholder="Password" value={password} onChangeText={setPassword} secureTextEntry />
      <Button title={loading ? 'Registering...' : 'Register'} onPress={handleRegister} disabled={loading} />
      <Button title="Already have an account? Login" onPress={() => navigation.navigate('LoginScreen')} />
      {loading && <ActivityIndicator size="large" color="#007bff" style={{ marginVertical: 10 }} />}
      <Modal visible={showWelcome} transparent animationType="fade">
        <View style={styles.modalOverlay}>
          <View style={styles.modalBox}>
            <Text style={styles.welcomeText}>Welcome to Akulearn!</Text>
          </View>
        </View>
      </Modal>
      <Modal visible={showFreePrompt} transparent animationType="slide">
        <View style={styles.modalOverlay}>
          <View style={styles.modalBox}>
            <Text style={styles.freeTitle}>🎉 Free First Year!</Text>
            <Text style={styles.freeText}>Enjoy Akulearn free for your first year. Upgrade to Premium anytime for more features!</Text>
            <View style={{ flexDirection: 'row', marginTop: 16 }}>
              <TouchableOpacity style={styles.freeBtn} onPress={() => { setShowFreePrompt(false); }}>
                <Text style={styles.freeBtnText}>Explore Free Content</Text>
              </TouchableOpacity>
              <TouchableOpacity style={[styles.freeBtn, { backgroundColor: '#007bff' }]} onPress={() => { setShowFreePrompt(false); navigation.navigate('SubscriptionOptionsScreen'); }}>
                <Text style={[styles.freeBtnText, { color: '#fff' }]}>Upgrade Now</Text>
              </TouchableOpacity>
            </View>
          </View>
        </View>
      </Modal>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 20, justifyContent: 'center' },
  title: { fontSize: 24, fontWeight: 'bold', marginBottom: 20, textAlign: 'center' },
  input: { borderWidth: 1, borderColor: '#ccc', borderRadius: 5, padding: 10, marginBottom: 12 },
  modalOverlay: { flex: 1, backgroundColor: 'rgba(0,0,0,0.3)', justifyContent: 'center', alignItems: 'center' },
  modalBox: { backgroundColor: '#fff', borderRadius: 10, padding: 30, alignItems: 'center', minWidth: 280 },
  welcomeText: { fontSize: 22, fontWeight: 'bold', color: '#28a745' },
  freeTitle: { fontSize: 20, fontWeight: 'bold', color: '#007bff', marginBottom: 8 },
  freeText: { fontSize: 16, color: '#333', textAlign: 'center' },
  freeBtn: { padding: 10, borderRadius: 6, backgroundColor: '#f0f0f0', marginHorizontal: 6 },
  freeBtnText: { fontSize: 15, color: '#007bff', fontWeight: 'bold' },
});
