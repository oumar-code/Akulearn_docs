import React, { useState } from 'react';
import { View, Text, TextInput, Button, StyleSheet, Alert, ScrollView } from 'react-native';

export default function CreateSchoolScreen({ navigation }) {
  const [form, setForm] = useState({
    school_name: '', address: '', city: '', state: '', contact_email: '', phone_number: '',
    admin_email: '', admin_password: '', admin_first_name: '', admin_last_name: ''
  });
  const [loading, setLoading] = useState(false);

  const handleChange = (key, value) => setForm({ ...form, [key]: value });

  const handleSubmit = async () => {
    setLoading(true);
    try {
      // Replace with actual backend API URL
      const response = await fetch('https://your-backend-api/admin/schools', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(form)
      });
      const data = await response.json();
      if (response.ok) {
        Alert.alert('Success', 'School created successfully!');
        navigation.goBack();
      } else {
        Alert.alert('Error', data.detail || 'Failed to create school.');
      }
    } catch (error) {
      Alert.alert('Error', error.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <ScrollView contentContainerStyle={styles.container}>
      <Text style={styles.title}>Create New School</Text>
      {Object.keys(form).map((key) => (
        <TextInput
          key={key}
          style={styles.input}
          placeholder={key.replace(/_/g, ' ').replace('admin ', 'Admin ')}
          value={form[key]}
          onChangeText={(v) => handleChange(key, v)}
          secureTextEntry={key === 'admin_password'}
          autoCapitalize={key.includes('email') ? 'none' : 'words'}
        />
      ))}
      <Button title={loading ? 'Creating...' : 'Create School'} onPress={handleSubmit} disabled={loading} />
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { padding: 20 },
  title: { fontSize: 22, fontWeight: 'bold', marginBottom: 20 },
  input: { width: '100%', padding: 10, marginBottom: 15, borderWidth: 1, borderColor: '#ccc', borderRadius: 5 },
});
