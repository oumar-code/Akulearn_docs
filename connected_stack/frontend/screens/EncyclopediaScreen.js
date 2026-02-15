import React, { useState, useEffect, useContext } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  TextInput,
  FlatList,
  Alert,
  ActivityIndicator,
  Dimensions,
} from 'react-native';
import { UserContext } from '../UserContext';
import {
  getEncyclopediaSubjects,
  searchEncyclopedia,
  getEncyclopediaEntry,
  getSubjectEntries
} from '../api';

const { width, height } = Dimensions.get('window');

const EncyclopediaScreen = ({ navigation }) => {
  const { user } = useContext(UserContext);
  const [subjects, setSubjects] = useState([]);
  const [selectedSubject, setSelectedSubject] = useState(null);
  const [entries, setEntries] = useState([]);
  const [selectedEntry, setSelectedEntry] = useState(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState('subjects');

  useEffect(() => {
    loadSubjects();
  }, []);

  const loadSubjects = async () => {
    try {
      const subjectData = await getEncyclopediaSubjects(user?.token);
      setSubjects(subjectData);
    } catch (error) {
      Alert.alert('Error', 'Failed to load encyclopedia subjects');
    }
  };

  const loadSubjectEntries = async (subject) => {
    setLoading(true);
    try {
      const entryData = await getSubjectEntries(subject.id, user?.token);
      setEntries(entryData);
      setSelectedSubject(subject);
      setActiveTab('entries');
    } catch (error) {
      Alert.alert('Error', 'Failed to load subject entries');
    } finally {
      setLoading(false);
    }
  };

  const loadEntryDetails = async (entry) => {
    setLoading(true);
    try {
      const entryDetails = await getEncyclopediaEntry(entry.id, user?.token);
      setSelectedEntry(entryDetails);
      setActiveTab('entry');
    } catch (error) {
      Alert.alert('Error', 'Failed to load entry details');
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = async () => {
    if (!searchQuery.trim()) {
      Alert.alert('Error', 'Please enter a search term');
      return;
    }

    setLoading(true);
    try {
      const results = await searchEncyclopedia(searchQuery, user?.token);
      setSearchResults(results);
      setActiveTab('search');
    } catch (error) {
      Alert.alert('Error', 'Search failed');
    } finally {
      setLoading(false);
    }
  };

  const renderSubjects = () => (
    <ScrollView style={styles.container}>
      <Text style={styles.title}>Encyclopedia</Text>
      <Text style={styles.subtitle}>Explore knowledge across subjects</Text>

      {/* Search Bar */}
      <View style={styles.searchContainer}>
        <TextInput
          style={styles.searchInput}
          placeholder="Search encyclopedia..."
          value={searchQuery}
          onChangeText={setSearchQuery}
          onSubmitEditing={handleSearch}
        />
        <TouchableOpacity style={styles.searchButton} onPress={handleSearch}>
          <Text style={styles.searchButtonText}>Search</Text>
        </TouchableOpacity>
      </View>

      {/* Subject Grid */}
      <View style={styles.subjectsGrid}>
        {subjects.map((subject, index) => (
          <TouchableOpacity
            key={index}
            style={styles.subjectCard}
            onPress={() => loadSubjectEntries(subject)}
          >
            <Text style={styles.subjectIcon}>{subject.icon || '📚'}</Text>
            <Text style={styles.subjectTitle}>{subject.name}</Text>
            <Text style={styles.subjectCount}>{subject.entry_count} entries</Text>
          </TouchableOpacity>
        ))}
      </View>
    </ScrollView>
  );

  const renderEntries = () => (
    <ScrollView style={styles.container}>
      <View style={styles.header}>
        <TouchableOpacity
          style={styles.backButton}
          onPress={() => setActiveTab('subjects')}
        >
          <Text style={styles.backButtonText}>← Back to Subjects</Text>
        </TouchableOpacity>
        <Text style={styles.sectionTitle}>{selectedSubject?.name} Entries</Text>
      </View>

      {loading ? (
        <ActivityIndicator size="large" color="#3498db" style={styles.loader} />
      ) : (
        <View style={styles.entriesList}>
          {entries.map((entry, index) => (
            <TouchableOpacity
              key={index}
              style={styles.entryCard}
              onPress={() => loadEntryDetails(entry)}
            >
              <Text style={styles.entryTitle}>{entry.title}</Text>
              <Text style={styles.entrySummary} numberOfLines={2}>
                {entry.summary}
              </Text>
              <View style={styles.entryMeta}>
                <Text style={styles.entryCategory}>{entry.category}</Text>
                <Text style={styles.entryDate}>{entry.last_updated}</Text>
              </View>
            </TouchableOpacity>
          ))}
        </View>
      )}
    </ScrollView>
  );

  const renderEntry = () => (
    <ScrollView style={styles.container}>
      <View style={styles.header}>
        <TouchableOpacity
          style={styles.backButton}
          onPress={() => setActiveTab('entries')}
        >
          <Text style={styles.backButtonText}>← Back to Entries</Text>
        </TouchableOpacity>
        <Text style={styles.sectionTitle}>{selectedEntry?.title}</Text>
      </View>

      {loading ? (
        <ActivityIndicator size="large" color="#3498db" style={styles.loader} />
      ) : selectedEntry ? (
        <View style={styles.entryContainer}>
          <View style={styles.entryHeader}>
            <Text style={styles.entryCategoryTag}>{selectedEntry.category}</Text>
            <Text style={styles.entryDate}>{selectedEntry.last_updated}</Text>
          </View>

          <Text style={styles.entrySummary}>{selectedEntry.summary}</Text>

          <Text style={styles.sectionTitle}>Content</Text>
          <Text style={styles.entryContent}>{selectedEntry.content}</Text>

          {selectedEntry.references && selectedEntry.references.length > 0 && (
            <View>
              <Text style={styles.sectionTitle}>References</Text>
              {selectedEntry.references.map((ref, index) => (
                <Text key={index} style={styles.reference}>
                  {index + 1}. {ref}
                </Text>
              ))}
            </View>
          )}

          {selectedEntry.related_entries && selectedEntry.related_entries.length > 0 && (
            <View>
              <Text style={styles.sectionTitle}>Related Entries</Text>
              <View style={styles.relatedEntries}>
                {selectedEntry.related_entries.map((related, index) => (
                  <TouchableOpacity
                    key={index}
                    style={styles.relatedEntryTag}
                    onPress={() => loadEntryDetails({ id: related.id })}
                  >
                    <Text style={styles.relatedEntryText}>{related.title}</Text>
                  </TouchableOpacity>
                ))}
              </View>
            </View>
          )}
        </View>
      ) : (
        <Text style={styles.noDataText}>Entry not found</Text>
      )}
    </ScrollView>
  );

  const renderSearch = () => (
    <ScrollView style={styles.container}>
      <View style={styles.header}>
        <TouchableOpacity
          style={styles.backButton}
          onPress={() => setActiveTab('subjects')}
        >
          <Text style={styles.backButtonText}>← Back to Subjects</Text>
        </TouchableOpacity>
        <Text style={styles.sectionTitle}>Search Results</Text>
        <Text style={styles.searchQuery}>"{searchQuery}"</Text>
      </View>

      {loading ? (
        <ActivityIndicator size="large" color="#3498db" style={styles.loader} />
      ) : searchResults.length > 0 ? (
        <View style={styles.entriesList}>
          {searchResults.map((result, index) => (
            <TouchableOpacity
              key={index}
              style={styles.entryCard}
              onPress={() => loadEntryDetails(result)}
            >
              <Text style={styles.entryTitle}>{result.title}</Text>
              <Text style={styles.entrySummary} numberOfLines={2}>
                {result.summary}
              </Text>
              <View style={styles.entryMeta}>
                <Text style={styles.entryCategory}>{result.category}</Text>
                <Text style={styles.entrySubject}>{result.subject}</Text>
              </View>
            </TouchableOpacity>
          ))}
        </View>
      ) : (
        <Text style={styles.noResultsText}>No results found for "{searchQuery}"</Text>
      )}
    </ScrollView>
  );

  const renderContent = () => {
    switch (activeTab) {
      case 'subjects':
        return renderSubjects();
      case 'entries':
        return renderEntries();
      case 'entry':
        return renderEntry();
      case 'search':
        return renderSearch();
      default:
        return renderSubjects();
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
  searchContainer: {
    flexDirection: 'row',
    marginBottom: 20,
  },
  searchInput: {
    flex: 1,
    height: 40,
    borderWidth: 1,
    borderColor: '#ddd',
    borderRadius: 8,
    paddingHorizontal: 12,
    backgroundColor: '#fff',
    marginRight: 8,
  },
  searchButton: {
    backgroundColor: '#3498db',
    paddingVertical: 10,
    paddingHorizontal: 16,
    borderRadius: 8,
    justifyContent: 'center',
  },
  searchButtonText: {
    color: '#fff',
    fontWeight: 'bold',
  },
  subjectsGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'space-between',
  },
  subjectCard: {
    backgroundColor: '#fff',
    borderRadius: 8,
    padding: 16,
    marginBottom: 12,
    width: '48%',
    alignItems: 'center',
    elevation: 2,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.1,
    shadowRadius: 2,
  },
  subjectIcon: {
    fontSize: 32,
    marginBottom: 8,
  },
  subjectTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#2c3e50',
    textAlign: 'center',
    marginBottom: 4,
  },
  subjectCount: {
    fontSize: 12,
    color: '#666',
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
  sectionTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#2c3e50',
  },
  searchQuery: {
    fontSize: 16,
    color: '#666',
    fontStyle: 'italic',
    marginTop: 4,
  },
  loader: {
    marginTop: 50,
  },
  entriesList: {
    paddingBottom: 20,
  },
  entryCard: {
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
  entryTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#2c3e50',
    marginBottom: 8,
  },
  entrySummary: {
    fontSize: 14,
    color: '#666',
    marginBottom: 8,
    lineHeight: 20,
  },
  entryMeta: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  entryCategory: {
    fontSize: 12,
    color: '#3498db',
    fontWeight: 'bold',
    backgroundColor: '#e8f4fd',
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 12,
  },
  entryDate: {
    fontSize: 12,
    color: '#95a5a6',
  },
  entrySubject: {
    fontSize: 12,
    color: '#27ae60',
    fontWeight: 'bold',
    backgroundColor: '#f0f9e8',
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 12,
  },
  entryContainer: {
    backgroundColor: '#fff',
    borderRadius: 8,
    padding: 16,
    elevation: 2,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.1,
    shadowRadius: 2,
  },
  entryHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 16,
  },
  entryCategoryTag: {
    fontSize: 12,
    color: '#3498db',
    fontWeight: 'bold',
    backgroundColor: '#e8f4fd',
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 16,
  },
  entryContent: {
    fontSize: 16,
    color: '#2c3e50',
    lineHeight: 24,
    marginBottom: 20,
  },
  reference: {
    fontSize: 14,
    color: '#666',
    marginBottom: 4,
    lineHeight: 20,
  },
  relatedEntries: {
    flexDirection: 'row',
    flexWrap: 'wrap',
  },
  relatedEntryTag: {
    backgroundColor: '#f8f9fa',
    borderRadius: 16,
    paddingHorizontal: 12,
    paddingVertical: 6,
    margin: 4,
  },
  relatedEntryText: {
    fontSize: 12,
    color: '#2c3e50',
  },
  noDataText: {
    fontSize: 16,
    color: '#666',
    textAlign: 'center',
    marginTop: 50,
  },
  noResultsText: {
    fontSize: 16,
    color: '#666',
    textAlign: 'center',
    marginTop: 50,
  },
});

export default EncyclopediaScreen;