import React, { useState, useEffect, useContext } from 'react';
import {
  View,
  Text,
  TouchableOpacity,
  ScrollView,
  Alert,
  StyleSheet,
  SafeAreaView
} from 'react-native';
import { UserContext } from '../UserContext';
import { submitAttempt, getRandomQuestions } from '../api';

export default function QuizScreen({ navigation, route }) {
  const { token, user } = useContext(UserContext);
  const { questions: initialQuestions, mode = 'quiz', count = 10 } = route.params || {};

  const [questions, setQuestions] = useState(initialQuestions || []);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [selectedAnswer, setSelectedAnswer] = useState('');
  const [answers, setAnswers] = useState({});
  const [timeRemaining, setTimeRemaining] = useState(30 * 60); // 30 minutes in seconds
  const [startTime, setStartTime] = useState(Date.now());
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!initialQuestions && mode === 'quiz') {
      loadRandomQuestions();
    }
  }, []);

  useEffect(() => {
    const timer = setInterval(() => {
      setTimeRemaining(prev => {
        if (prev <= 1) {
          handleSubmitQuiz();
          return 0;
        }
        return prev - 1;
      });
    }, 1000);

    return () => clearInterval(timer);
  }, []);

  const loadRandomQuestions = async () => {
    setLoading(true);
    try {
      const result = await getRandomQuestions(count, {}, token);
      setQuestions(result.questions);
    } catch (error) {
      Alert.alert('Error', 'Failed to load questions');
      navigation.goBack();
    } finally {
      setLoading(false);
    }
  };

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  const handleAnswerSelect = (answer) => {
    setSelectedAnswer(answer);
    setAnswers(prev => ({
      ...prev,
      [currentQuestionIndex]: answer
    }));
  };

  const handleNext = () => {
    if (currentQuestionIndex < questions.length - 1) {
      setCurrentQuestionIndex(prev => prev + 1);
      setSelectedAnswer(answers[currentQuestionIndex + 1] || '');
    }
  };

  const handlePrevious = () => {
    if (currentQuestionIndex > 0) {
      setCurrentQuestionIndex(prev => prev - 1);
      setSelectedAnswer(answers[currentQuestionIndex - 1] || '');
    }
  };

  const handleSubmitQuiz = async () => {
    const endTime = Date.now();
    const totalTime = Math.floor((endTime - startTime) / 1000);

    // Submit all answers
    const submissionPromises = Object.entries(answers).map(async ([index, answer]) => {
      const question = questions[parseInt(index)];
      if (question && answer) {
        try {
          await submitAttempt(question.id, answer, totalTime / questions.length, token);
        } catch (error) {
          console.error('Failed to submit attempt:', error);
        }
      }
    });

    await Promise.all(submissionPromises);

    const answeredCount = Object.keys(answers).length;
    Alert.alert(
      'Quiz Completed',
      `You answered ${answeredCount} out of ${questions.length} questions in ${formatTime(totalTime)}.`,
      [
        {
          text: 'View Results',
          onPress: () => navigation.navigate('Progress')
        },
        {
          text: 'Take Another Quiz',
          onPress: () => navigation.navigate('Search')
        }
      ]
    );
  };

  const currentQuestion = questions[currentQuestionIndex];
  const progress = ((currentQuestionIndex + 1) / questions.length) * 100;

  if (loading) {
    return (
      <SafeAreaView style={styles.container}>
        <View style={styles.loadingContainer}>
          <Text style={styles.loadingText}>Loading questions...</Text>
        </View>
      </SafeAreaView>
    );
  }

  if (!currentQuestion) {
    return (
      <SafeAreaView style={styles.container}>
        <View style={styles.loadingContainer}>
          <Text style={styles.loadingText}>No questions available</Text>
        </View>
      </SafeAreaView>
    );
  }

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <View style={styles.headerLeft}>
          <Text style={styles.questionCounter}>
            {currentQuestionIndex + 1} of {questions.length}
          </Text>
          <View style={styles.progressBar}>
            <View style={[styles.progressFill, { width: `${progress}%` }]} />
          </View>
        </View>
        <View style={styles.headerRight}>
          <Text style={[styles.timer, timeRemaining < 300 && styles.timerWarning]}>
            {formatTime(timeRemaining)}
          </Text>
        </View>
      </View>

      <ScrollView style={styles.content} showsVerticalScrollIndicator={false}>
        <View style={styles.questionCard}>
          <Text style={styles.questionText}>{currentQuestion.question_text}</Text>

          <View style={styles.optionsContainer}>
            {currentQuestion.options?.map((option, index) => {
              const optionLetter = String.fromCharCode(65 + index); // A, B, C, D
              const isSelected = selectedAnswer === optionLetter;

              return (
                <TouchableOpacity
                  key={index}
                  style={[styles.optionButton, isSelected && styles.optionSelected]}
                  onPress={() => handleAnswerSelect(optionLetter)}
                >
                  <Text style={[styles.optionLetter, isSelected && styles.optionLetterSelected]}>
                    {optionLetter}.
                  </Text>
                  <Text style={[styles.optionText, isSelected && styles.optionTextSelected]}>
                    {option}
                  </Text>
                </TouchableOpacity>
              );
            })}
          </View>
        </View>
      </ScrollView>

      <View style={styles.footer}>
        <TouchableOpacity
          style={[styles.navButton, currentQuestionIndex === 0 && styles.navButtonDisabled]}
          onPress={handlePrevious}
          disabled={currentQuestionIndex === 0}
        >
          <Text style={[styles.navButtonText, currentQuestionIndex === 0 && styles.navButtonTextDisabled]}>
            Previous
          </Text>
        </TouchableOpacity>

        {currentQuestionIndex < questions.length - 1 ? (
          <TouchableOpacity
            style={styles.navButton}
            onPress={handleNext}
          >
            <Text style={styles.navButtonText}>Next</Text>
          </TouchableOpacity>
        ) : (
          <TouchableOpacity
            style={[styles.navButton, styles.submitButton]}
            onPress={handleSubmitQuiz}
          >
            <Text style={styles.submitButtonText}>Submit Quiz</Text>
          </TouchableOpacity>
        )}
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  loadingText: {
    fontSize: 18,
    color: '#666',
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: 15,
    backgroundColor: '#fff',
    borderBottomWidth: 1,
    borderBottomColor: '#e0e0e0',
  },
  headerLeft: {
    flex: 1,
  },
  questionCounter: {
    fontSize: 16,
    fontWeight: '600',
    color: '#333',
    marginBottom: 5,
  },
  progressBar: {
    height: 4,
    backgroundColor: '#e0e0e0',
    borderRadius: 2,
  },
  progressFill: {
    height: '100%',
    backgroundColor: '#3498db',
    borderRadius: 2,
  },
  headerRight: {
    alignItems: 'flex-end',
  },
  timer: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#333',
  },
  timerWarning: {
    color: '#e74c3c',
  },
  content: {
    flex: 1,
    padding: 15,
  },
  questionCard: {
    backgroundColor: '#fff',
    borderRadius: 12,
    padding: 20,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  questionText: {
    fontSize: 18,
    fontWeight: '600',
    color: '#333',
    lineHeight: 24,
    marginBottom: 20,
  },
  optionsContainer: {
    gap: 12,
  },
  optionButton: {
    flexDirection: 'row',
    alignItems: 'flex-start',
    padding: 15,
    borderWidth: 2,
    borderColor: '#e0e0e0',
    borderRadius: 8,
    backgroundColor: '#fff',
  },
  optionSelected: {
    borderColor: '#3498db',
    backgroundColor: '#ebf5fb',
  },
  optionLetter: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#666',
    marginRight: 10,
    minWidth: 20,
  },
  optionLetterSelected: {
    color: '#3498db',
  },
  optionText: {
    fontSize: 16,
    color: '#333',
    flex: 1,
    lineHeight: 22,
  },
  optionTextSelected: {
    color: '#3498db',
    fontWeight: '600',
  },
  footer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    padding: 15,
    backgroundColor: '#fff',
    borderTopWidth: 1,
    borderTopColor: '#e0e0e0',
  },
  navButton: {
    flex: 1,
    padding: 12,
    borderRadius: 6,
    alignItems: 'center',
    marginHorizontal: 5,
    backgroundColor: '#f0f0f0',
  },
  navButtonDisabled: {
    backgroundColor: '#e0e0e0',
  },
  navButtonText: {
    fontSize: 16,
    fontWeight: '600',
    color: '#666',
  },
  navButtonTextDisabled: {
    color: '#ccc',
  },
  submitButton: {
    backgroundColor: '#27ae60',
  },
  submitButtonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: 'bold',
  },
});
