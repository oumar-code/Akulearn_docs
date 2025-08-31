import React, { useState } from 'react';
import { View, TextInput, Button, Text, ActivityIndicator } from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { login } from '../api';

export default function LoginScreen({ navigation }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
    const login = async () => {
    setLoading(true);
      setError('');
      try {
        const result = await loginUser(username, password);
        setToken(result.token);
        setUser({ username, role: result.role });
        navigation.navigate('DashboardScreen');
    } catch (e) {
        setError('Invalid credentials');
    } finally {
      setLoading(false);
    }
  }
  return (
    <View style={{ padding: 24 }}>
      <TextInput placeholder="Username" value={username} onChangeText={setUsername} style={{ marginBottom: 12 }} />
      <TextInput placeholder="Password" value={password} onChangeText={setPassword} secureTextEntry style={{ marginBottom: 12 }} />
      <Button title="Login" onPress={handleLogin} disabled={loading} />
      {loading && <ActivityIndicator />}
      {error ? <Text style={{ color: 'red' }}>{error}</Text> : null}
    </View>
  );
}
