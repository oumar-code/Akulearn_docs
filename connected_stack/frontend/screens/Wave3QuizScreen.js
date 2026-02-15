import React, { useState, useContext, useEffect } from 'react';
import {
  View,
  Text,
  TouchableOpacity,
  StyleSheet,
  ActivityIndicator,
  SafeAreaView,
  ScrollView,
  Modal,
  Animated,
} from 'react-native';
import { UserContext } from '../UserContext';
import {
  getWave3Lesson,
  submitWave3Quiz,
  recordWave3Activity,
  getWave3StudentStats,
} from '../api';

export default function Wave3QuizScreen({ route, navigation }) {
  const { lessonId } = route.params;
  const { user } = useContext(UserContext);
  const [lesson, setLesson] = useState(null);
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [answers, setAnswers] = useState({});
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [showResults, setShowResults] = useState(false);
  const [quizResults, setQuizResults] = useState(null);
  const [studentStats, setStudentStats] = useState(null);
  const [startTime, setStartTime] = useState(Date.now());
  const scoreAnimation = new Animated.Value(0);

  useEffect(() => {
    loadLesson();
    loadStudentStats();
  }, []);

  const loadLesson = async () => {
    try {
      const data = await getWave3Lesson(lessonId, user?.token);
      setLesson(data);
    } catch (err) {
      console.error('Failed to load lesson:', err);
    } finally {
      setLoading(false);
    }
  };

  const loadStudentStats = async () => {
    try {
      const studentId = user?.id || 'student_001';
      const stats = await getWave3StudentStats(studentId, user?.token);
      setStudentStats(stats);
    } catch (err) {
      console.error('Failed to load student stats:', err);
    }
  };

  const handleAnswer = (questionIndex, answer) => {
    setAnswers({ ...answers, [questionIndex]: answer });
  };

  const handleNext = () => {
    if (currentQuestion < lesson.practice_problems.length - 1) {
      setCurrentQuestion(currentQuestion + 1);
    }
  };

  const handlePrevious = () => {
    if (currentQuestion > 0) {
      setCurrentQuestion(currentQuestion - 1);
    }
  };

  const handleSubmit = async () => {
    setSubmitting(true);
    try {
      const studentId = user?.id || 'student_001';
      const timeElapsed = Math.floor((Date.now() - startTime) / 1000);
      
      // Calculate score
      const questions = lesson.practice_problems;
      let correctCount = 0;
      const answerDetails = questions.map((q, index) => {
        const userAnswer = answers[index];
        const isCorrect = userAnswer === q.correct_answer;
        if (isCorrect) correctCount++;
        return {
          question_id: `${lessonId}_q${index}`,
          user_answer: userAnswer,
          correct_answer: q.correct_answer,
          is_correct: isCorrect,
        };
      });

      // Submit quiz
      const quizData = {
        quiz_id: `quiz_${lessonId}_${Date.now()}`,
        lesson_id: lessonId,
        student_id: studentId,
        score: correctCount,
        max_score: questions.length,
        time_taken_seconds: timeElapsed,
        questions_correct: correctCount,
        questions_total: questions.length,
        answers: answerDetails,
      };

      const results = await submitWave3Quiz(quizData, user?.token);
      setQuizResults(results);
      
      // Animate score
      Animated.spring(scoreAnimation, {
        toValue: (correctCount / questions.length) * 100,
        useNativeDriver: false,
      }).start();

      // Reload stats to show new achievements
      await loadStudentStats();
      
      setShowResults(true);
    } catch (err) {
      console.error('Failed to submit quiz:', err);
      alert('Failed to submit quiz. Please try again.');
    } finally {
      setSubmitting(false);
    }
  };

  const renderAchievementBadge = (achievement) => {
    const badgeColors = {
      Bronze: '#CD7F32',
      Silver: '#C0C0C0',
      Gold: '#FFD700',
      Platinum: '#E5E4E2',
      Diamond: '#B9F2FF',
    };

    return (
      <View
        key={achievement.id}
        style={[
          styles.achievementBadge,
          { backgroundColor: badgeColors[achievement.badge_level] || '#ccc' },
        ]}
      >
        <Text style={styles.achievementIcon}>{achievement.icon}</Text>
        <Text style={styles.achievementName}>{achievement.name}</Text>
      </View>
    );
  };

  if (loading) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color="#3498db" />
        <Text style={styles.loadingText}>Loading quiz...</Text>
      </View>
    );
  }

  if (!lesson || !lesson.practice_problems || lesson.practice_problems.length === 0) {
    return (
      <View style={styles.errorContainer}>
        <Text style={styles.errorText}>No quiz questions available</Text>
        <TouchableOpacity
          style={styles.button}
          onPress={() => navigation.goBack()}
        >
          <Text style={styles.buttonText}>Go Back</Text>
        </TouchableOpacity>
      </View>
    );
  }

  const question = lesson.practice_problems[currentQuestion];
  const hasAnswered = answers.hasOwnProperty(currentQuestion);
  const allAnswered = Object.keys(answers).length === lesson.practice_problems.length;

  return (
    <SafeAreaView style={styles.container}>
      {/* Student Stats Header */}
      {studentStats && (
        <View style={styles.statsHeader}>
          <View style={styles.statItem}>
            <Text style={styles.statValue}>{studentStats.points}</Text>
            <Text style={styles.statLabel}>Points</Text>
          </View>
          <View style={styles.statItem}>
            <Text style={styles.statValue}>{studentStats.level}</Text>
            <Text style={styles.statLabel}>Level</Text>
          </View>
          <View style={styles.statItem}>
            <Text style={styles.statValue}>{studentStats.streak?.current_streak || 0}</Text>
            <Text style={styles.statLabel}>🔥 Streak</Text>
          </View>
        </View>
      )}

      {/* Progress Bar */}
      <View style={styles.progressContainer}>
        <View style={styles.progressBar}>
          <View
            style={[
              styles.progressFill,
              {
                width: `${
                  ((currentQuestion + 1) / lesson.practice_problems.length) * 100
                }%`,
              },
            ]}
          />
        </View>
        <Text style={styles.progressText}>
          Question {currentQuestion + 1} of {lesson.practice_problems.length}
        </Text>
      </View>

      <ScrollView style={styles.scrollView}>
        {/* Question */}
        <View style={styles.questionContainer}>
          <Text style={styles.questionText}>{question.question}</Text>
        </View>

        {/* Options */}
        <View style={styles.optionsContainer}>
          {question.options?.map((option, index) => (
            <TouchableOpacity
              key={index}
              style={[
                styles.option,
                answers[currentQuestion] === option && styles.optionSelected,
              ]}
              onPress={() => handleAnswer(currentQuestion, option)}
            >
              <View style={styles.optionCircle}>
                {answers[currentQuestion] === option && (
                  <View style={styles.optionCircleInner} />
                )}
              </View>
              <Text
                style={[
                  styles.optionText,
                  answers[currentQuestion] === option && styles.optionTextSelected,
                ]}
              >
                {option}
              </Text>
            </TouchableOpacity>
          ))}
        </View>
      </ScrollView>

      {/* Navigation Buttons */}
      <View style={styles.navigationContainer}>
        <TouchableOpacity
          style={[styles.navButton, currentQuestion === 0 && styles.navButtonDisabled]}
          onPress={handlePrevious}
          disabled={currentQuestion === 0}
        >
          <Text style={styles.navButtonText}>← Previous</Text>
        </TouchableOpacity>

        {currentQuestion === lesson.practice_problems.length - 1 ? (
          <TouchableOpacity
            style={[
              styles.submitButton,
              (!allAnswered || submitting) && styles.submitButtonDisabled,
            ]}
            onPress={handleSubmit}
            disabled={!allAnswered || submitting}
          >
            {submitting ? (
              <ActivityIndicator color="#fff" />
            ) : (
              <Text style={styles.submitButtonText}>Submit Quiz</Text>
            )}
          </TouchableOpacity>
        ) : (
          <TouchableOpacity
            style={[
              styles.navButton,
              !hasAnswered && styles.navButtonDisabled,
            ]}
            onPress={handleNext}
            disabled={!hasAnswered}
          >
            <Text style={styles.navButtonText}>Next →</Text>
          </TouchableOpacity>
        )}
      </View>

      {/* Results Modal */}
      <Modal
        visible={showResults}
        transparent
        animationType="slide"
        onRequestClose={() => setShowResults(false)}
      >
        <View style={styles.modalOverlay}>
          <View style={styles.modalContent}>
            <Text style={styles.modalTitle}>Quiz Complete! 🎉</Text>
            
            {quizResults && (
              <>
                <View style={styles.scoreCircle}>
                  <Text style={styles.scoreValue}>
                    {Math.round(
                      (quizResults.questions_correct / quizResults.questions_total) * 100
                    )}
                    %
                  </Text>
                  <Text style={styles.scoreLabel}>Score</Text>
                </View>

                <View style={styles.resultsStats}>
                  <View style={styles.resultStat}>
                    <Text style={styles.resultStatValue}>
                      {quizResults.questions_correct}/{quizResults.questions_total}
                    </Text>
                    <Text style={styles.resultStatLabel}>Correct</Text>
                  </View>
                  <View style={styles.resultStat}>
                    <Text style={styles.resultStatValue}>
                      {Math.floor(quizResults.time_taken_seconds / 60)}m{' '}
                      {quizResults.time_taken_seconds % 60}s
                    </Text>
                    <Text style={styles.resultStatLabel}>Time</Text>
                  </View>
                </View>

                {/* New Achievements */}
                {quizResults.new_achievements &&
                  quizResults.new_achievements.length > 0 && (
                    <View style={styles.achievementsContainer}>
                      <Text style={styles.achievementsTitle}>
                        🏆 New Achievements!
                      </Text>
                      <ScrollView horizontal showsHorizontalScrollIndicator={false}>
                        {quizResults.new_achievements.map(renderAchievementBadge)}
                      </ScrollView>
                    </View>
                  )}

                {/* Points Earned */}
                <View style={styles.pointsEarned}>
                  <Text style={styles.pointsText}>
                    +{quizResults.points_earned || 0} Points
                  </Text>
                </View>
              </>
            )}

            <TouchableOpacity
              style={styles.modalButton}
              onPress={() => {
                setShowResults(false);
                navigation.goBack();
              }}
            >
              <Text style={styles.modalButtonText}>Continue</Text>
            </TouchableOpacity>
          </View>
        </View>
      </Modal>
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
    marginTop: 10,
    fontSize: 16,
    color: '#666',
  },
  errorContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 20,
  },
  errorText: {
    fontSize: 16,
    color: '#e74c3c',
    textAlign: 'center',
    marginBottom: 20,
  },
  statsHeader: {
    flexDirection: 'row',
    backgroundColor: '#fff',
    padding: 15,
    justifyContent: 'space-around',
    borderBottomWidth: 1,
    borderBottomColor: '#e0e0e0',
  },
  statItem: {
    alignItems: 'center',
  },
  statValue: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#3498db',
  },
  statLabel: {
    fontSize: 12,
    color: '#666',
    marginTop: 4,
  },
  progressContainer: {
    backgroundColor: '#fff',
    padding: 15,
  },
  progressBar: {
    height: 8,
    backgroundColor: '#e0e0e0',
    borderRadius: 4,
    overflow: 'hidden',
    marginBottom: 10,
  },
  progressFill: {
    height: '100%',
    backgroundColor: '#4CAF50',
  },
  progressText: {
    fontSize: 14,
    color: '#666',
    textAlign: 'center',
  },
  scrollView: {
    flex: 1,
  },
  questionContainer: {
    backgroundColor: '#fff',
    padding: 20,
    margin: 15,
    borderRadius: 10,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  questionText: {
    fontSize: 18,
    color: '#333',
    lineHeight: 26,
  },
  optionsContainer: {
    padding: 15,
  },
  option: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#fff',
    padding: 15,
    borderRadius: 10,
    marginBottom: 10,
    borderWidth: 2,
    borderColor: '#e0e0e0',
  },
  optionSelected: {
    borderColor: '#3498db',
    backgroundColor: '#e3f2fd',
  },
  optionCircle: {
    width: 24,
    height: 24,
    borderRadius: 12,
    borderWidth: 2,
    borderColor: '#ccc',
    marginRight: 15,
    justifyContent: 'center',
    alignItems: 'center',
  },
  optionCircleInner: {
    width: 12,
    height: 12,
    borderRadius: 6,
    backgroundColor: '#3498db',
  },
  optionText: {
    flex: 1,
    fontSize: 16,
    color: '#333',
  },
  optionTextSelected: {
    color: '#3498db',
    fontWeight: '600',
  },
  navigationContainer: {
    flexDirection: 'row',
    padding: 15,
    backgroundColor: '#fff',
    borderTopWidth: 1,
    borderTopColor: '#e0e0e0',
  },
  navButton: {
    flex: 1,
    backgroundColor: '#3498db',
    padding: 15,
    borderRadius: 8,
    alignItems: 'center',
    marginHorizontal: 5,
  },
  navButtonDisabled: {
    backgroundColor: '#ccc',
  },
  navButtonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
  },
  submitButton: {
    flex: 1,
    backgroundColor: '#4CAF50',
    padding: 15,
    borderRadius: 8,
    alignItems: 'center',
    marginHorizontal: 5,
  },
  submitButtonDisabled: {
    backgroundColor: '#ccc',
  },
  submitButtonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: 'bold',
  },
  button: {
    backgroundColor: '#3498db',
    padding: 15,
    borderRadius: 8,
    alignItems: 'center',
  },
  buttonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
  },
  modalOverlay: {
    flex: 1,
    backgroundColor: 'rgba(0, 0, 0, 0.5)',
    justifyContent: 'center',
    alignItems: 'center',
  },
  modalContent: {
    backgroundColor: '#fff',
    borderRadius: 20,
    padding: 30,
    width: '85%',
    maxHeight: '80%',
  },
  modalTitle: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#333',
    textAlign: 'center',
    marginBottom: 20,
  },
  scoreCircle: {
    width: 120,
    height: 120,
    borderRadius: 60,
    backgroundColor: '#4CAF50',
    justifyContent: 'center',
    alignItems: 'center',
    alignSelf: 'center',
    marginBottom: 20,
  },
  scoreValue: {
    fontSize: 32,
    fontWeight: 'bold',
    color: '#fff',
  },
  scoreLabel: {
    fontSize: 14,
    color: '#fff',
    marginTop: 5,
  },
  resultsStats: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    marginBottom: 20,
  },
  resultStat: {
    alignItems: 'center',
  },
  resultStatValue: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#333',
  },
  resultStatLabel: {
    fontSize: 14,
    color: '#666',
    marginTop: 5,
  },
  achievementsContainer: {
    marginBottom: 20,
  },
  achievementsTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 10,
  },
  achievementBadge: {
    padding: 10,
    borderRadius: 8,
    marginRight: 10,
    alignItems: 'center',
    minWidth: 80,
  },
  achievementIcon: {
    fontSize: 24,
    marginBottom: 5,
  },
  achievementName: {
    fontSize: 12,
    color: '#fff',
    fontWeight: '600',
  },
  pointsEarned: {
    backgroundColor: '#FFF9C4',
    padding: 15,
    borderRadius: 8,
    marginBottom: 20,
  },
  pointsText: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#F57F17',
    textAlign: 'center',
  },
  modalButton: {
    backgroundColor: '#3498db',
    padding: 15,
    borderRadius: 8,
    alignItems: 'center',
  },
  modalButtonText: {
    color: '#fff',
    fontSize: 18,
    fontWeight: 'bold',
  },
});
