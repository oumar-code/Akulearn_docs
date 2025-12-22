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
  getDatasetCategories,
  getDatasetByCategory,
  analyzeDataset,
  getDataVisualization
} from '../api';

const { width, height } = Dimensions.get('window');

const DatasetExplorerScreen = ({ navigation }) => {
  const { user } = useContext(UserContext);
  const [categories, setCategories] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState(null);
  const [datasets, setDatasets] = useState([]);
  const [selectedDataset, setSelectedDataset] = useState(null);
  const [analysis, setAnalysis] = useState(null);
  const [visualization, setVisualization] = useState(null);
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState('categories');

  useEffect(() => {
    loadCategories();
  }, []);

  const loadCategories = async () => {
    try {
      const categoryData = await getDatasetCategories(user?.token);
      setCategories(categoryData);
    } catch (error) {
      Alert.alert('Error', 'Failed to load dataset categories');
    }
  };

  const loadDatasets = async (category) => {
    setLoading(true);
    try {
      const datasetData = await getDatasetByCategory(category, user?.token);
      setDatasets(datasetData);
      setSelectedCategory(category);
      setActiveTab('datasets');
    } catch (error) {
      Alert.alert('Error', 'Failed to load datasets');
    } finally {
      setLoading(false);
    }
  };

  const analyzeDatasetData = async (dataset) => {
    setLoading(true);
    try {
      const analysisData = await analyzeDataset(dataset.id, user?.token);
      setAnalysis(analysisData);
      setSelectedDataset(dataset);
      setActiveTab('analysis');
    } catch (error) {
      Alert.alert('Error', 'Failed to analyze dataset');
    } finally {
      setLoading(false);
    }
  };

  const loadVisualization = async (dataset) => {
    setLoading(true);
    try {
      const vizData = await getDataVisualization(dataset.id, user?.token);
      setVisualization(vizData);
      setSelectedDataset(dataset);
      setActiveTab('visualization');
    } catch (error) {
      Alert.alert('Error', 'Failed to load visualization');
    } finally {
      setLoading(false);
    }
  };

  const renderCategories = () => (
    <ScrollView style={styles.container}>
      <Text style={styles.title}>Dataset Explorer</Text>
      <Text style={styles.subtitle}>Explore Nigerian economic and scientific data</Text>

      {categories.map((category, index) => (
        <TouchableOpacity
          key={index}
          style={styles.categoryCard}
          onPress={() => loadDatasets(category)}
        >
          <Text style={styles.categoryTitle}>{category.name}</Text>
          <Text style={styles.categoryDescription}>{category.description}</Text>
          <Text style={styles.categoryCount}>{category.dataset_count} datasets</Text>
        </TouchableOpacity>
      ))}
    </ScrollView>
  );

  const renderDatasets = () => (
    <ScrollView style={styles.container}>
      <View style={styles.header}>
        <TouchableOpacity
          style={styles.backButton}
          onPress={() => setActiveTab('categories')}
        >
          <Text style={styles.backButtonText}>← Back to Categories</Text>
        </TouchableOpacity>
        <Text style={styles.sectionTitle}>{selectedCategory?.name} Datasets</Text>
      </View>

      {loading ? (
        <ActivityIndicator size="large" color="#3498db" style={styles.loader} />
      ) : (
        datasets.map((dataset, index) => (
          <View key={index} style={styles.datasetCard}>
            <Text style={styles.datasetTitle}>{dataset.title}</Text>
            <Text style={styles.datasetDescription}>{dataset.description}</Text>
            <Text style={styles.datasetMeta}>
              {dataset.records_count} records • {dataset.last_updated}
            </Text>

            <View style={styles.datasetActions}>
              <TouchableOpacity
                style={styles.actionButton}
                onPress={() => analyzeDatasetData(dataset)}
              >
                <Text style={styles.actionButtonText}>Analyze</Text>
              </TouchableOpacity>

              <TouchableOpacity
                style={[styles.actionButton, styles.visualizeButton]}
                onPress={() => loadVisualization(dataset)}
              >
                <Text style={styles.visualizeButtonText}>Visualize</Text>
              </TouchableOpacity>
            </View>
          </View>
        ))
      )}
    </ScrollView>
  );

  const renderAnalysis = () => (
    <ScrollView style={styles.container}>
      <View style={styles.header}>
        <TouchableOpacity
          style={styles.backButton}
          onPress={() => setActiveTab('datasets')}
        >
          <Text style={styles.backButtonText}>← Back to Datasets</Text>
        </TouchableOpacity>
        <Text style={styles.sectionTitle}>Data Analysis</Text>
      </View>

      {selectedDataset && (
        <View style={styles.analysisContainer}>
          <Text style={styles.datasetTitle}>{selectedDataset.title}</Text>

          {loading ? (
            <ActivityIndicator size="large" color="#3498db" style={styles.loader} />
          ) : analysis ? (
            <View>
              <Text style={styles.analysisSectionTitle}>Summary Statistics</Text>
              <View style={styles.statsGrid}>
                {Object.entries(analysis.summary_stats).map(([key, value]) => (
                  <View key={key} style={styles.statItem}>
                    <Text style={styles.statLabel}>{key}</Text>
                    <Text style={styles.statValue}>{value}</Text>
                  </View>
                ))}
              </View>

              <Text style={styles.analysisSectionTitle}>Key Insights</Text>
              {analysis.insights.map((insight, index) => (
                <View key={index} style={styles.insightCard}>
                  <Text style={styles.insightText}>{insight}</Text>
                </View>
              ))}

              <Text style={styles.analysisSectionTitle}>Trends</Text>
              {analysis.trends.map((trend, index) => (
                <View key={index} style={styles.trendCard}>
                  <Text style={styles.trendText}>{trend}</Text>
                </View>
              ))}
            </View>
          ) : (
            <Text style={styles.noDataText}>No analysis data available</Text>
          )}
        </View>
      )}
    </ScrollView>
  );

  const renderVisualization = () => (
    <ScrollView style={styles.container}>
      <View style={styles.header}>
        <TouchableOpacity
          style={styles.backButton}
          onPress={() => setActiveTab('datasets')}
        >
          <Text style={styles.backButtonText}>← Back to Datasets</Text>
        </TouchableOpacity>
        <Text style={styles.sectionTitle}>Data Visualization</Text>
      </View>

      {selectedDataset && (
        <View style={styles.visualizationContainer}>
          <Text style={styles.datasetTitle}>{selectedDataset.title}</Text>

          {loading ? (
            <ActivityIndicator size="large" color="#3498db" style={styles.loader} />
          ) : visualization ? (
            <View>
              <Text style={styles.vizTitle}>Chart Type: {visualization.chart_type}</Text>

              {/* Placeholder for chart - in real implementation, use a charting library */}
              <View style={styles.chartPlaceholder}>
                <Text style={styles.chartPlaceholderText}>
                  Chart visualization would be displayed here
                </Text>
                <Text style={styles.chartPlaceholderSubtext}>
                  Using library like react-native-chart-kit or victory-native
                </Text>
              </View>

              <Text style={styles.analysisSectionTitle}>Chart Data</Text>
              <ScrollView horizontal style={styles.dataTable}>
                <View>
                  {visualization.data.labels && (
                    <View style={styles.tableRow}>
                      <Text style={[styles.tableCell, styles.tableHeader]}>Label</Text>
                      {visualization.data.labels.map((label, index) => (
                        <Text key={index} style={styles.tableCell}>{label}</Text>
                      ))}
                    </View>
                  )}
                  {visualization.data.datasets && visualization.data.datasets.map((dataset, datasetIndex) => (
                    <View key={datasetIndex} style={styles.tableRow}>
                      <Text style={[styles.tableCell, styles.tableHeader]}>{dataset.label}</Text>
                      {dataset.data.map((value, index) => (
                        <Text key={index} style={styles.tableCell}>{value}</Text>
                      ))}
                    </View>
                  ))}
                </View>
              </ScrollView>
            </View>
          ) : (
            <Text style={styles.noDataText}>No visualization data available</Text>
          )}
        </View>
      )}
    </ScrollView>
  );

  const renderContent = () => {
    switch (activeTab) {
      case 'categories':
        return renderCategories();
      case 'datasets':
        return renderDatasets();
      case 'analysis':
        return renderAnalysis();
      case 'visualization':
        return renderVisualization();
      default:
        return renderCategories();
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
  loader: {
    marginTop: 50,
  },
  categoryCard: {
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
  categoryTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#2c3e50',
    marginBottom: 8,
  },
  categoryDescription: {
    fontSize: 14,
    color: '#666',
    marginBottom: 8,
  },
  categoryCount: {
    fontSize: 12,
    color: '#3498db',
    fontWeight: 'bold',
  },
  datasetCard: {
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
  datasetTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#2c3e50',
    marginBottom: 8,
  },
  datasetDescription: {
    fontSize: 14,
    color: '#666',
    marginBottom: 8,
  },
  datasetMeta: {
    fontSize: 12,
    color: '#95a5a6',
    marginBottom: 12,
  },
  datasetActions: {
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  actionButton: {
    backgroundColor: '#3498db',
    paddingVertical: 8,
    paddingHorizontal: 16,
    borderRadius: 6,
    flex: 1,
    marginHorizontal: 4,
    alignItems: 'center',
  },
  actionButtonText: {
    color: '#fff',
    fontSize: 14,
    fontWeight: 'bold',
  },
  visualizeButton: {
    backgroundColor: '#9b59b6',
  },
  visualizeButtonText: {
    color: '#fff',
    fontSize: 14,
    fontWeight: 'bold',
  },
  analysisContainer: {
    backgroundColor: '#fff',
    borderRadius: 8,
    padding: 16,
    elevation: 2,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.1,
    shadowRadius: 2,
  },
  analysisSectionTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#2c3e50',
    marginTop: 16,
    marginBottom: 12,
  },
  statsGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    marginBottom: 16,
  },
  statItem: {
    width: '48%',
    backgroundColor: '#f8f9fa',
    borderRadius: 6,
    padding: 12,
    margin: '1%',
    alignItems: 'center',
  },
  statLabel: {
    fontSize: 12,
    color: '#666',
    marginBottom: 4,
  },
  statValue: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#2c3e50',
  },
  insightCard: {
    backgroundColor: '#e8f4fd',
    borderRadius: 6,
    padding: 12,
    marginBottom: 8,
    borderLeftWidth: 4,
    borderLeftColor: '#3498db',
  },
  insightText: {
    fontSize: 14,
    color: '#2c3e50',
  },
  trendCard: {
    backgroundColor: '#f0f9e8',
    borderRadius: 6,
    padding: 12,
    marginBottom: 8,
    borderLeftWidth: 4,
    borderLeftColor: '#27ae60',
  },
  trendText: {
    fontSize: 14,
    color: '#2c3e50',
  },
  noDataText: {
    fontSize: 16,
    color: '#666',
    textAlign: 'center',
    marginTop: 50,
  },
  visualizationContainer: {
    backgroundColor: '#fff',
    borderRadius: 8,
    padding: 16,
    elevation: 2,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.1,
    shadowRadius: 2,
  },
  vizTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#2c3e50',
    marginBottom: 16,
  },
  chartPlaceholder: {
    height: 200,
    backgroundColor: '#f8f9fa',
    borderRadius: 8,
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 16,
    borderWidth: 2,
    borderColor: '#dee2e6',
    borderStyle: 'dashed',
  },
  chartPlaceholderText: {
    fontSize: 16,
    color: '#6c757d',
    textAlign: 'center',
  },
  chartPlaceholderSubtext: {
    fontSize: 12,
    color: '#adb5bd',
    textAlign: 'center',
    marginTop: 4,
  },
  dataTable: {
    marginTop: 16,
  },
  tableRow: {
    flexDirection: 'row',
    borderBottomWidth: 1,
    borderBottomColor: '#dee2e6',
    paddingVertical: 8,
  },
  tableCell: {
    minWidth: 80,
    paddingHorizontal: 8,
    fontSize: 12,
    color: '#2c3e50',
  },
  tableHeader: {
    fontWeight: 'bold',
    backgroundColor: '#f8f9fa',
  },
});

export default DatasetExplorerScreen;