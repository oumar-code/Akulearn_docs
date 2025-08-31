import React, { useEffect, useState } from 'react';
import { View, Text, Button, ActivityIndicator } from 'react-native';

export default function AdminPanel() {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  useEffect(() => {
    setLoading(true);
    // Replace with actual API call
    setTimeout(() => {
      setUsers([{ id: 1, name: 'Alice', role: 'teacher' }]);
      setLoading(false);
    }, 500);
  }, []);
  const removeUser = id => {
    // Replace with actual API call
    alert('Removed user ' + id);
  };
  return (
    <View style={{ padding: 16 }}>
      <Text style={{ fontSize: 18, fontWeight: 'bold' }}>Admin Panel</Text>
      <Text>Manage users, content uploads, and view analytics.</Text>
      {loading && <ActivityIndicator />}
      {error ? <Text style={{ color: 'red' }}>{error}</Text> : null}
      {users.map(user => (
        <View key={user.id} style={{ marginVertical: 8 }}>
          <Text>{user.name} ({user.role})</Text>
          <Button title="Remove" onPress={() => removeUser(user.id)} />
        </View>
      ))}
    </View>
  );
}
