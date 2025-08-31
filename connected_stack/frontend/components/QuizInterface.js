import React, { useState } from 'react';
import { View, Text, TextInput, TouchableOpacity, StyleSheet } from 'react-native';
import { theme } from '../theme';

export default function QuizInterface({ questions, onSubmit }) {
  const [answers, setAnswers] = useState(Array(questions.length).fill(''));

  const handleChange = (idx, value) => {
    const newAnswers = [...answers];
    newAnswers[idx] = value;
    setAnswers(newAnswers);
  };

  return (
    <View style={styles.card}>
      <Text style={styles.header}>Quiz</Text>
      {questions.map((q, idx) => (
        <View key={idx}>
          <Text>{q.text}</Text>
          <TextInput
            style={styles.input}
            value={answers[idx]}
            onChangeText={val => handleChange(idx, val)}
            placeholder="Your answer"
          />
        </View>
      ))}
      <TouchableOpacity style={styles.button} onPress={() => onSubmit(answers)}>
        <Text style={{ color: '#fff' }}>Submit</Text>
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  card: {
    backgroundColor: theme.colors.card,
    borderRadius: theme.borderRadius,
    padding: 16,
    marginVertical: 16,
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
