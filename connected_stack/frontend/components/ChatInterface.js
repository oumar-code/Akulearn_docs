import React, { useState } from 'react';
import { View, Text, TextInput, TouchableOpacity, StyleSheet } from 'react-native';
import { theme } from '../theme';

export default function ChatInterface({ messages, onSend }) {
  const [input, setInput] = useState('');

  const handleSend = () => {
    if (input.trim()) {
      onSend(input);
      setInput('');
    }
  };

  return (
    <View style={styles.chat}>
      <Text style={styles.header}>AI Tutor Chat</Text>
      {messages.map((msg, idx) => (
        <View key={idx}>
          <Text><Text style={{ fontWeight: 'bold' }}>{msg.sender}:</Text> {msg.text}</Text>
        </View>
      ))}
      <TextInput
        style={styles.input}
        value={input}
        onChangeText={setInput}
        placeholder="Type your message..."
        onSubmitEditing={handleSend}
      />
      <TouchableOpacity style={styles.button} onPress={handleSend}>
        <Text style={{ color: '#fff' }}>Send</Text>
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  chat: {
    backgroundColor: '#f1f1f1',
    borderRadius: theme.borderRadius,
    padding: 16,
    marginVertical: 16,
    minHeight: 120,
  },
  header: {
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 8,
  },
  input: {
    borderWidth: 1,
    borderColor: '#ccc',
    borderRadius: theme.borderRadius,
    padding: 8,
    fontSize: 16,
    marginVertical: 8,
    width: '100%',
  },
  button: {
    backgroundColor: theme.colors.primary,
    borderRadius: theme.borderRadius,
    padding: 12,
    alignItems: 'center',
    marginTop: 12,
  },
});
