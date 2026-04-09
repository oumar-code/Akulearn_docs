/**
 * Visualization Integration Example
 * 
 * Complete example showing how to integrate both Knowledge Graph
 * and Learning Pathway visualizations into your application.
 */

import React, { useState, useEffect } from 'react';
import KnowledgeGraphVisualization from './KnowledgeGraphVisualization';
import LearningPathwayVisualization from './LearningPathwayVisualization';
import './VisualizationIntegrationExample.css';

const VisualizationIntegrationExample = () => {
  const [graphData, setGraphData] = useState(null);
  const [pathwayData, setPathwayData] = useState(null);
  const [studentProgress, setStudentProgress] = useState({});
  const [activeView, setActiveView] = useState('graph'); // 'graph' or 'pathway'
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Fetch data from backend on component mount
  useEffect(() => {
    fetchVisualizationData();
  }, []);

  const fetchVisualizationData = async () => {
    try {
      setLoading(true);
      setError(null);

      // Fetch knowledge graph data
      const graphResponse = await fetch('/api/v3/knowledge-graph');
      if (!graphResponse.ok) {
        throw new Error('Failed to fetch knowledge graph');
      }
      const graph = await graphResponse.json();
      setGraphData(graph);

      // Fetch learning pathways data
      const pathwayResponse = await fetch('/api/v3/learning-paths');
      if (!pathwayResponse.ok) {
        throw new Error('Failed to fetch learning pathways');
      }
      const pathways = await pathwayResponse.json();
      setPathwayData(pathways);

      // Fetch student progress
      const progressResponse = await fetch('/api/v3/students/me/progress');
      if (progressResponse.ok) {
        const progress = await progressResponse.json();
        setStudentProgress(progress);
      }
    } catch (err) {
      console.error('Error fetching visualization data:', err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  // Handle lesson click from either visualization
  const handleLessonClick = (lessonId) => {
    console.log('Navigating to lesson:', lessonId);
    // Navigate to lesson detail page
    window.location.href = `/lessons/${lessonId}`;
  };

  // Handle lesson progress update
  const handleProgressUpdate = async (lessonId, progressData) => {
    try {
      const response = await fetch(`/api/v3/students/me/lessons/${lessonId}/progress`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(progressData)
      });

      if (response.ok) {
        // Update local state
        setStudentProgress(prev => ({
          ...prev,
          [lessonId]: progressData
        }));
      }
    } catch (err) {
      console.error('Error updating progress:', err);
    }
  };

  if (loading) {
    return (
      <div className="visualization-loading">
        <div className="spinner" />
        <p>Loading visualizations...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="visualization-error">
        <h2>⚠️ Error Loading Visualizations</h2>
        <p>{error}</p>
        <button onClick={fetchVisualizationData}>Retry</button>
      </div>
    );
  }

  return (
    <div className="visualization-container">
      {/* Navigation Tabs */}
      <div className="visualization-nav">
        <button
          className={`nav-tab ${activeView === 'graph' ? 'active' : ''}`}
          onClick={() => setActiveView('graph')}
        >
          🗺️ Knowledge Graph
          <span className="tab-description">Explore all lessons and connections</span>
        </button>
        <button
          className={`nav-tab ${activeView === 'pathway' ? 'active' : ''}`}
          onClick={() => setActiveView('pathway')}
        >
          🎯 Learning Pathways
          <span className="tab-description">Follow guided learning paths</span>
        </button>
      </div>

      {/* Visualization Content */}
      <div className="visualization-content">
        {activeView === 'graph' ? (
          <KnowledgeGraphVisualization
            graphData={graphData}
            studentProgress={studentProgress}
            onNodeClick={handleLessonClick}
          />
        ) : (
          <LearningPathwayVisualization
            pathwayData={pathwayData}
            studentProgress={studentProgress}
            onLessonClick={handleLessonClick}
          />
        )}
      </div>

      {/* Help Section */}
      <div className="visualization-help">
        {activeView === 'graph' ? (
          <div className="help-content">
            <h3>💡 Knowledge Graph Tips</h3>
            <ul>
              <li>🖱️ Drag nodes to rearrange the graph</li>
              <li>🔍 Use mouse wheel or pinch to zoom</li>
              <li>🎨 Filter by subject, difficulty, or topics</li>
              <li>📍 Hover over nodes to see lesson details</li>
              <li>🔗 Arrows show prerequisites (blue) and related content (gray)</li>
            </ul>
          </div>
        ) : (
          <div className="help-content">
            <h3>💡 Learning Pathway Tips</h3>
            <ul>
              <li>📚 Select a pathway from the sidebar</li>
              <li>🔓 Complete lessons to unlock the next ones</li>
              <li>📊 Track your progress with visual indicators</li>
              <li>💚 Green = Completed, 🟡 Yellow = In Progress, 🔒 Gray = Locked</li>
              <li>🎯 Follow the recommended sequence for best learning</li>
            </ul>
          </div>
        )}
      </div>
    </div>
  );
};

// Example: Using with React Router
export const VisualizationRoutes = () => {
  return (
    <>
      <Route path="/visualizations" element={<VisualizationIntegrationExample />} />
      <Route path="/visualizations/graph" element={
        <KnowledgeGraphVisualization
          graphData={/* fetch from API */}
          studentProgress={/* fetch from API */}
        />
      } />
      <Route path="/visualizations/pathways" element={
        <LearningPathwayVisualization
          pathwayData={/* fetch from API */}
          studentProgress={/* fetch from API */}
        />
      } />
    </>
  );
};

// Example: Using with custom data
export const CustomVisualizationExample = () => {
  const customGraphData = {
    nodes: [
      { id: 'L1', label: 'Introduction to Algebra', type: 'lesson', subject: 'mathematics', difficulty: 'beginner' },
      { id: 'L2', label: 'Linear Equations', type: 'lesson', subject: 'mathematics', difficulty: 'beginner' },
      { id: 'L3', label: 'Quadratic Equations', type: 'lesson', subject: 'mathematics', difficulty: 'intermediate' }
    ],
    edges: [
      { source: 'L1', target: 'L2', type: 'prerequisite' },
      { source: 'L2', target: 'L3', type: 'prerequisite' }
    ],
    learning_paths: []
  };

  const customPathwayData = {
    pathways: [
      {
        id: 'PATH_1',
        name: 'Algebra Mastery',
        description: 'Complete algebra course from basics to advanced',
        subject: 'mathematics',
        difficulty: 'beginner',
        estimated_duration_hours: 20,
        nodes: ['L1', 'L2', 'L3']
      }
    ],
    lessons: {
      'L1': { id: 'L1', title: 'Introduction to Algebra', duration_minutes: 30, difficulty: 'beginner' },
      'L2': { id: 'L2', title: 'Linear Equations', duration_minutes: 45, difficulty: 'beginner' },
      'L3': { id: 'L3', title: 'Quadratic Equations', duration_minutes: 60, difficulty: 'intermediate' }
    }
  };

  const customProgress = {
    'L1': { status: 'completed', progress_percentage: 100 },
    'L2': { status: 'in-progress', progress_percentage: 60 }
  };

  return (
    <div>
      <h1>Custom Visualization Example</h1>
      <KnowledgeGraphVisualization
        graphData={customGraphData}
        studentProgress={customProgress}
        onNodeClick={(id) => console.log('Clicked:', id)}
      />
      <LearningPathwayVisualization
        pathwayData={customPathwayData}
        studentProgress={customProgress}
        onLessonClick={(id) => console.log('Clicked:', id)}
      />
    </div>
  );
};

export default VisualizationIntegrationExample;
