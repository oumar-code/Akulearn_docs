import React, { useState, useEffect, useContext } from 'react';
import {
  View,
  Text,
  TouchableOpacity,
  FlatList,
  StyleSheet,
  SafeAreaView,
  ActivityIndicator,
  Alert
} from 'react-native';
import { UserContext } from '../UserContext';
import { getSubjects, getTopicsBySubject, getContentByTopic } from '../api';

export default function LearnScreen({ navigation }) {
  const { token } = useContext(UserContext);
  const [subjects, setSubjects] = useState([]);
  const [selectedSubject, setSelectedSubject] = useState(null);
  const [topics, setTopics] = useState([]);
  const [selectedTopic, setSelectedTopic] = useState(null);
  const [content, setContent] = useState([]);
  const [loading, setLoading] = useState(true);
  const [currentView, setCurrentView] = useState('subjects'); // 'subjects', 'topics', 'content'

  useEffect(() => {
    loadSubjects();
  }, []);

  const loadSubjects = async () => {
    try {
      const result = await getSubjects();
      setSubjects(result.subjects);
    } catch (error) {
      Alert.alert('Error', 'Failed to load subjects');
    } finally {
      setLoading(false);
    }
  };

  const selectSubject = async (subject) => {
    setSelectedSubject(subject);
    setLoading(true);
    try {
      const result = await getTopicsBySubject(subject);
      setTopics(result.topics);
      setCurrentView('topics');
    } catch (error) {
      Alert.alert('Error', 'Failed to load topics');
    } finally {
      setLoading(false);
    }
  };

  const selectTopic = async (topic) => {
    setSelectedTopic(topic);
    setLoading(true);
    try {
      const result = await getContentByTopic(selectedSubject, topic);
      setContent(result.content);
      setCurrentView('content');
    } catch (error) {
      Alert.alert('Error', 'Failed to load content');
    } finally {
      setLoading(false);
    }
  };

  const goBack = () => {
    if (currentView === 'content') {
      setCurrentView('topics');
      setSelectedTopic(null);
      setContent([]);
    } else if (currentView === 'topics') {
      setCurrentView('subjects');
      setSelectedSubject(null);
      setTopics([]);
    }
  };

  const renderSubjectItem = ({ item }) => (
    <TouchableOpacity
      style={styles.subjectCard}
      onPress={() => selectSubject(item)}
    >
      <Text style={styles.subjectTitle}>{item}</Text>
      <Text style={styles.subjectSubtitle}>Tap to explore topics</Text>
    </TouchableOpacity>
  );

  const renderTopicItem = ({ item }) => (
    <TouchableOpacity
      style={styles.topicCard}
      onPress={() => selectTopic(item)}
    >
      <Text style={styles.topicTitle}>{item}</Text>
      <Text style={styles.topicSubtitle}>View learning materials</Text>
    </TouchableOpacity>
  );

  const renderContentItem = ({ item }) => (
    <TouchableOpacity
      style={styles.contentCard}
      onPress={() => navigation.navigate('ContentReader', { contentId: item.id })}
    >
      <View style={styles.contentHeader}>
        <Text style={styles.contentTitle}>{item.title}</Text>
        <View style={[styles.difficultyBadge, { backgroundColor: getDifficultyColor(item.difficulty) }]}>
          <Text style={styles.difficultyText}>{item.difficulty}</Text>
        </View>
      </View>
      <Text style={styles.contentType}>{item.content_type.replace('_', ' ').toUpperCase()}</Text>
      <Text style={styles.contentMeta}>
        {item.estimated_read_time} min read • {item.tags.slice(0, 3).join(', ')}
      </Text>
    </TouchableOpacity>
  );

  const getDifficultyColor = (difficulty) => {
    switch (difficulty) {
      case 'basic': return '#27ae60';
      case 'intermediate': return '#f39c12';
      case 'advanced': return '#e74c3c';
      default: return '#95a5a6';
    }
  };

  if (loading) {
    return (
      <SafeAreaView style={styles.container}>
        <View style={styles.loadingContainer}>
          <ActivityIndicator size="large" color="#3498db" />
          <Text style={styles.loadingText}>Loading...</Text>
        </View>
      </SafeAreaView>
    );
  }

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        {currentView !== 'subjects' && (
          <TouchableOpacity style={styles.backButton} onPress={goBack}>
            <Text style={styles.backButtonText}>← Back</Text>
          </TouchableOpacity>
        )}
        <Text style={styles.headerTitle}>
          {currentView === 'subjects' && 'Subjects'}
          {currentView === 'topics' && selectedSubject}
          {currentView === 'content' && selectedTopic}
        </Text>
      </View>

      {currentView === 'subjects' && (
        <FlatList
          data={subjects}
          renderItem={renderSubjectItem}
          keyExtractor={(item) => item}
          style={styles.list}
          showsVerticalScrollIndicator={false}
        />
      )}

      {currentView === 'topics' && (
        <FlatList
          data={topics}
          renderItem={renderTopicItem}
          keyExtractor={(item) => item}
          style={styles.list}
          showsVerticalScrollIndicator={false}
        />
      )}

      {currentView === 'content' && (
        <FlatList
          data={content}
          renderItem={renderContentItem}
          keyExtractor={(item) => item.id}
          style={styles.list}
          showsVerticalScrollIndicator={false}
          ListEmptyComponent={
            <View style={styles.emptyContainer}>
              <Text style={styles.emptyText}>No content available for this topic yet.</Text>
              <Text style={styles.emptySubtext}>Check back soon for new materials!</Text>
            </View>
          }
        />
      )}
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
    fontSize: 16,
    color: '#666',
    marginTop: 10,
  },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    padding: 15,
    backgroundColor: '#fff',
    borderBottomWidth: 1,
    borderBottomColor: '#e0e0e0',
  },
  backButton: {
    marginRight: 15,
  },
  backButtonText: {
    fontSize: 16,
    color: '#3498db',
    fontWeight: '600',
  },
  headerTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#333',
    flex: 1,
  },
  list: {
    flex: 1,
    padding: 15,
  },
  subjectCard: {
    backgroundColor: '#fff',
    borderRadius: 12,
    padding: 20,
    marginBottom: 15,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  subjectTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 5,
  },
  subjectSubtitle: {
    fontSize: 14,
    color: '#666',
  },
  topicCard: {
    backgroundColor: '#fff',
    borderRadius: 12,
    padding: 20,
    marginBottom: 10,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  topicTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: '#333',
    marginBottom: 5,
  },
  topicSubtitle: {
    fontSize: 14,
    color: '#666',
  },
  contentCard: {
    backgroundColor: '#fff',
    borderRadius: 12,
    padding: 15,
    marginBottom: 10,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  contentHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    marginBottom: 8,
  },
  contentTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: '#333',
    flex: 1,
    marginRight: 10,
  },
  difficultyBadge: {
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 12,
  },
  difficultyText: {
    color: '#fff',
    fontSize: 12,
    fontWeight: 'bold',
    textTransform: 'capitalize',
  },
  contentType: {
    fontSize: 12,
    color: '#666',
    fontWeight: '600',
    textTransform: 'uppercase',
    marginBottom: 5,
  },
  contentMeta: {
    fontSize: 12,
    color: '#666',
  },
  emptyContainer: {
    alignItems: 'center',
    padding: 40,
  },
  emptyText: {
    fontSize: 16,
    color: '#666',
    textAlign: 'center',
    marginBottom: 10,
  },
  emptySubtext: {
    fontSize: 14,
    color: '#999',
    textAlign: 'center',
  },
});