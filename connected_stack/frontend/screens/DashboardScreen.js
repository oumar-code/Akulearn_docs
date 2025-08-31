
import React, { useContext, useEffect, useState } from 'react';
import { View, Text, ActivityIndicator } from 'react-native';
import { UserContext } from '../UserContext';
import { fetchProgress } from '../api';

export default function DashboardScreen() {
  const { user, token } = useContext(UserContext);
  const [progress, setProgress] = useState(0);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  useEffect(() => {
    const loadProgress = async () => {
      setLoading(true);
      try {
        const data = await fetchProgress(user.username, token);
        setProgress(data.progress);
      } catch (e) {
        setError('Unable to load progress.');
      } finally {
        setLoading(false);
      }
    };
    if (user && token) loadProgress();
  }, [user, token]);
  return (
    <View>
      <Text>Dashboard ({user?.role})</Text>
      {loading && <ActivityIndicator />}
      {error ? <Text style={{ color: 'red' }}>{error}</Text> : null}
      <Text>Progress: {progress}%</Text>
      {/* Add role-based panels here */}
    </View>
  );
}
