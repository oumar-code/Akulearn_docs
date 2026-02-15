import React, { useState, useEffect, useContext } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  Alert,
  ActivityIndicator,
  Dimensions,
  Animated,
} from 'react-native';
import { UserContext } from '../UserContext';
import {
  getFlashcardDecks,
  getStudySession,
  submitFlashcardResponse,
  getFlashcardStats
} from '../api';

const { width, height } = Dimensions.get('window');

const FlashcardScreen = ({ navigation }) => {
  const { user } = useContext(UserContext);
  const [decks, setDecks] = useState([]);
  const [selectedDeck, setSelectedDeck] = useState(null);
  const [currentCard, setCurrentCard] = useState(null);
  const [showAnswer, setShowAnswer] = useState(false);
  const [sessionCards, setSessionCards] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState('decks');
  const [flipAnimation] = useState(new Animated.Value(0));

  useEffect(() => {
    loadDecks();
    loadStats();
  }, []);

  const loadDecks = async () => {
    try {
      const deckData = await getFlashcardDecks(user?.token);
      setDecks(deckData);
    } catch (error) {
      Alert.alert('Error', 'Failed to load flashcard decks');
    }
  };

  const loadStats = async () => {
    try {
      const statsData = await getFlashcardStats(user?.token);
      setStats(statsData);
    } catch (error) {
      console.log('Failed to load stats');
    }
  };

  const startStudySession = async (deck) => {
    setLoading(true);
    try {
      const sessionData = await getStudySession(deck.id, user?.token);
      setSessionCards(sessionData.cards);
      setSelectedDeck(deck);
      setCurrentIndex(0);
      setCurrentCard(sessionData.cards[0]);
      setShowAnswer(false);
      setActiveTab('study');
    } catch (error) {
      Alert.alert('Error', 'Failed to start study session');
    } finally {
      setLoading(false);
    }
  };

  const flipCard = () => {
    Animated.spring(flipAnimation, {
      toValue: showAnswer ? 0 : 180,
      friction: 8,
      tension: 10,
      useNativeDriver: true,
    }).start();
    setShowAnswer(!showAnswer);
  };

  const submitResponse = async (quality) => {
    if (!currentCard) return;

    try {
      await submitFlashcardResponse(currentCard.id, quality, user?.token);

      // Move to next card
      const nextIndex = currentIndex + 1;
      if (nextIndex < sessionCards.length) {
        setCurrentIndex(nextIndex);
        setCurrentCard(sessionCards[nextIndex]);
        setShowAnswer(false);
        flipAnimation.setValue(0);
      } else {
        // Session complete
        Alert.alert(
          'Session Complete!',
          'Great job! You\'ve completed this study session.',
          [
            {
              text: 'Continue Studying',
              onPress: () => setActiveTab('decks')
            },
            {
              text: 'View Stats',
              onPress: () => setActiveTab('stats')
            }
          ]
        );
        loadStats(); // Refresh stats
      }
    } catch (error) {
      Alert.alert('Error', 'Failed to submit response');
    }
  };

  const renderDecks = () => (
    <ScrollView style={styles.container}>
      <Text style={styles.title}>Flashcards</Text>
      <Text style={styles.subtitle}>Master concepts with spaced repetition</Text>

      {/* Stats Overview */}
      {stats && (
        <View style={styles.statsOverview}>
          <View style={styles.statItem}>
            <Text style={styles.statNumber}>{stats.total_cards}</Text>
            <Text style={styles.statLabel}>Total Cards</Text>
          </View>
          <View style={styles.statItem}>
            <Text style={styles.statNumber}>{stats.studied_today}</Text>
            <Text style={styles.statLabel}>Studied Today</Text>
          </View>
          <View style={styles.statItem}>
            <Text style={styles.statNumber}>{stats.due_today}</Text>
            <Text style={styles.statLabel}>Due Today</Text>
          </View>
        </View>
      )}

      {/* Deck List */}
      {decks.map((deck, index) => (
        <TouchableOpacity
          key={index}
          style={styles.deckCard}
          onPress={() => startStudySession(deck)}
        >
          <View style={styles.deckHeader}>
            <Text style={styles.deckTitle}>{deck.name}</Text>
            <Text style={styles.deckSubject}>{deck.subject}</Text>
          </View>

          <Text style={styles.deckDescription}>{deck.description}</Text>

          <View style={styles.deckStats}>
            <Text style={styles.deckStat}>{deck.card_count} cards</Text>
            <Text style={styles.deckStat}>{deck.due_cards} due</Text>
            <Text style={styles.deckStat}>{deck.new_cards} new</Text>
          </View>

          <View style={styles.progressBar}>
            <View
              style={[
                styles.progressFill,
                { width: `${(deck.mastered_cards / deck.card_count) * 100}%` }
              ]}
            />
          </View>
          <Text style={styles.progressText}>
            {deck.mastered_cards}/{deck.card_count} mastered
          </Text>
        </TouchableOpacity>
      ))}
    </ScrollView>
  );

  const renderStudy = () => (
    <View style={styles.studyContainer}>
      <View style={styles.studyHeader}>
        <TouchableOpacity
          style={styles.backButton}
          onPress={() => setActiveTab('decks')}
        >
          <Text style={styles.backButtonText}>← End Session</Text>
        </TouchableOpacity>

        <Text style={styles.sessionProgress}>
          {currentIndex + 1} / {sessionCards.length}
        </Text>
      </View>

      {loading ? (
        <ActivityIndicator size="large" color="#3498db" style={styles.loader} />
      ) : currentCard ? (
        <View style={styles.cardContainer}>
          {/* Flashcard */}
          <TouchableOpacity
            style={styles.flashcard}
            onPress={flipCard}
            activeOpacity={0.9}
          >
            <Animated.View
              style={[
                styles.cardFace,
                {
                  transform: [
                    {
                      rotateY: flipAnimation.interpolate({
                        inputRange: [0, 180],
                        outputRange: ['0deg', '180deg'],
                      }),
                    },
                  ],
                },
              ]}
            >
              {!showAnswer ? (
                <View style={styles.cardFront}>
                  <Text style={styles.cardQuestion}>{currentCard.question}</Text>
                  <Text style={styles.tapHint}>Tap to reveal answer</Text>
                </View>
              ) : (
                <Animated.View
                  style={[
                    styles.cardBack,
                    {
                      transform: [{ rotateY: '180deg' }],
                    },
                  ]}
                >
                  <Text style={styles.cardAnswer}>{currentCard.answer}</Text>
                </Animated.View>
              )}
            </Animated.View>
          </TouchableOpacity>

          {/* Answer Buttons */}
          {showAnswer && (
            <View style={styles.answerButtons}>
              <TouchableOpacity
                style={[styles.answerButton, styles.againButton]}
                onPress={() => submitResponse(1)}
              >
                <Text style={styles.againButtonText}>Again</Text>
              </TouchableOpacity>

              <TouchableOpacity
                style={[styles.answerButton, styles.hardButton]}
                onPress={() => submitResponse(2)}
              >
                <Text style={styles.hardButtonText}>Hard</Text>
              </TouchableOpacity>

              <TouchableOpacity
                style={[styles.answerButton, styles.goodButton]}
                onPress={() => submitResponse(3)}
              >
                <Text style={styles.goodButtonText}>Good</Text>
              </TouchableOpacity>

              <TouchableOpacity
                style={[styles.answerButton, styles.easyButton]}
                onPress={() => submitResponse(4)}
              >
                <Text style={styles.easyButtonText}>Easy</Text>
              </TouchableOpacity>
            </View>
          )}
        </View>
      ) : (
        <Text style={styles.noCardsText}>No cards in this session</Text>
      )}
    </View>
  );

  const renderStats = () => (
    <ScrollView style={styles.container}>
      <View style={styles.header}>
        <TouchableOpacity
          style={styles.backButton}
          onPress={() => setActiveTab('decks')}
        >
          <Text style={styles.backButtonText}>← Back to Decks</Text>
        </TouchableOpacity>
        <Text style={styles.sectionTitle}>Study Statistics</Text>
      </View>

      {stats ? (
        <View style={styles.statsContainer}>
          <View style={styles.statCard}>
            <Text style={styles.statCardTitle}>Today's Progress</Text>
            <View style={styles.statGrid}>
              <View style={styles.statItem}>
                <Text style={styles.statNumber}>{stats.studied_today}</Text>
                <Text style={styles.statLabel}>Cards Studied</Text>
              </View>
              <View style={styles.statItem}>
                <Text style={styles.statNumber}>{stats.minutes_today}</Text>
                <Text style={styles.statLabel}>Minutes</Text>
              </View>
            </View>
          </View>

          <View style={styles.statCard}>
            <Text style={styles.statCardTitle}>Overall Progress</Text>
            <View style={styles.statGrid}>
              <View style={styles.statItem}>
                <Text style={styles.statNumber}>{stats.total_studied}</Text>
                <Text style={styles.statLabel}>Total Studied</Text>
              </View>
              <View style={styles.statItem}>
                <Text style={styles.statNumber}>{stats.current_streak}</Text>
                <Text style={styles.statLabel}>Day Streak</Text>
              </View>
            </View>
          </View>

          <View style={styles.statCard}>
            <Text style={styles.statCardTitle}>Performance</Text>
            <View style={styles.performanceStats}>
              <View style={styles.performanceItem}>
                <Text style={styles.performanceLabel}>Average Response Time</Text>
                <Text style={styles.performanceValue}>{stats.avg_response_time}s</Text>
              </View>
              <View style={styles.performanceItem}>
                <Text style={styles.performanceLabel}>Accuracy Rate</Text>
                <Text style={styles.performanceValue}>{stats.accuracy_rate}%</Text>
              </View>
            </View>
          </View>

          <View style={styles.statCard}>
            <Text style={styles.statCardTitle}>Upcoming Reviews</Text>
            <View style={styles.upcomingReviews}>
              <Text style={styles.reviewItem}>Due today: {stats.due_today} cards</Text>
              <Text style={styles.reviewItem}>Due tomorrow: {stats.due_tomorrow} cards</Text>
              <Text style={styles.reviewItem}>Due this week: {stats.due_week} cards</Text>
            </View>
          </View>
        </View>
      ) : (
        <Text style={styles.noDataText}>No statistics available</Text>
      )}
    </ScrollView>
  );

  const renderContent = () => {
    switch (activeTab) {
      case 'decks':
        return renderDecks();
      case 'study':
        return renderStudy();
      case 'stats':
        return renderStats();
      default:
        return renderDecks();
    }
  };

  return (
    <View style={styles.mainContainer}>
      {renderContent()}
    </View>
  );
};

