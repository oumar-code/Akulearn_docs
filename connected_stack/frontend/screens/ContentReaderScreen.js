import React, { useState, useEffect, useContext } from 'react';
import {
  View,
  Text,
  ScrollView,
  StyleSheet,
  SafeAreaView,
  TouchableOpacity,
  ActivityIndicator,
  Alert,
  Dimensions
} from 'react-native';
import { UserContext } from '../UserContext';
import { getContentById, updateContentProgress } from '../api';

const { width, height } = Dimensions.get('window');

export default function ContentReaderScreen({ route, navigation }) {
  const { contentId } = route.params;
  const { token, user } = useContext(UserContext);
  const [content, setContent] = useState(null);
  const [loading, setLoading] = useState(true);
  const [progress, setProgress] = useState(0);
  const [startTime, setStartTime] = useState(null);
  const [isCompleted, setIsCompleted] = useState(false);

  useEffect(() => {
    loadContent();
    setStartTime(new Date());
  }, []);

  const loadContent = async () => {
    try {
      const result = await getContentById(contentId);
      setContent(result.content);
      setIsCompleted(result.progress?.completed || false);
    } catch (error) {
      Alert.alert('Error', 'Failed to load content');
      navigation.goBack();
    } finally {
      setLoading(false);
    }
  };

  const handleScroll = (event) => {
    const { contentOffset, contentSize, layoutMeasurement } = event.nativeEvent;
    const scrollProgress = contentOffset.y / (contentSize.height - layoutMeasurement.height);
    const clampedProgress = Math.max(0, Math.min(1, scrollProgress));
    setProgress(clampedProgress);

    // Mark as completed when user reaches 80% of content
    if (clampedProgress >= 0.8 && !isCompleted) {
      markAsCompleted();
    }
  };

  const markAsCompleted = async () => {
    try {
      const timeSpent = Math.floor((new Date() - startTime) / 1000); // seconds
      await updateContentProgress(contentId, {
        completed: true,
        time_spent: timeSpent,
        last_read_at: new Date().toISOString()
      });
      setIsCompleted(true);
    } catch (error) {
      console.error('Failed to update progress:', error);
    }
  };

  const renderContentSection = (section, index) => {
    switch (section.type) {
      case 'heading':
        return (
          <Text key={index} style={styles.heading}>
            {section.content}
          </Text>
        );
      case 'paragraph':
        return (
          <Text key={index} style={styles.paragraph}>
            {section.content}
          </Text>
        );
      case 'list':
        return (
          <View key={index} style={styles.list}>
            {section.items.map((item, itemIndex) => (
              <Text key={itemIndex} style={styles.listItem}>
                • {item}
              </Text>
            ))}
          </View>
        );
      case 'code':
        return (
          <View key={index} style={styles.codeBlock}>
            <Text style={styles.codeText}>{section.content}</Text>
          </View>
        );
      case 'quote':
        return (
          <View key={index} style={styles.quote}>
            <Text style={styles.quoteText}>"{section.content}"</Text>
          </View>
        );
      default:
        return (
          <Text key={index} style={styles.paragraph}>
            {section.content}
          </Text>
        );
    }
  };

  if (loading) {
    return (
      <SafeAreaView style={styles.container}>
        <View style={styles.loadingContainer}>
          <ActivityIndicator size="large" color="#3498db" />
          <Text style={styles.loadingText}>Loading content...</Text>
        </View>
      </SafeAreaView>
    );
  }

  if (!content) {
    return (
      <SafeAreaView style={styles.container}>
        <View style={styles.errorContainer}>
          <Text style={styles.errorText}>Content not found</Text>
          <TouchableOpacity
            style={styles.backButton}
            onPress={() => navigation.goBack()}
          >
            <Text style={styles.backButtonText}>Go Back</Text>
          </TouchableOpacity>
        </View>
      </SafeAreaView>
    );
  }

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <TouchableOpacity
          style={styles.backButton}
          onPress={() => navigation.goBack()}
        >
          <Text style={styles.backButtonText}>← Back</Text>
        </TouchableOpacity>
        <View style={styles.headerContent}>
          <Text style={styles.title} numberOfLines={1}>
            {content.title}
          </Text>
          <View style={styles.meta}>
            <Text style={styles.metaText}>
              {content.subject} • {content.topic}
            </Text>
            <Text style={styles.metaText}>
              {content.estimated_read_time} min read
            </Text>
          </View>
        </View>
        {isCompleted && (
          <View style={styles.completedBadge}>
            <Text style={styles.completedText}>✓</Text>
          </View>
        )}
      </View>

      <View style={styles.progressBar}>
        <View
          style={[
            styles.progressFill,
            { width: `${progress * 100}%` }
          ]}
        />
      </View>

      <ScrollView
        style={styles.scrollView}
        onScroll={handleScroll}
        scrollEventThrottle={16}
        showsVerticalScrollIndicator={false}
      >
        <View style={styles.contentContainer}>
          {content.sections.map((section, index) =>
            renderContentSection(section, index)
          )}
        </View>

        <View style={styles.footer}>
          <Text style={styles.footerText}>
            Content Type: {content.content_type.replace('_', ' ').toUpperCase()}
          </Text>
          <Text style={styles.footerText}>
            Difficulty: {content.difficulty.charAt(0).toUpperCase() + content.difficulty.slice(1)}
          </Text>
          {content.tags.length > 0 && (
            <Text style={styles.footerText}>
              Tags: {content.tags.join(', ')}
            </Text>
          )}
        </View>
      </ScrollView>
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
  errorContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 20,
  },
  errorText: {
    fontSize: 18,
    color: '#666',
    marginBottom: 20,
  },
  backButton: {
    padding: 10,
  },
  backButtonText: {
    fontSize: 16,
    color: '#3498db',
    fontWeight: '600',
  },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    padding: 15,
    backgroundColor: '#fff',
    borderBottomWidth: 1,
    borderBottomColor: '#e0e0e0',
  },
  headerContent: {
    flex: 1,
    marginLeft: 10,
  },
  title: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 5,
  },
  meta: {
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  metaText: {
    fontSize: 12,
    color: '#666',
  },
  completedBadge: {
    width: 30,
    height: 30,
    borderRadius: 15,
    backgroundColor: '#27ae60',
    justifyContent: 'center',
    alignItems: 'center',
    marginLeft: 10,
  },
  completedText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: 'bold',
  },
  progressBar: {
    height: 4,
    backgroundColor: '#e0e0e0',
  },
  progressFill: {
    height: '100%',
    backgroundColor: '#3498db',
  },
  scrollView: {
    flex: 1,
  },
  contentContainer: {
    padding: 20,
    backgroundColor: '#fff',
    margin: 15,
    borderRadius: 12,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  heading: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 15,
    marginTop: 10,
  },
  paragraph: {
    fontSize: 16,
    lineHeight: 24,
    color: '#333',
    marginBottom: 15,
  },
  list: {
    marginBottom: 15,
    marginLeft: 10,
  },
  listItem: {
    fontSize: 16,
    lineHeight: 24,
    color: '#333',
    marginBottom: 5,
  },
  codeBlock: {
    backgroundColor: '#f8f8f8',
    borderRadius: 8,
    padding: 15,
    marginBottom: 15,
    borderLeftWidth: 4,
    borderLeftColor: '#3498db',
  },
  codeText: {
    fontFamily: 'monospace',
    fontSize: 14,
    color: '#333',
  },
  quote: {
    borderLeftWidth: 4,
    borderLeftColor: '#f39c12',
    paddingLeft: 15,
    marginBottom: 15,
    backgroundColor: '#fff9e6',
    paddingVertical: 10,
  },
  quoteText: {
    fontSize: 16,
    fontStyle: 'italic',
    color: '#333',
    lineHeight: 24,
  },
  footer: {
    padding: 20,
    backgroundColor: '#f9f9f9',
    marginHorizontal: 15,
    marginBottom: 15,
    borderRadius: 12,
  },
  footerText: {
    fontSize: 12,
    color: '#666',
    marginBottom: 5,
  },
});