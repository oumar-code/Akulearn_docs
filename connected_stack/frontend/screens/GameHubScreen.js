import React, { useState, useEffect, useContext } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  FlatList,
  Alert,
  ActivityIndicator,
  Dimensions,
} from 'react-native';
import { UserContext } from '../UserContext';
import {
  getGameData,
  getGameLeaderboard,
  startGameSession,
  submitGameScore
} from '../api';

const { width, height } = Dimensions.get('window');

const GameHubScreen = ({ navigation }) => {
  const { user } = useContext(UserContext);
  const [games, setGames] = useState([]);
  const [selectedGame, setSelectedGame] = useState(null);
  const [leaderboard, setLeaderboard] = useState([]);
  const [userStats, setUserStats] = useState(null);
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState('games');

  useEffect(() => {
    loadGames();
    loadUserStats();
  }, []);

  const loadGames = async () => {
    try {
      const gameData = await getGameData(user?.token);
      setGames(gameData);
    } catch (error) {
      Alert.alert('Error', 'Failed to load games');
    }
  };

  const loadUserStats = async () => {
    try {
      // This would be a new API endpoint for user game stats
      // For now, we'll use placeholder data
      setUserStats({
        total_games_played: 15,
        total_score: 2450,
        average_score: 163,
        best_game: 'Math Quiz',
        achievements: ['First Win', 'Speed Demon', 'Perfect Score']
      });
    } catch (error) {
      console.log('Failed to load user stats');
    }
  };

  const loadLeaderboard = async (gameId) => {
    setLoading(true);
    try {
      const leaderboardData = await getGameLeaderboard(gameId, user?.token);
      setLeaderboard(leaderboardData);
      setActiveTab('leaderboard');
    } catch (error) {
      Alert.alert('Error', 'Failed to load leaderboard');
    } finally {
      setLoading(false);
    }
  };

  const startGame = (game) => {
    setSelectedGame(game);
    navigation.navigate('GamePlay', { game });
  };

  const renderGames = () => (
    <ScrollView style={styles.container}>
      <Text style={styles.title}>Game Hub</Text>
      <Text style={styles.subtitle}>Learn through interactive games</Text>

      {/* User Stats */}
      {userStats && (
        <View style={styles.statsCard}>
          <Text style={styles.statsTitle}>Your Gaming Stats</Text>
          <View style={styles.statsGrid}>
            <View style={styles.statItem}>
              <Text style={styles.statNumber}>{userStats.total_games_played}</Text>
              <Text style={styles.statLabel}>Games Played</Text>
            </View>
            <View style={styles.statItem}>
              <Text style={styles.statNumber}>{userStats.total_score}</Text>
              <Text style={styles.statLabel}>Total Score</Text>
            </View>
            <View style={styles.statItem}>
              <Text style={styles.statNumber}>{userStats.average_score}</Text>
              <Text style={styles.statLabel}>Avg Score</Text>
            </View>
          </View>

          <View style={styles.achievements}>
            <Text style={styles.achievementsTitle}>Achievements</Text>
            <View style={styles.achievementBadges}>
              {userStats.achievements.map((achievement, index) => (
                <View key={index} style={styles.achievementBadge}>
                  <Text style={styles.achievementText}>{achievement}</Text>
                </View>
              ))}
            </View>
          </View>
        </View>
      )}

      {/* Game Categories */}
      <Text style={styles.sectionTitle}>Game Categories</Text>
      <View style={styles.categoriesGrid}>
        {['Mathematics', 'Science', 'Language', 'General Knowledge'].map((category, index) => (
          <TouchableOpacity
            key={index}
            style={styles.categoryCard}
            onPress={() => {
              // Filter games by category
              const filteredGames = games.filter(game => game.category === category);
              setGames(filteredGames);
            }}
          >
            <Text style={styles.categoryIcon}>
              {category === 'Mathematics' ? '🔢' :
               category === 'Science' ? '🧪' :
               category === 'Language' ? '📝' : '🧠'}
            </Text>
            <Text style={styles.categoryTitle}>{category}</Text>
          </TouchableOpacity>
        ))}
      </View>

      {/* Games List */}
      <Text style={styles.sectionTitle}>Available Games</Text>
      {games.map((game, index) => (
        <View key={index} style={styles.gameCard}>
          <View style={styles.gameHeader}>
            <Text style={styles.gameTitle}>{game.title}</Text>
            <Text style={styles.gameCategory}>{game.category}</Text>
          </View>

          <Text style={styles.gameDescription}>{game.description}</Text>

          <View style={styles.gameStats}>
            <Text style={styles.gameStat}>⏱️ {game.estimated_time} min</Text>
            <Text style={styles.gameStat}>⭐ {game.difficulty}</Text>
            <Text style={styles.gameStat}>🏆 {game.high_score || 'N/A'}</Text>
          </View>

          <View style={styles.gameActions}>
            <TouchableOpacity
              style={styles.playButton}
              onPress={() => startGame(game)}
            >
              <Text style={styles.playButtonText}>Play Now</Text>
            </TouchableOpacity>

            <TouchableOpacity
              style={styles.leaderboardButton}
              onPress={() => loadLeaderboard(game.id)}
            >
              <Text style={styles.leaderboardButtonText}>Leaderboard</Text>
            </TouchableOpacity>
          </View>
        </View>
      ))}
    </ScrollView>
  );

  const renderLeaderboard = () => (
    <ScrollView style={styles.container}>
      <View style={styles.header}>
        <TouchableOpacity
          style={styles.backButton}
          onPress={() => setActiveTab('games')}
        >
          <Text style={styles.backButtonText}>← Back to Games</Text>
        </TouchableOpacity>
        <Text style={styles.sectionTitle}>Leaderboard</Text>
      </View>

      {loading ? (
        <ActivityIndicator size="large" color="#3498db" style={styles.loader} />
      ) : (
        <View style={styles.leaderboardContainer}>
          {leaderboard.map((entry, index) => (
            <View key={index} style={[
              styles.leaderboardEntry,
              index < 3 && styles.topThreeEntry
            ]}>
              <View style={styles.rankContainer}>
                <Text style={[
                  styles.rankNumber,
                  index < 3 && styles.topThreeRank
                ]}>
                  {index + 1}
                </Text>
                {index < 3 && (
                  <Text style={styles.rankMedal}>
                    {index === 0 ? '🥇' : index === 1 ? '🥈' : '🥉'}
                  </Text>
                )}
              </View>

              <View style={styles.playerInfo}>
                <Text style={styles.playerName}>{entry.player_name}</Text>
                <Text style={styles.playerScore}>{entry.score} points</Text>
              </View>

              <Text style={styles.entryDate}>{entry.date}</Text>
            </View>
          ))}
        </View>
      )}
    </ScrollView>
  );

  const renderContent = () => {
    switch (activeTab) {
      case 'games':
        return renderGames();
      case 'leaderboard':
        return renderLeaderboard();
      default:
        return renderGames();
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
  statsCard: {
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
  statsTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#2c3e50',
    marginBottom: 16,
  },
  statsGrid: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    marginBottom: 16,
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
  achievements: {
    borderTopWidth: 1,
    borderTopColor: '#ecf0f1',
    paddingTop: 16,
  },
  achievementsTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#2c3e50',
    marginBottom: 12,
  },
  achievementBadges: {
    flexDirection: 'row',
    flexWrap: 'wrap',
  },
  achievementBadge: {
    backgroundColor: '#f39c12',
    borderRadius: 16,
    paddingHorizontal: 12,
    paddingVertical: 6,
    margin: 4,
  },
  achievementText: {
    color: '#fff',
    fontSize: 12,
    fontWeight: 'bold',
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#2c3e50',
    marginBottom: 12,
  },
  categoriesGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'space-between',
    marginBottom: 20,
  },
  categoryCard: {
    backgroundColor: '#fff',
    borderRadius: 8,
    padding: 16,
    width: '48%',
    alignItems: 'center',
    marginBottom: 12,
    elevation: 2,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.1,
    shadowRadius: 2,
  },
  categoryIcon: {
    fontSize: 32,
    marginBottom: 8,
  },
  categoryTitle: {
    fontSize: 14,
    fontWeight: 'bold',
    color: '#2c3e50',
    textAlign: 'center',
  },
  gameCard: {
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
  gameHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 8,
  },
  gameTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#2c3e50',
  },
  gameCategory: {
    fontSize: 12,
    color: '#3498db',
    backgroundColor: '#e8f4fd',
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 12,
  },
  gameDescription: {
    fontSize: 14,
    color: '#666',
    marginBottom: 12,
  },
  gameStats: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 16,
  },
  gameStat: {
    fontSize: 12,
    color: '#666',
  },
  gameActions: {
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  playButton: {
    backgroundColor: '#27ae60',
    paddingVertical: 10,
    paddingHorizontal: 20,
    borderRadius: 6,
    flex: 1,
    marginHorizontal: 4,
    alignItems: 'center',
  },
  playButtonText: {
    color: '#fff',
    fontSize: 14,
    fontWeight: 'bold',
  },
  leaderboardButton: {
    backgroundColor: '#3498db',
    paddingVertical: 10,
    paddingHorizontal: 20,
    borderRadius: 6,
    flex: 1,
    marginHorizontal: 4,
    alignItems: 'center',
  },
  leaderboardButtonText: {
    color: '#fff',
    fontSize: 14,
    fontWeight: 'bold',
  },
  header: {
    marginBottom: 20,
  },
  backButton: {
    marginBottom: 12,
  },
  backButtonText: {
    color: '#3498db',
    fontSize: 16,
  },
  loader: {
    marginTop: 50,
  },
  leaderboardContainer: {
    paddingBottom: 20,
  },
  leaderboardEntry: {
    backgroundColor: '#fff',
    borderRadius: 8,
    padding: 16,
    marginBottom: 8,
    flexDirection: 'row',
    alignItems: 'center',
    elevation: 1,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.1,
    shadowRadius: 1,
  },
  topThreeEntry: {
    backgroundColor: '#f8f9fa',
    borderWidth: 2,
    borderColor: '#f39c12',
  },
  rankContainer: {
    width: 40,
    alignItems: 'center',
  },
  rankNumber: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#666',
  },
  topThreeRank: {
    color: '#f39c12',
    fontSize: 20,
  },
  rankMedal: {
    fontSize: 16,
    marginTop: 4,
  },
  playerInfo: {
    flex: 1,
    marginLeft: 12,
  },
  playerName: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#2c3e50',
  },
  playerScore: {
    fontSize: 14,
    color: '#666',
  },
  entryDate: {
    fontSize: 12,
    color: '#95a5a6',
  },
});

export default GameHubScreen;