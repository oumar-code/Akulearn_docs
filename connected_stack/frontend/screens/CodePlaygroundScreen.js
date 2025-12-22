import React, { useState, useEffect, useContext } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  TextInput,
  Alert,
  ActivityIndicator,
  Dimensions,
} from 'react-native';
import { UserContext } from '../UserContext';
import {
  getCodePlaygroundData,
  runCode,
  getCodingChallenges,
  submitCodingChallenge
} from '../api';

const { width, height } = Dimensions.get('window');

const CodePlaygroundScreen = ({ navigation }) => {
  const { user } = useContext(UserContext);
  const [playgroundData, setPlaygroundData] = useState(null);
  const [challenges, setChallenges] = useState([]);
  const [selectedLanguage, setSelectedLanguage] = useState('python');
  const [code, setCode] = useState('');
  const [output, setOutput] = useState('');
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState('playground');

  useEffect(() => {
    loadPlaygroundData();
    loadChallenges();
  }, []);

  const loadPlaygroundData = async () => {
    try {
      const data = await getCodePlaygroundData(user?.token);
      setPlaygroundData(data);
      // Set default code for Python
      if (data?.python?.examples?.basic_syntax) {
        setCode(data.python.examples.basic_syntax.code);
      }
    } catch (error) {
      Alert.alert('Error', 'Failed to load playground data');
    }
  };

  const loadChallenges = async () => {
    try {
      const challengeData = await getCodingChallenges(user?.token);
      setChallenges(challengeData);
    } catch (error) {
      Alert.alert('Error', 'Failed to load challenges');
    }
  };

  const handleRunCode = async () => {
    if (!code.trim()) {
      Alert.alert('Error', 'Please enter some code to run');
      return;
    }

    setLoading(true);
    try {
      const result = await runCode(code, selectedLanguage, user?.token);
      setOutput(result.output || 'Code executed successfully');
    } catch (error) {
      setOutput(`Error: ${error.message}`);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmitChallenge = async (challengeId, solution) => {
    try {
      const result = await submitCodingChallenge(challengeId, solution, user?.token);
      Alert.alert('Success', `Challenge submitted! Score: ${result.score}`);
    } catch (error) {
      Alert.alert('Error', 'Failed to submit challenge');
    }
  };

  const loadExample = (example) => {
    setCode(example.code);
    setSelectedLanguage(example.language || 'python');
  };

  const renderPlayground = () => (
    <ScrollView style={styles.container}>
      <Text style={styles.title}>Code Playground</Text>

      {/* Language Selector */}
      <View style={styles.languageSelector}>
        {['python', 'javascript'].map((lang) => (
          <TouchableOpacity
            key={lang}
            style={[
              styles.languageButton,
              selectedLanguage === lang && styles.activeLanguageButton
            ]}
            onPress={() => setSelectedLanguage(lang)}
          >
            <Text style={[
              styles.languageButtonText,
              selectedLanguage === lang && styles.activeLanguageButtonText
            ]}>
              {lang.charAt(0).toUpperCase() + lang.slice(1)}
            </Text>
          </TouchableOpacity>
        ))}
      </View>

      {/* Code Editor */}
      <TextInput
        style={styles.codeEditor}
        multiline
        placeholder="Enter your code here..."
        value={code}
        onChangeText={setCode}
        textAlignVertical="top"
      />

      {/* Run Button */}
      <TouchableOpacity
        style={[styles.runButton, loading && styles.disabledButton]}
        onPress={handleRunCode}
        disabled={loading}
      >
        {loading ? (
          <ActivityIndicator color="#fff" />
        ) : (
          <Text style={styles.runButtonText}>Run Code</Text>
        )}
      </TouchableOpacity>

      {/* Output */}
      <View style={styles.outputContainer}>
        <Text style={styles.outputLabel}>Output:</Text>
        <Text style={styles.outputText}>{output}</Text>
      </View>

      {/* Examples */}
      <Text style={styles.sectionTitle}>Examples</Text>
      {playgroundData && (
        <ScrollView horizontal showsHorizontalScrollIndicator={false} style={styles.examplesContainer}>
          {Object.entries(playgroundData[selectedLanguage]?.examples || {}).map(([key, example]) => (
            <TouchableOpacity
              key={key}
              style={styles.exampleCard}
              onPress={() => loadExample(example)}
            >
              <Text style={styles.exampleTitle}>{example.title}</Text>
              <Text style={styles.exampleDescription}>{example.description}</Text>
            </TouchableOpacity>
          ))}
        </ScrollView>
      )}
    </ScrollView>
  );

  const renderChallenges = () => (
    <ScrollView style={styles.container}>
      <Text style={styles.title}>Coding Challenges</Text>

      {challenges.map((challenge, index) => (
        <View key={challenge.id || index} style={styles.challengeCard}>
          <Text style={styles.challengeTitle}>{challenge.title}</Text>
          <Text style={styles.challengeDescription}>{challenge.description}</Text>
          <Text style={styles.challengeDifficulty}>Difficulty: {challenge.difficulty}</Text>

          <View style={styles.challengeActions}>
            <TouchableOpacity
              style={styles.challengeButton}
              onPress={() => navigation.navigate('ChallengeDetail', { challenge })}
            >
              <Text style={styles.challengeButtonText}>View Challenge</Text>
            </TouchableOpacity>

            <TouchableOpacity
              style={[styles.challengeButton, styles.solveButton]}
              onPress={() => {
                setCode(challenge.template || '');
                setSelectedLanguage(challenge.language || 'python');
                setActiveTab('playground');
              }}
            >
              <Text style={styles.solveButtonText}>Solve Now</Text>
            </TouchableOpacity>
          </View>
        </View>
      ))}
    </ScrollView>
  );

  return (
    <View style={styles.mainContainer}>
      {/* Tab Navigation */}
      <View style={styles.tabContainer}>
        <TouchableOpacity
          style={[styles.tab, activeTab === 'playground' && styles.activeTab]}
          onPress={() => setActiveTab('playground')}
        >
          <Text style={[styles.tabText, activeTab === 'playground' && styles.activeTabText]}>
            Playground
          </Text>
        </TouchableOpacity>

        <TouchableOpacity
          style={[styles.tab, activeTab === 'challenges' && styles.activeTab]}
          onPress={() => setActiveTab('challenges')}
        >
          <Text style={[styles.tabText, activeTab === 'challenges' && styles.activeTabText]}>
            Challenges
          </Text>
        </TouchableOpacity>
      </View>

      {/* Content */}
      {activeTab === 'playground' ? renderPlayground() : renderChallenges()}
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
    marginBottom: 20,
    textAlign: 'center',
  },
  tabContainer: {
    flexDirection: 'row',
    backgroundColor: '#fff',
    elevation: 2,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 2,
  },
  tab: {
    flex: 1,
    paddingVertical: 12,
    alignItems: 'center',
  },
  activeTab: {
    borderBottomWidth: 2,
    borderBottomColor: '#3498db',
  },
  tabText: {
    fontSize: 16,
    color: '#666',
  },
  activeTabText: {
    color: '#3498db',
    fontWeight: 'bold',
  },
  languageSelector: {
    flexDirection: 'row',
    marginBottom: 16,
  },
  languageButton: {
    flex: 1,
    paddingVertical: 8,
    paddingHorizontal: 16,
    marginHorizontal: 4,
    borderRadius: 8,
    backgroundColor: '#ecf0f1',
    alignItems: 'center',
  },
  activeLanguageButton: {
    backgroundColor: '#3498db',
  },
  languageButtonText: {
    fontSize: 14,
    color: '#666',
  },
  activeLanguageButtonText: {
    color: '#fff',
  },
  codeEditor: {
    height: 200,
    borderWidth: 1,
    borderColor: '#ddd',
    borderRadius: 8,
    padding: 12,
    fontFamily: 'monospace',
    fontSize: 14,
    backgroundColor: '#fff',
    marginBottom: 16,
  },
  runButton: {
    backgroundColor: '#27ae60',
    paddingVertical: 12,
    paddingHorizontal: 24,
    borderRadius: 8,
    alignItems: 'center',
    marginBottom: 16,
  },
  disabledButton: {
    backgroundColor: '#95a5a6',
  },
  runButtonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: 'bold',
  },
  outputContainer: {
    backgroundColor: '#2c3e50',
    borderRadius: 8,
    padding: 12,
    marginBottom: 20,
  },
  outputLabel: {
    color: '#ecf0f1',
    fontSize: 14,
    fontWeight: 'bold',
    marginBottom: 8,
  },
  outputText: {
    color: '#ecf0f1',
    fontFamily: 'monospace',
    fontSize: 12,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#2c3e50',
    marginBottom: 12,
  },
  examplesContainer: {
    marginBottom: 20,
  },
  exampleCard: {
    backgroundColor: '#fff',
    borderRadius: 8,
    padding: 12,
    marginRight: 12,
    width: 200,
    elevation: 2,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.1,
    shadowRadius: 2,
  },
  exampleTitle: {
    fontSize: 14,
    fontWeight: 'bold',
    color: '#2c3e50',
    marginBottom: 4,
  },
  exampleDescription: {
    fontSize: 12,
    color: '#666',
  },
  challengeCard: {
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
  challengeTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#2c3e50',
    marginBottom: 8,
  },
  challengeDescription: {
    fontSize: 14,
    color: '#666',
    marginBottom: 8,
  },
  challengeDifficulty: {
    fontSize: 12,
    color: '#e74c3c',
    fontWeight: 'bold',
    marginBottom: 12,
  },
  challengeActions: {
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  challengeButton: {
    backgroundColor: '#3498db',
    paddingVertical: 8,
    paddingHorizontal: 16,
    borderRadius: 6,
    flex: 1,
    marginHorizontal: 4,
    alignItems: 'center',
  },
  solveButton: {
    backgroundColor: '#27ae60',
  },
  challengeButtonText: {
    color: '#fff',
    fontSize: 14,
    fontWeight: 'bold',
  },
  solveButtonText: {
    color: '#fff',
    fontSize: 14,
    fontWeight: 'bold',
  },
});

export default CodePlaygroundScreen;