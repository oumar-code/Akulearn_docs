import React, { useState, useContext, useEffect } from 'react';
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  FlatList,
  StyleSheet,
  ActivityIndicator,
  SafeAreaView,
  ScrollView,
} from 'react-native';
import { UserContext } from '../UserContext';
import { searchWave3Lessons, getWave3Recommendations, recordWave3Interaction } from '../api';

export default function Wave3SearchScreen({ navigation }) {
  const { user } = useContext(UserContext);
  const [searchQuery, setSearchQuery] = useState('');
  const [searchType, setSearchType] = useState('keyword'); // keyword, nerdc, waec
  const [results, setResults] = useState([]);
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    loadRecommendations();
  }, []);

  const loadRecommendations = async () => {
    try {
      const studentId = user?.id || 'student_001';
      const recs = await getWave3Recommendations(studentId, 'hybrid', 5, user?.token);
      setRecommendations(recs.recommendations || []);
    } catch (err) {
      console.error('Failed to load recommendations:', err);
    }
  };

  const handleSearch = async () => {
    if (!searchQuery.trim()) {
      setError('Please enter a search query');
      return;
    }

    setLoading(true);
    setError('');
    try {
      const data = await searchWave3Lessons(searchQuery, searchType, user?.token);
      setResults(data.lessons || []);
      if (data.lessons.length === 0) {
        setError('No lessons found');
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleLessonPress = async (lesson) => {
    // Record interaction for recommendations
    try {
      const studentId = user?.id || 'student_001';
      await recordWave3Interaction(
        studentId,
        lesson.id,
        'view',
        { source: 'search' },
        user?.token
      );
    } catch (err) {
      console.error('Failed to record interaction:', err);
    }

    navigation.navigate('Wave3Lesson', { lessonId: lesson.id });
  };

  const renderLesson = ({ item }) => (
    <TouchableOpacity
      style={styles.lessonCard}
      onPress={() => handleLessonPress(item)}
    >
      <View style={styles.lessonHeader}>
        <Text style={styles.lessonSubject}>{item.subject}</Text>
        <Text style={styles.lessonDifficulty}>{item.difficulty_level}</Text>
      </View>
      <Text style={styles.lessonTitle}>{item.title}</Text>
      <Text style={styles.lessonDescription} numberOfLines={2}>
        {item.description}
      </Text>
      <View style={styles.lessonMeta}>
        <Text style={styles.metaText}>⏱️ {item.duration_minutes} min</Text>
        <Text style={styles.metaText}>📚 {item.num_objectives} objectives</Text>
        <Text style={styles.metaText}>📝 {item.num_problems} problems</Text>
      </View>
      {item.nerdc_codes && item.nerdc_codes.length > 0 && (
        <View style={styles.tags}>
          {item.nerdc_codes.slice(0, 3).map((code, index) => (
            <View key={index} style={styles.tag}>
              <Text style={styles.tagText}>{code}</Text>
            </View>
          ))}
        </View>
      )}
    </TouchableOpacity>
  );

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView style={styles.scrollView}>
        {/* Search Section */}
        <View style={styles.searchSection}>
          <Text style={styles.sectionTitle}>Search Lessons</Text>
          
          {/* Search Type Selector */}
          <View style={styles.searchTypeContainer}>
            {['keyword', 'nerdc', 'waec'].map((type) => (
              <TouchableOpacity
                key={type}
                style={[
                  styles.searchTypeButton,
                  searchType === type && styles.searchTypeActive,
                ]}
                onPress={() => setSearchType(type)}
              >
                <Text
                  style={[
                    styles.searchTypeText,
                    searchType === type && styles.searchTypeTextActive,
                  ]}
                >
                  {type.toUpperCase()}
                </Text>
              </TouchableOpacity>
            ))}
          </View>

          {/* Search Input */}
          <View style={styles.searchInputContainer}>
            <TextInput
              style={styles.searchInput}
              placeholder={`Search by ${searchType}...`}
              value={searchQuery}
              onChangeText={setSearchQuery}
              onSubmitEditing={handleSearch}
            />
            <TouchableOpacity
              style={styles.searchButton}
              onPress={handleSearch}
              disabled={loading}
            >
              {loading ? (
                <ActivityIndicator color="#fff" />
              ) : (
                <Text style={styles.searchButtonText}>Search</Text>
              )}
            </TouchableOpacity>
          </View>

          {error ? <Text style={styles.errorText}>{error}</Text> : null}
        </View>

        {/* Recommendations Section */}
        {recommendations.length > 0 && results.length === 0 && (
          <View style={styles.recommendationsSection}>
            <Text style={styles.sectionTitle}>Recommended for You</Text>
            <Text style={styles.sectionSubtitle}>
              Based on your learning history and preferences
            </Text>
            {recommendations.map((item, index) => (
              <TouchableOpacity
                key={index}
                style={styles.recommendationCard}
                onPress={() => handleLessonPress(item.lesson)}
              >
                <Text style={styles.lessonTitle}>{item.lesson.title}</Text>
                <Text style={styles.lessonDescription} numberOfLines={1}>
                  {item.lesson.subject} • {item.lesson.difficulty_level}
                </Text>
                <View style={styles.scoreContainer}>
                  <Text style={styles.scoreLabel}>Match:</Text>
                  <View style={styles.scoreBar}>
                    <View
                      style={[
                        styles.scoreFill,
                        { width: `${item.score * 100}%` },
                      ]}
                    />
                  </View>
                  <Text style={styles.scoreText}>{Math.round(item.score * 100)}%</Text>
                </View>
              </TouchableOpacity>
            ))}
          </View>
        )}

        {/* Results Section */}
        {results.length > 0 && (
          <View style={styles.resultsSection}>
            <Text style={styles.sectionTitle}>
              {results.length} Result{results.length !== 1 ? 's' : ''} Found
            </Text>
            <FlatList
              data={results}
              renderItem={renderLesson}
              keyExtractor={(item) => item.id}
              scrollEnabled={false}
            />
          </View>
        )}
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  scrollView: {
    flex: 1,
  },
  searchSection: {
    backgroundColor: '#fff',
    padding: 20,
    marginBottom: 10,
  },
  sectionTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 10,
  },
  sectionSubtitle: {
    fontSize: 14,
    color: '#666',
    marginBottom: 15,
  },
  searchTypeContainer: {
    flexDirection: 'row',
    marginBottom: 15,
  },
  searchTypeButton: {
    flex: 1,
    padding: 10,
    backgroundColor: '#f0f0f0',
    borderRadius: 8,
    marginHorizontal: 5,
    alignItems: 'center',
  },
  searchTypeActive: {
    backgroundColor: '#3498db',
  },
  searchTypeText: {
    color: '#666',
    fontWeight: '600',
  },
  searchTypeTextActive: {
    color: '#fff',
  },
  searchInputContainer: {
    flexDirection: 'row',
    marginBottom: 10,
  },
  searchInput: {
    flex: 1,
    borderWidth: 1,
    borderColor: '#ddd',
    padding: 12,
    borderRadius: 8,
    fontSize: 16,
    marginRight: 10,
  },
  searchButton: {
    backgroundColor: '#3498db',
    padding: 12,
    borderRadius: 8,
    justifyContent: 'center',
    alignItems: 'center',
    minWidth: 80,
  },
  searchButtonText: {
    color: '#fff',
    fontWeight: '600',
    fontSize: 16,
  },
  errorText: {
    color: '#e74c3c',
    marginTop: 10,
  },
  recommendationsSection: {
    backgroundColor: '#fff',
    padding: 20,
    marginBottom: 10,
  },
  recommendationCard: {
    backgroundColor: '#f8f9fa',
    padding: 15,
    borderRadius: 8,
    marginBottom: 10,
  },
  scoreContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    marginTop: 10,
  },
  scoreLabel: {
    fontSize: 12,
    color: '#666',
    marginRight: 10,
  },
  scoreBar: {
    flex: 1,
    height: 6,
    backgroundColor: '#e0e0e0',
    borderRadius: 3,
    overflow: 'hidden',
  },
  scoreFill: {
    height: '100%',
    backgroundColor: '#4CAF50',
  },
  scoreText: {
    fontSize: 12,
    fontWeight: '600',
    color: '#4CAF50',
    marginLeft: 10,
  },
  resultsSection: {
    padding: 20,
  },
  lessonCard: {
    backgroundColor: '#fff',
    padding: 15,
    borderRadius: 10,
    marginBottom: 15,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  lessonHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 10,
  },
  lessonSubject: {
    fontSize: 14,
    fontWeight: '600',
    color: '#3498db',
  },
  lessonDifficulty: {
    fontSize: 12,
    color: '#666',
    backgroundColor: '#f0f0f0',
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 4,
  },
  lessonTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 5,
  },
  lessonDescription: {
    fontSize: 14,
    color: '#666',
    marginBottom: 10,
  },
  lessonMeta: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    marginBottom: 10,
  },
  metaText: {
    fontSize: 12,
    color: '#999',
    marginRight: 15,
  },
  tags: {
    flexDirection: 'row',
    flexWrap: 'wrap',
  },
  tag: {
    backgroundColor: '#e3f2fd',
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 4,
    marginRight: 5,
    marginTop: 5,
  },
  tagText: {
    fontSize: 11,
    color: '#1976d2',
  },
});
