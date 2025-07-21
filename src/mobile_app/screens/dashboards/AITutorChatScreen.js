import React from 'react';
import { View, Text, StyleSheet } from 'react-native';

export default function AITutorChatScreen() {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>AI Tutor Chat</Text>
      <Text>Chat interface will appear here.</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, justifyContent: 'center', alignItems: 'center', padding: 20 },
  title: { fontSize: 22, fontWeight: 'bold', marginBottom: 20 },
});