const styles = StyleSheet.create({
  mainContainer: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  container: {
    flex: 1,
    padding: 16,
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#2c3e50',
    marginBottom: 8,
    textAlign: 'center',
  },
  subtitle: {
    fontSize: 16,
    color: '#666',
    marginBottom: 20,
    textAlign: 'center',
  },
  statsOverview: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    backgroundColor: '#fff',
    borderRadius: 8,
    padding: 16,
    marginBottom: 20,
    elevation: 2,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.1,
    shadowRadius: 2,
  },
  statItem: {
    alignItems: 'center',
  },
  statNumber: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#3498db',
  },
  statLabel: {
    fontSize: 12,
    color: '#666',
    marginTop: 4,
  },
  deckCard: {
    backgroundColor: '#fff',
    borderRadius: 8,
    padding: 16,
    marginBottom: 12,
    elevation: 2,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.1,
    shadowRadius: 2,
  },
  deckHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 8,
  },
  deckTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#2c3e50',
  },
  deckSubject: {
    fontSize: 12,
    color: '#3498db',
    backgroundColor: '#e8f4fd',
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 12,
  },
  deckDescription: {
    fontSize: 14,
    color: '#666',
    marginBottom: 12,
  },
  deckStats: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 12,
  },
  deckStat: {
    fontSize: 12,
    color: '#666',
  },
  progressBar: {
    height: 4,
    backgroundColor: '#ecf0f1',
    borderRadius: 2,
    marginBottom: 8,
  },
  progressFill: {
    height: '100%',
    backgroundColor: '#27ae60',
    borderRadius: 2,
  },
  progressText: {
    fontSize: 12,
    color: '#666',
    textAlign: 'right',
  },
  studyContainer: {
    flex: 1,
    padding: 16,
  },
  studyHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 20,
  },
  backButton: {
    paddingVertical: 8,
  },
  backButtonText: {
    color: '#3498db',
    fontSize: 16,
  },
  sessionProgress: {
    fontSize: 16,
    color: '#666',
  },
  loader: {
    marginTop: 100,
  },
  cardContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  flashcard: {
    width: width * 0.9,
    height: height * 0.5,
    marginBottom: 30,
  },
  cardFace: {
    width: '100%',
    height: '100%',
    backgroundColor: '#fff',
    borderRadius: 12,
    elevation: 4,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.2,
    shadowRadius: 4,
    justifyContent: 'center',
    alignItems: 'center',
    backfaceVisibility: 'hidden',
  },
  cardFront: {
    alignItems: 'center',
    padding: 20,
  },
  cardQuestion: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#2c3e50',
    textAlign: 'center',
    marginBottom: 20,
  },
  tapHint: {
    fontSize: 14,
    color: '#666',
    textAlign: 'center',
  },
  cardBack: {
    alignItems: 'center',
    padding: 20,
  },
  cardAnswer: {
    fontSize: 16,
    color: '#2c3e50',
    textAlign: 'center',
    lineHeight: 24,
  },
  answerButtons: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    width: '100%',
    paddingHorizontal: 10,
  },
  answerButton: {
    paddingVertical: 12,
    paddingHorizontal: 16,
    borderRadius: 8,
    minWidth: 70,
    alignItems: 'center',
  },
  againButton: {
    backgroundColor: '#e74c3c',
  },
  againButtonText: {
    color: '#fff',
    fontWeight: 'bold',
  },
  hardButton: {
    backgroundColor: '#e67e22',
  },
  hardButtonText: {
    color: '#fff',
    fontWeight: 'bold',
  },
  goodButton: {
    backgroundColor: '#f39c12',
  },
  goodButtonText: {
    color: '#fff',
    fontWeight: 'bold',
  },
  easyButton: {
    backgroundColor: '#27ae60',
  },
  easyButtonText: {
    color: '#fff',
    fontWeight: 'bold',
  },
  noCardsText: {
    fontSize: 16,
    color: '#666',
    textAlign: 'center',
    marginTop: 100,
  },
  header: {
    marginBottom: 20,
  },
  sectionTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#2c3e50',
  },
  statsContainer: {
    paddingBottom: 20,
  },
  statCard: {
    backgroundColor: '#fff',
    borderRadius: 8,
    padding: 16,
    marginBottom: 12,
    elevation: 2,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.1,
    shadowRadius: 2,
  },
  statCardTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#2c3e50',
    marginBottom: 16,
  },
  statGrid: {
    flexDirection: 'row',
    justifyContent: 'space-around',
  },
  performanceStats: {
    paddingTop: 8,
  },
  performanceItem: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingVertical: 8,
    borderBottomWidth: 1,
    borderBottomColor: '#ecf0f1',
  },
  performanceLabel: {
    fontSize: 14,
    color: '#666',
  },
  performanceValue: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#2c3e50',
  },
  upcomingReviews: {
    paddingTop: 8,
  },
  reviewItem: {
    fontSize: 14,
    color: '#666',
    marginBottom: 8,
  },
  noDataText: {
    fontSize: 16,
    color: '#666',
    textAlign: 'center',
    marginTop: 50,
  },
});

export default FlashcardScreen;