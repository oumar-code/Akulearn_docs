import React from 'react';
import { View, Text, TouchableOpacity, StyleSheet } from 'react-native';
import { theme } from '../theme';

export default function Navbar({ role }) {
  return (
    <View style={styles.navbar}>
      <Text style={styles.title}>Akulearn Coach</Text>
      <View style={styles.buttons}>
        {role === 'student' && <TouchableOpacity style={styles.button}><Text>Dashboard</Text></TouchableOpacity>}
        {role === 'teacher' && <TouchableOpacity style={styles.button}><Text>Review</Text></TouchableOpacity>}
        {role === 'admin' && <TouchableOpacity style={styles.button}><Text>Admin</Text></TouchableOpacity>}
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  navbar: {
    backgroundColor: theme.colors.primary,
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: 16,
  },
  title: {
    color: '#fff',
    fontSize: 20,
    fontWeight: 'bold',
  },
  buttons: {
    flexDirection: 'row',
  },
  button: {
    backgroundColor: theme.colors.secondary,
    borderRadius: theme.borderRadius,
    padding: 8,
    marginLeft: 8,
  },
});
