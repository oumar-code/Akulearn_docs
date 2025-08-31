import React, { useEffect, useState } from 'react';
import { View, Text, Button, ActivityIndicator } from 'react-native';

export default function ReviewPanel() {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  useEffect(() => {
    setLoading(true);
    // Replace with actual API call
    setTimeout(() => {
      setItems([{ id: 1, title: 'Math Video' }]);
      setLoading(false);
    }, 500);
  }, []);
  const approve = id => {
    // Replace with actual API call
    alert('Approved ' + id);
  };
  const reject = id => {
    // Replace with actual API call
    alert('Rejected ' + id);
  };
  return (
    <View style={{ padding: 16 }}>
      <Text style={{ fontSize: 18, fontWeight: 'bold' }}>Review Panel</Text>
      <Text>Review and approve submitted content here.</Text>
      {loading && <ActivityIndicator />}
      {error ? <Text style={{ color: 'red' }}>{error}</Text> : null}
      {items.map(item => (
        <View key={item.id} style={{ marginVertical: 8 }}>
          <Text>{item.title}</Text>
          <Button title="Approve" onPress={() => approve(item.id)} />
          <Button title="Reject" onPress={() => reject(item.id)} />
        </View>
      ))}
    </View>
  );
}
