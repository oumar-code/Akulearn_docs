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
  getResearchTemplates,
  createResearchJournal,
  getResearchJournals,
  saveResearchJournal,
  getCitationStyles,
  generateCitation
} from '../api';

const { width, height } = Dimensions.get('window');

const ResearchHubScreen = ({ navigation }) => {
  const { user } = useContext(UserContext);
  const [templates, setTemplates] = useState([]);
  const [journals, setJournals] = useState([]);
  const [citationStyles, setCitationStyles] = useState([]);
  const [selectedTemplate, setSelectedTemplate] = useState(null);
  const [currentJournal, setCurrentJournal] = useState(null);
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState('templates');

  useEffect(() => {
    loadTemplates();
    loadJournals();
    loadCitationStyles();
  }, []);

  const loadTemplates = async () => {
    try {
      const templateData = await getResearchTemplates(user?.token);
      setTemplates(templateData);
    } catch (error) {
      Alert.alert('Error', 'Failed to load research templates');
    }
  };

  const loadJournals = async () => {
    try {
      const journalData = await getResearchJournals(user?.token);
      setJournals(journalData);
    } catch (error) {
      Alert.alert('Error', 'Failed to load research journals');
    }
  };

  const loadCitationStyles = async () => {
    try {
      const stylesData = await getCitationStyles(user?.token);
      setCitationStyles(stylesData);
    } catch (error) {
      console.log('Failed to load citation styles');
    }
  };

  const createNewJournal = async (template) => {
    setLoading(true);
    try {
      const newJournal = await createResearchJournal(template.id, user?.token);
      setCurrentJournal(newJournal);
      setSelectedTemplate(template);
      setActiveTab('editor');
    } catch (error) {
      Alert.alert('Error', 'Failed to create research journal');
    } finally {
      setLoading(false);
    }
  };

  const saveJournal = async () => {
    if (!currentJournal) return;

    try {
      await saveResearchJournal(currentJournal.id, currentJournal, user?.token);
      Alert.alert('Success', 'Research journal saved successfully');
      loadJournals(); // Refresh the list
    } catch (error) {
      Alert.alert('Error', 'Failed to save research journal');
    }
  };

  const generateCitationForJournal = async (source, style) => {
    try {
      const citation = await generateCitation(source, style, user?.token);
      // Add citation to current journal
      if (currentJournal) {
        const updatedJournal = {
          ...currentJournal,
          citations: [...(currentJournal.citations || []), citation]
        };
        setCurrentJournal(updatedJournal);
      }
      return citation;
    } catch (error) {
      Alert.alert('Error', 'Failed to generate citation');
    }
  };

  const renderTemplates = () => (
    <ScrollView style={styles.container}>
      <Text style={styles.title}>Research Hub</Text>
      <Text style={styles.subtitle}>Academic writing and research tools</Text>

      {/* Quick Actions */}
      <View style={styles.quickActions}>
        <TouchableOpacity
          style={styles.quickActionButton}
          onPress={() => setActiveTab('journals')}
        >
          <Text style={styles.quickActionIcon}>📝</Text>
          <Text style={styles.quickActionText}>My Journals</Text>
        </TouchableOpacity>

        <TouchableOpacity
          style={styles.quickActionButton}
          onPress={() => setActiveTab('citations')}
        >
          <Text style={styles.quickActionIcon}>📚</Text>
          <Text style={styles.quickActionText}>Citations</Text>
        </TouchableOpacity>

        <TouchableOpacity
          style={styles.quickActionButton}
          onPress={() => navigation.navigate('ResearchTools')}
        >
          <Text style={styles.quickActionIcon}>🔬</Text>
          <Text style={styles.quickActionText}>Research Tools</Text>
        </TouchableOpacity>
      </View>

      {/* Research Templates */}
      <Text style={styles.sectionTitle}>Research Templates</Text>
      {templates.map((template, index) => (
        <TouchableOpacity
          key={index}
          style={styles.templateCard}
          onPress={() => createNewJournal(template)}
        >
          <View style={styles.templateHeader}>
            <Text style={styles.templateTitle}>{template.title}</Text>
            <Text style={styles.templateType}>{template.type}</Text>
          </View>

          <Text style={styles.templateDescription}>{template.description}</Text>

          <View style={styles.templateFeatures}>
            {template.features.map((feature, idx) => (
              <Text key={idx} style={styles.templateFeature}>• {feature}</Text>
            ))}
          </View>

          <View style={styles.templateActions}>
            <TouchableOpacity
              style={styles.useTemplateButton}
              onPress={() => createNewJournal(template)}
            >
              <Text style={styles.useTemplateButtonText}>Use Template</Text>
            </TouchableOpacity>
          </View>
        </TouchableOpacity>
      ))}
    </ScrollView>
  );

  const renderJournals = () => (
    <ScrollView style={styles.container}>
      <View style={styles.header}>
        <TouchableOpacity
          style={styles.backButton}
          onPress={() => setActiveTab('templates')}
        >
          <Text style={styles.backButtonText}>← Back to Templates</Text>
        </TouchableOpacity>
        <Text style={styles.sectionTitle}>My Research Journals</Text>
      </View>

      {journals.length > 0 ? (
        journals.map((journal, index) => (
          <TouchableOpacity
            key={index}
            style={styles.journalCard}
            onPress={() => {
              setCurrentJournal(journal);
              setActiveTab('editor');
            }}
          >
            <View style={styles.journalHeader}>
              <Text style={styles.journalTitle}>{journal.title}</Text>
              <Text style={styles.journalStatus}>{journal.status}</Text>
            </View>

            <Text style={styles.journalAbstract} numberOfLines={2}>
              {journal.abstract || 'No abstract yet'}
            </Text>

            <View style={styles.journalMeta}>
              <Text style={styles.journalDate}>{journal.last_modified}</Text>
              <Text style={styles.journalWords}>
                {journal.word_count || 0} words
              </Text>
            </View>
          </TouchableOpacity>
        ))
      ) : (
        <View style={styles.emptyState}>
          <Text style={styles.emptyStateIcon}>📝</Text>
          <Text style={styles.emptyStateTitle}>No Research Journals Yet</Text>
          <Text style={styles.emptyStateText}>
            Create your first research journal using one of our templates
          </Text>
          <TouchableOpacity
            style={styles.emptyStateButton}
            onPress={() => setActiveTab('templates')}
          >
            <Text style={styles.emptyStateButtonText}>Browse Templates</Text>
          </TouchableOpacity>
        </View>
      )}
    </ScrollView>
  );

  const renderEditor = () => (
    <View style={styles.editorContainer}>
      <View style={styles.editorHeader}>
        <TouchableOpacity
          style={styles.backButton}
          onPress={() => setActiveTab('journals')}
        >
          <Text style={styles.backButtonText}>← Back</Text>
        </TouchableOpacity>

        <Text style={styles.editorTitle}>
          {currentJournal?.title || 'Research Journal'}
        </Text>

        <TouchableOpacity
          style={styles.saveButton}
          onPress={saveJournal}
        >
          <Text style={styles.saveButtonText}>Save</Text>
        </TouchableOpacity>
      </View>

      {loading ? (
        <ActivityIndicator size="large" color="#3498db" style={styles.loader} />
      ) : currentJournal ? (
        <ScrollView style={styles.editorContent}>
          {/* Title */}
          <TextInput
            style={styles.titleInput}
            placeholder="Research Title"
            value={currentJournal.title}
            onChangeText={(text) =>
              setCurrentJournal({...currentJournal, title: text})
            }
          />

          {/* Abstract */}
          <Text style={styles.sectionLabel}>Abstract</Text>
          <TextInput
            style={styles.abstractInput}
            placeholder="Write your research abstract..."
            multiline
            value={currentJournal.abstract}
            onChangeText={(text) =>
              setCurrentJournal({...currentJournal, abstract: text})
            }
          />

          {/* Research Content */}
          <Text style={styles.sectionLabel}>Research Content</Text>
          <TextInput
            style={styles.contentInput}
            placeholder="Write your research here..."
            multiline
            value={currentJournal.content}
            onChangeText={(text) =>
              setCurrentJournal({...currentJournal, content: text})
            }
          />

          {/* Methodology */}
          <Text style={styles.sectionLabel}>Methodology</Text>
          <TextInput
            style={styles.methodologyInput}
            placeholder="Describe your research methodology..."
            multiline
            value={currentJournal.methodology}
            onChangeText={(text) =>
              setCurrentJournal({...currentJournal, methodology: text})
            }
          />

          {/* Citations */}
          <View style={styles.citationsSection}>
            <Text style={styles.sectionLabel}>Citations</Text>
            <TouchableOpacity
              style={styles.addCitationButton}
              onPress={() => setActiveTab('citations')}
            >
              <Text style={styles.addCitationButtonText}>+ Add Citation</Text>
            </TouchableOpacity>

            {currentJournal.citations && currentJournal.citations.map((citation, index) => (
              <View key={index} style={styles.citationItem}>
                <Text style={styles.citationText}>{citation}</Text>
              </View>
            ))}
          </View>
        </ScrollView>
      ) : (
        <Text style={styles.noDataText}>No journal selected</Text>
      )}
    </View>
  );

  const renderCitations = () => (
    <ScrollView style={styles.container}>
      <View style={styles.header}>
        <TouchableOpacity
          style={styles.backButton}
          onPress={() => setActiveTab('templates')}
        >
          <Text style={styles.backButtonText}>← Back</Text>
        </TouchableOpacity>
        <Text style={styles.sectionTitle}>Citation Tools</Text>
      </View>

      {/* Citation Styles */}
      <Text style={styles.subSectionTitle}>Citation Styles</Text>
      <View style={styles.stylesGrid}>
        {citationStyles.map((style, index) => (
          <TouchableOpacity
            key={index}
            style={styles.styleCard}
            onPress={() => {
              // Set as preferred style for current journal
              if (currentJournal) {
                setCurrentJournal({
                  ...currentJournal,
                  citation_style: style.name
                });
              }
            }}
          >
            <Text style={styles.styleName}>{style.name}</Text>
            <Text style={styles.styleExample}>{style.example}</Text>
          </TouchableOpacity>
        ))}
      </View>

      {/* Citation Generator */}
      <Text style={styles.subSectionTitle}>Generate Citation</Text>
      <View style={styles.citationGenerator}>
        <TextInput
          style={styles.sourceInput}
          placeholder="Enter source details (author, title, year, etc.)"
          multiline
        />

        <TouchableOpacity
          style={styles.generateButton}
          onPress={() => {
            // This would generate a citation
            Alert.alert('Feature', 'Citation generation would be implemented here');
          }}
        >
          <Text style={styles.generateButtonText}>Generate Citation</Text>
        </TouchableOpacity>
      </View>

      {/* Citation Examples */}
      <Text style={styles.subSectionTitle}>Citation Examples</Text>
      <View style={styles.examplesContainer}>
        <Text style={styles.exampleTitle}>APA Style:</Text>
        <Text style={styles.exampleText}>
          Smith, J. (2023). The impact of technology on education. Journal of Educational Technology, 15(2), 45-67.
        </Text>

        <Text style={styles.exampleTitle}>MLA Style:</Text>
        <Text style={styles.exampleText}>
          Smith, John. "The Impact of Technology on Education." Journal of Educational Technology, vol. 15, no. 2, 2023, pp. 45-67.
        </Text>

        <Text style={styles.exampleTitle}>Chicago Style:</Text>
        <Text style={styles.exampleText}>
          Smith, John. "The Impact of Technology on Education." Journal of Educational Technology 15, no. 2 (2023): 45-67.
        </Text>
      </View>
    </ScrollView>
  );

  const renderContent = () => {
    switch (activeTab) {
      case 'templates':
        return renderTemplates();
      case 'journals':
        return renderJournals();
      case 'editor':
        return renderEditor();
      case 'citations':
        return renderCitations();
      default:
        return renderTemplates();
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
  quickActions: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    marginBottom: 20,
  },
  quickActionButton: {
    backgroundColor: '#fff',
    borderRadius: 8,
    padding: 16,
    alignItems: 'center',
    width: '30%',
    elevation: 2,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.1,
    shadowRadius: 2,
  },
  quickActionIcon: {
    fontSize: 24,
    marginBottom: 8,
  },
  quickActionText: {
    fontSize: 12,
    color: '#2c3e50',
    textAlign: 'center',
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#2c3e50',
    marginBottom: 12,
  },
  templateCard: {
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
  templateHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 8,
  },
  templateTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#2c3e50',
  },
  templateType: {
    fontSize: 12,
    color: '#3498db',
    backgroundColor: '#e8f4fd',
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 12,
  },
  templateDescription: {
    fontSize: 14,
    color: '#666',
    marginBottom: 12,
  },
  templateFeatures: {
    marginBottom: 16,
  },
  templateFeature: {
    fontSize: 12,
    color: '#666',
    marginBottom: 4,
  },
  templateActions: {
    alignItems: 'flex-end',
  },
  useTemplateButton: {
    backgroundColor: '#3498db',
    paddingVertical: 8,
    paddingHorizontal: 16,
    borderRadius: 6,
  },
  useTemplateButtonText: {
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
  journalCard: {
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
  journalHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 8,
  },
  journalTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#2c3e50',
  },
  journalStatus: {
    fontSize: 12,
    color: '#27ae60',
    backgroundColor: '#f0f9e8',
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 12,
  },
  journalAbstract: {
    fontSize: 14,
    color: '#666',
    marginBottom: 8,
  },
  journalMeta: {
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  journalDate: {
    fontSize: 12,
    color: '#95a5a6',
  },
  journalWords: {
    fontSize: 12,
    color: '#95a5a6',
  },
  emptyState: {
    alignItems: 'center',
    paddingVertical: 50,
  },
  emptyStateIcon: {
    fontSize: 48,
    marginBottom: 16,
  },
  emptyStateTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#2c3e50',
    marginBottom: 8,
  },
  emptyStateText: {
    fontSize: 14,
    color: '#666',
    textAlign: 'center',
    marginBottom: 20,
  },
  emptyStateButton: {
    backgroundColor: '#3498db',
    paddingVertical: 10,
    paddingHorizontal: 20,
    borderRadius: 6,
  },
  emptyStateButtonText: {
    color: '#fff',
    fontSize: 14,
    fontWeight: 'bold',
  },
  editorContainer: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  editorHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    backgroundColor: '#fff',
    padding: 16,
    elevation: 2,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.1,
    shadowRadius: 2,
  },
  editorTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#2c3e50',
    flex: 1,
    textAlign: 'center',
  },
  saveButton: {
    backgroundColor: '#27ae60',
    paddingVertical: 6,
    paddingHorizontal: 12,
    borderRadius: 4,
  },
  saveButtonText: {
    color: '#fff',
    fontSize: 12,
    fontWeight: 'bold',
  },
  editorContent: {
    flex: 1,
    padding: 16,
  },
  titleInput: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#2c3e50',
    borderBottomWidth: 1,
    borderBottomColor: '#ddd',
    paddingVertical: 8,
    marginBottom: 16,
  },
  sectionLabel: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#2c3e50',
    marginTop: 16,
    marginBottom: 8,
  },
  abstractInput: {
    borderWidth: 1,
    borderColor: '#ddd',
    borderRadius: 6,
    padding: 12,
    fontSize: 14,
    minHeight: 80,
    textAlignVertical: 'top',
  },
  contentInput: {
    borderWidth: 1,
    borderColor: '#ddd',
    borderRadius: 6,
    padding: 12,
    fontSize: 14,
    minHeight: 200,
    textAlignVertical: 'top',
  },
  methodologyInput: {
    borderWidth: 1,
    borderColor: '#ddd',
    borderRadius: 6,
    padding: 12,
    fontSize: 14,
    minHeight: 120,
    textAlignVertical: 'top',
  },
  citationsSection: {
    marginBottom: 20,
  },
  addCitationButton: {
    backgroundColor: '#3498db',
    paddingVertical: 8,
    paddingHorizontal: 16,
    borderRadius: 6,
    alignSelf: 'flex-start',
    marginBottom: 12,
  },
  addCitationButtonText: {
    color: '#fff',
    fontSize: 14,
    fontWeight: 'bold',
  },
  citationItem: {
    backgroundColor: '#f8f9fa',
    borderRadius: 6,
    padding: 12,
    marginBottom: 8,
  },
  citationText: {
    fontSize: 12,
    color: '#2c3e50',
    fontStyle: 'italic',
  },
  loader: {
    marginTop: 100,
  },
  noDataText: {
    fontSize: 16,
    color: '#666',
    textAlign: 'center',
    marginTop: 50,
  },
  subSectionTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#2c3e50',
    marginTop: 20,
    marginBottom: 12,
  },
  stylesGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'space-between',
  },
  styleCard: {
    backgroundColor: '#fff',
    borderRadius: 6,
    padding: 12,
    width: '48%',
    marginBottom: 12,
    elevation: 1,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.1,
    shadowRadius: 1,
  },
  styleName: {
    fontSize: 14,
    fontWeight: 'bold',
    color: '#2c3e50',
    marginBottom: 4,
  },
  styleExample: {
    fontSize: 12,
    color: '#666',
  },
  citationGenerator: {
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
  sourceInput: {
    borderWidth: 1,
    borderColor: '#ddd',
    borderRadius: 6,
    padding: 12,
    fontSize: 14,
    minHeight: 80,
    textAlignVertical: 'top',
    marginBottom: 12,
  },
  generateButton: {
    backgroundColor: '#27ae60',
    paddingVertical: 10,
    paddingHorizontal: 20,
    borderRadius: 6,
    alignItems: 'center',
  },
  generateButtonText: {
    color: '#fff',
    fontSize: 14,
    fontWeight: 'bold',
  },
  examplesContainer: {
    backgroundColor: '#fff',
    borderRadius: 8,
    padding: 16,
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
    marginTop: 12,
    marginBottom: 4,
  },
  exampleText: {
    fontSize: 12,
    color: '#666',
    fontStyle: 'italic',
    lineHeight: 18,
  },
});

export default ResearchHubScreen;