import React, { useState } from 'react';
import { View, Text, TextInput, Button, StyleSheet, Alert, ActivityIndicator } from 'react-native';
import jwtDecode from 'jwt-decode';
import AsyncStorage from '@react-native-async-storage/async-storage';

export default function LoginScreen({ navigation }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);

  // Enhance login flow: robust role-based navigation, error/loading handling
  const handleLogin = async () => {
    setLoading(true);
    try {
      // Replace with actual API call
      const response = await fetch('https://your-backend-api/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
      });
      const data = await response.json();
      if (response.ok && data.token) {
        await AsyncStorage.setItem('akulearn_token', data.token);
        // Decode JWT to get role and firstName
        const decoded = jwtDecode(data.token);
        const role = decoded.role;
        const userId = decoded.user_id || decoded.id;
        const firstName = decoded.first_name || 'User';
        // Redirect based on role
        switch (role) {
          case 'super_admin':
            navigation.replace('SuperAdminDashboard', { firstName, role, userId });
            break;
          case 'school_admin':
            navigation.replace('SchoolAdminDashboard', { firstName, role, userId });
            break;
          case 'teacher':
            navigation.replace('TeacherDashboard', { firstName, role, userId });
            break;
          case 'student':
            navigation.replace('StudentDashboard', { firstName, role, userId });
            break;
          case 'guardian':
            navigation.replace('GuardianDashboard', { firstName, role, userId });
            break;
          case 'corporation':
            navigation.replace('CorporateDashboard', { firstName, role, userId });
            break;
          case 'government':
            navigation.replace('GovernmentDashboard', { firstName, role, userId });
            break;
          case 'ngo_partner':
            navigation.replace('NgoPartnerDashboard', { firstName, role, userId });
            break;
          case 'it_support':
            navigation.replace('ITSupportDashboard', { firstName, role, userId });
            break;
          default:
            Alert.alert('Unknown role', 'Your account role is not recognized.');
        }
      } else {
        Alert.alert('Login Error', data.detail || 'Invalid credentials. Please try again.');
      }
    } catch (e) {
      Alert.alert('Network Error', e.message || 'Unable to connect.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Akulearn Login</Text>
      <TextInput
        style={styles.input}
        placeholder="Email"
        value={email}
        onChangeText={setEmail}
        autoCapitalize="none"
        keyboardType="email-address"
      />
      <TextInput
        style={styles.input}
        placeholder="Password"
        value={password}
        onChangeText={setPassword}
        secureTextEntry
      />
      <Button title={loading ? 'Logging in...' : 'Login'} onPress={handleLogin} disabled={loading} />
      {loading && <ActivityIndicator size="large" color="#007bff" style={{ marginVertical: 10 }} />}
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, justifyContent: 'center', alignItems: 'center', padding: 20 },
  title: { fontSize: 24, fontWeight: 'bold', marginBottom: 20 },
  input: { width: '100%', padding: 10, marginBottom: 15, borderWidth: 1, borderColor: '#ccc', borderRadius: 5 },
});
