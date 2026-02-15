import React, { useState, useContext, useEffect } from 'react';
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  FlatList,
  StyleSheet,
  Alert,
  ActivityIndicator,
  Modal
} from 'react-native';
import { UserContext } from '../UserContext';
import { searchQuestions } from '../api';

const SUBJECTS = [
  'All Subjects',
  'Mathematics',
  'Physics',
  'Chemistry',
  'Biology',
  'English Language',
  'Use of English',
  'Geography',
  'History',
  'Economics',
  'Commerce',
  'Accounting',
  'Literature in English',
  'Government',
  'Christian Religious Studies',
  'Islamic Religious Studies'
];

const EXAM_BOARDS = ['All Boards', 'WAEC', 'NECO', 'JAMB'];
const DIFFICULTIES = ['All Difficulties', 'easy', 'medium', 'hard'];

export default function SearchScreen({ navigation }) {
  const { token } = useContext(UserContext);
  const [searchQuery, setSearchQuery] = useState('');
  const [filters, setFilters] = useState({
    exam_board: 'All Boards',
    subject: 'All Subjects',
    difficulty: 'All Difficulties',
    year: '',
    topic: ''
  });
  const [questions, setQuestions] = useState([]);
  const [loading, setLoading] = useState(false);
  const [hasSearched, setHasSearched] = useState(false);
  const [showExamBoardPicker, setShowExamBoardPicker] = useState(false);
  const [showSubjectPicker, setShowSubjectPicker] = useState(false);
  const [showDifficultyPicker, setShowDifficultyPicker] = useState(false);

  const updateFilter = (key, value) => {
    setFilters(prev => ({ ...prev, [key]: value }));
  };

  const performSearch = async () => {
    setLoading(true);
    try {
      const searchParams = {
        q: searchQuery,
        limit: 50
      };

      if (filters.exam_board !== 'All Boards') {
        searchParams.exam_board = filters.exam_board;
      }
      if (filters.subject !== 'All Subjects') {
        searchParams.subject = filters.subject;
      }
      if (filters.difficulty !== 'All Difficulties') {
        searchParams.difficulty = filters.difficulty;
      }
      if (filters.year) {
        searchParams.year = parseInt(filters.year);
      }
      if (filters.topic) {
        searchParams.topic = filters.topic;
      }

      const result = await searchQuestions(searchParams, token);
      setQuestions(result.questions || []);
      setHasSearched(true);
    } catch (error) {
      Alert.alert('Search Failed', error.message);
      setQuestions([]);
    } finally {
      setLoading(false);
    }
  };

  const clearFilters = () => {
    setFilters({
      exam_board: 'All Boards',
      subject: 'All Subjects',
      difficulty: 'All Difficulties',
      year: '',
      topic: ''
    });
    setSearchQuery('');
    setQuestions([]);
    setHasSearched(false);
  };

  const renderQuestionItem = ({ item }) => (
    <TouchableOpacity
      style={styles.questionItem}
      onPress={() => navigation.navigate('Quiz', {
        questions: [item],
        mode: 'single'
      })}
    >
      <View style={styles.questionHeader}>
        <Text style={styles.questionId}>{item.id}</Text>
        <View style={[styles.difficultyBadge, { backgroundColor: getDifficultyColor(item.difficulty) }]}>
          <Text style={styles.difficultyText}>{item.difficulty}</Text>
        </View>
      </View>
      <Text style={styles.questionText} numberOfLines={2}>
        {item.question_text}
      </Text>
      <View style={styles.questionMeta}>
        <Text style={styles.metaText}>{item.exam_board} • {item.subject}</Text>
        <Text style={styles.metaText}>{item.year} • {item.topic}</Text>
      </View>
    </TouchableOpacity>
  );

  const getDifficultyColor = (difficulty) => {
    switch (difficulty) {
      case 'easy': return '#27ae60';
      case 'medium': return '#f39c12';
      case 'hard': return '#e74c3c';
      default: return '#95a5a6';
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Search Questions</Text>

      <TextInput
        style={styles.searchInput}
        placeholder="Search by keyword (e.g., quadratic equation)"
        value={searchQuery}
        onChangeText={setSearchQuery}
      />

      <View style={styles.filtersContainer}>
        <View style={styles.filterRow}>
          <View style={styles.filterItem}>
            <Text style={styles.filterLabel}>Exam Board</Text>
            <TouchableOpacity
              style={styles.pickerContainer}
              onPress={() => setShowExamBoardPicker(true)}
            >
              <Text style={styles.pickerText}>{filters.exam_board}</Text>
            </TouchableOpacity>
          </View>

          <View style={styles.filterItem}>
            <Text style={styles.filterLabel}>Subject</Text>
            <TouchableOpacity
              style={styles.pickerContainer}
              onPress={() => setShowSubjectPicker(true)}
            >
              <Text style={styles.pickerText}>{filters.subject}</Text>
            </TouchableOpacity>
          </View>
        </View>

        <View style={styles.filterRow}>
          <View style={styles.filterItem}>
            <Text style={styles.filterLabel}>Difficulty</Text>
            <TouchableOpacity
              style={styles.pickerContainer}
              onPress={() => setShowDifficultyPicker(true)}
            >
              <Text style={styles.pickerText}>{filters.difficulty}</Text>
            </TouchableOpacity>
          </View>

          <View style={styles.filterItem}>
            <Text style={styles.filterLabel}>Year</Text>
            <TextInput
              style={styles.yearInput}
              placeholder="e.g., 2020"
              value={filters.year}
              onChangeText={(value) => updateFilter('year', value)}
              keyboardType="numeric"
              maxLength={4}
            />
          </View>
        </View>

        <TextInput
          style={styles.topicInput}
          placeholder="Specific topic (optional)"
          value={filters.topic}
          onChangeText={(value) => updateFilter('topic', value)}
        />
      </View>

      <View style={styles.buttonRow}>
        <TouchableOpacity
          style={[styles.button, styles.searchButton]}
          onPress={performSearch}
          disabled={loading}
        >
          {loading ? (
            <ActivityIndicator color="#fff" size="small" />
          ) : (
            <Text style={styles.buttonText}>Search</Text>
          )}
        </TouchableOpacity>

        <TouchableOpacity
          style={[styles.button, styles.clearButton]}
          onPress={clearFilters}
        >
          <Text style={styles.clearButtonText}>Clear</Text>
        </TouchableOpacity>
      </View>

      {hasSearched && (
        <Text style={styles.resultsText}>
          {questions.length} questions found
        </Text>
      )}

      <FlatList
        data={questions}
        renderItem={renderQuestionItem}
        keyExtractor={(item) => item.id}
        style={styles.questionsList}
        showsVerticalScrollIndicator={false}
      />

      {/* Modals for dropdowns */}
      <Modal visible={showExamBoardPicker} transparent animationType="slide">
        <View style={styles.modalOverlay}>
          <View style={styles.modalContent}>
            <Text style={styles.modalTitle}>Select Exam Board</Text>
            {EXAM_BOARDS.map(board => (
              <TouchableOpacity
                key={board}
                style={styles.modalOption}
                onPress={() => {
                  updateFilter('exam_board', board);
                  setShowExamBoardPicker(false);
                }}
              >
                <Text style={[
                  styles.modalOptionText,
                  filters.exam_board === board && styles.modalOptionSelected
                ]}>
                  {board}
                </Text>
              </TouchableOpacity>
            ))}
            <TouchableOpacity
              style={styles.modalClose}
              onPress={() => setShowExamBoardPicker(false)}
            >
              <Text style={styles.modalCloseText}>Cancel</Text>
            </TouchableOpacity>
          </View>
        </View>
      </Modal>

      <Modal visible={showSubjectPicker} transparent animationType="slide">
        <View style={styles.modalOverlay}>
          <View style={styles.modalContent}>
            <Text style={styles.modalTitle}>Select Subject</Text>
            {SUBJECTS.map(subject => (
              <TouchableOpacity
                key={subject}
                style={styles.modalOption}
                onPress={() => {
                  updateFilter('subject', subject);
                  setShowSubjectPicker(false);
                }}
              >
                <Text style={[
                  styles.modalOptionText,
                  filters.subject === subject && styles.modalOptionSelected
                ]}>
                  {subject}
                </Text>
              </TouchableOpacity>
            ))}
            <TouchableOpacity
              style={styles.modalClose}
              onPress={() => setShowSubjectPicker(false)}
            >
              <Text style={styles.modalCloseText}>Cancel</Text>
            </TouchableOpacity>
          </View>
        </View>
      </Modal>

      <Modal visible={showDifficultyPicker} transparent animationType="slide">
        <View style={styles.modalOverlay}>
          <View style={styles.modalContent}>
            <Text style={styles.modalTitle}>Select Difficulty</Text>
            {DIFFICULTIES.map(diff => (
              <TouchableOpacity
                key={diff}
                style={styles.modalOption}
                onPress={() => {
                  updateFilter('difficulty', diff);
                  setShowDifficultyPicker(false);
                }}
              >
                <Text style={[
                  styles.modalOptionText,
                  filters.difficulty === diff && styles.modalOptionSelected
                ]}>
                  {diff}
                </Text>
              </TouchableOpacity>
            ))}
            <TouchableOpacity
              style={styles.modalClose}
              onPress={() => setShowDifficultyPicker(false)}
            >
              <Text style={styles.modalCloseText}>Cancel</Text>
            </TouchableOpacity>
          </View>
        </View>
      </Modal>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 15,
    backgroundColor: '#fff',
  },
  title: {
    fontSize: 20,
    fontWeight: 'bold',
    marginBottom: 15,
    color: '#333',
  },
  searchInput: {
    borderWidth: 1,
    borderColor: '#ddd',
    padding: 12,
    borderRadius: 8,
    fontSize: 16,
    marginBottom: 15,
  },
  filtersContainer: {
    marginBottom: 15,
  },
  filterRow: {
    flexDirection: 'row',
    marginBottom: 10,
  },
  filterItem: {
    flex: 1,
    marginHorizontal: 5,
  },
  filterLabel: {
    fontSize: 14,
    fontWeight: '600',
    marginBottom: 5,
    color: '#333',
  },
  pickerContainer: {
    borderWidth: 1,
    borderColor: '#ddd',
    borderRadius: 6,
    padding: 10,
    backgroundColor: '#fff',
  },
  pickerText: {
    fontSize: 16,
    color: '#333',
  },
  modalOverlay: {
    flex: 1,
    backgroundColor: 'rgba(0,0,0,0.5)',
    justifyContent: 'center',
    alignItems: 'center',
  },
  modalContent: {
    backgroundColor: '#fff',
    borderRadius: 12,
    padding: 20,
    width: '80%',
    maxHeight: '60%',
  },
  modalTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 20,
    textAlign: 'center',
    color: '#333',
  },
  modalOption: {
    padding: 15,
    borderBottomWidth: 1,
    borderBottomColor: '#f0f0f0',
  },
  modalOptionText: {
    fontSize: 16,
    color: '#333',
  },
  modalOptionSelected: {
    color: '#3498db',
    fontWeight: 'bold',
  },
  modalClose: {
    marginTop: 20,
    padding: 15,
    alignItems: 'center',
  },
  modalCloseText: {
    color: '#666',
    fontSize: 16,
  },
  yearInput: {
    borderWidth: 1,
    borderColor: '#ddd',
    padding: 10,
    borderRadius: 6,
    fontSize: 16,
  },
  topicInput: {
    borderWidth: 1,
    borderColor: '#ddd',
    padding: 10,
    borderRadius: 6,
    fontSize: 16,
    marginTop: 10,
  },
  buttonRow: {
    flexDirection: 'row',
    marginBottom: 15,
  },
  button: {
    flex: 1,
    padding: 12,
    borderRadius: 6,
    alignItems: 'center',
    marginHorizontal: 5,
  },
  searchButton: {
    backgroundColor: '#3498db',
  },
  clearButton: {
    backgroundColor: '#ecf0f1',
    borderWidth: 1,
    borderColor: '#bdc3c7',
  },
  buttonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
  },
  clearButtonText: {
    color: '#7f8c8d',
    fontSize: 16,
    fontWeight: '600',
  },
  resultsText: {
    fontSize: 14,
    color: '#666',
    marginBottom: 10,
  },
  questionsList: {
    flex: 1,
  },
  questionItem: {
    backgroundColor: '#f9f9f9',
    padding: 15,
    marginBottom: 10,
    borderRadius: 8,
    borderLeftWidth: 4,
    borderLeftColor: '#3498db',
  },
  questionHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 8,
  },
  questionId: {
    fontSize: 12,
    color: '#666',
    fontWeight: '600',
  },
  difficultyBadge: {
    paddingHorizontal: 8,
    paddingVertical: 2,
    borderRadius: 10,
  },
  difficultyText: {
    color: '#fff',
    fontSize: 10,
    fontWeight: 'bold',
    textTransform: 'uppercase',
  },
  questionText: {
    fontSize: 16,
    color: '#333',
    lineHeight: 22,
    marginBottom: 8,
  },
  questionMeta: {
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  metaText: {
    fontSize: 12,
    color: '#666',
  },
});