import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { theme } from '../theme';

export default function ProgressDashboard({ progress }) {
  return (
    <View style={styles.card}>
      <Text style={styles.header}>Progress Tracker</Text>
      <View style={styles.progressBar}>
        <View style={[styles.progress, { width: `${progress}%` }]} />
      </View>
      <Text>{progress}% completed</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  card: {
    backgroundColor: theme.colors.card,
    borderRadius: theme.borderRadius,
    padding: 16,
    marginVertical: 16,
    shadowColor: '#000',
    shadowOpacity: 0.05,
    shadowRadius: 8,
  },
  header: {
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 8,
  },
  progressBar: {
    backgroundColor: theme.colors.secondary,
    borderRadius: theme.borderRadius,
    height: 16,
    width: '100%',
    marginVertical: 8,
  },
  progress: {
    backgroundColor: theme.colors.accent,
    height: '100%',
    borderRadius: theme.borderRadius,
  },
});
