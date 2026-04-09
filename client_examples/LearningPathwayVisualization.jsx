import React, { useState, useEffect } from 'react';
import './LearningPathwayVisualization.css';

const LearningPathwayVisualization = ({ pathwayData, studentProgress, onLessonClick }) => {
  const [selectedPath, setSelectedPath] = useState(null);
  const [hoveredLesson, setHoveredLesson] = useState(null);

  useEffect(() => {
    if (pathwayData?.learning_paths && pathwayData.learning_paths.length > 0) {
      setSelectedPath(pathwayData.learning_paths[0]);
    }
  }, [pathwayData]);

  if (!pathwayData || !pathwayData.learning_paths) {
    return <div className="pathway-loading">Loading pathways...</div>;
  }

  const getLessonData = (lessonId) => {
    return pathwayData.nodes.find(node => node.id === lessonId);
  };

  const getLessonStatus = (lessonId) => {
    if (!studentProgress || !studentProgress[lessonId]) {
      return 'not-started';
    }
    if (studentProgress[lessonId].completed) {
      return 'completed';
    }
    if (studentProgress[lessonId].progress > 0) {
      return 'in-progress';
    }
    return 'not-started';
  };

  const getStatusColor = (status) => {
    const colors = {
      'completed': '#10b981',
      'in-progress': '#f59e0b',
      'not-started': '#6b7280',
      'locked': '#d1d5db'
    };
    return colors[status] || '#6b7280';
  };

  const getDifficultyColor = (difficulty) => {
    const colors = {
      beginner: '#60a5fa',
      intermediate: '#8b5cf6',
      advanced: '#ec4899',
      expert: '#ef4444'
    };
    return colors[difficulty] || '#6b7280';
  };

  const isLessonUnlocked = (lessonId, lessonIndex) => {
    if (!selectedPath) return false;
    if (lessonIndex === 0) return true; // First lesson always unlocked
    
    // Check if previous lesson is completed
    const previousLessonId = selectedPath.nodes[lessonIndex - 1];
    const previousStatus = getLessonStatus(previousLessonId);
    return previousStatus === 'completed';
  };

  const calculatePathProgress = (path) => {
    if (!path || !studentProgress) return 0;
    
    const completed = path.nodes.filter(
      nodeId => studentProgress[nodeId]?.completed
    ).length;
    
    return Math.round((completed / path.nodes.length) * 100);
  };

  const handleLessonClick = (lessonId, lessonIndex) => {
    if (!isLessonUnlocked(lessonId, lessonIndex)) {
      alert('Complete previous lessons to unlock this one!');
      return;
    }
    if (onLessonClick) {
      onLessonClick(lessonId);
    }
  };

  return (
    <div className="learning-pathway-container">
      <div className="pathway-sidebar">
        <h2>Learning Pathways</h2>
        
        <div className="pathway-list">
          {pathwayData.learning_paths.map(path => (
            <div
              key={path.id}
              className={`pathway-card ${selectedPath?.id === path.id ? 'selected' : ''}`}
              onClick={() => setSelectedPath(path)}
            >
              <h3>{path.name}</h3>
              <p className="pathway-description">{path.description}</p>
              
              <div className="pathway-meta">
                <span className="pathway-badge" style={{
                  background: getDifficultyColor(path.difficulty),
                  color: '#fff'
                }}>
                  {path.difficulty}
                </span>
                <span className="pathway-duration">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                    <circle cx="12" cy="12" r="10"/>
                    <polyline points="12 6 12 12 16 14"/>
                  </svg>
                  {path.estimated_hours}h
                </span>
                <span className="pathway-lessons">
                  {path.nodes.length} lessons
                </span>
              </div>

              <div className="pathway-progress">
                <div className="progress-bar">
                  <div 
                    className="progress-fill"
                    style={{width: `${calculatePathProgress(path)}%`}}
                  />
                </div>
                <span className="progress-text">
                  {calculatePathProgress(path)}% Complete
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="pathway-visualization">
        {selectedPath && (
          <>
            <div className="pathway-header">
              <h1>{selectedPath.name}</h1>
              <p>{selectedPath.description}</p>
              
              <div className="pathway-stats">
                <div className="stat">
                  <span className="stat-label">Subject</span>
                  <span className="stat-value">{selectedPath.subject}</span>
                </div>
                <div className="stat">
                  <span className="stat-label">Difficulty</span>
                  <span className="stat-value">{selectedPath.difficulty}</span>
                </div>
                <div className="stat">
                  <span className="stat-label">Duration</span>
                  <span className="stat-value">{selectedPath.estimated_hours} hours</span>
                </div>
                <div className="stat">
                  <span className="stat-label">Progress</span>
                  <span className="stat-value">{calculatePathProgress(selectedPath)}%</span>
                </div>
              </div>
            </div>

            <div className="pathway-flow">
              {selectedPath.nodes.map((lessonId, index) => {
                const lesson = getLessonData(lessonId);
                const status = getLessonStatus(lessonId);
                const unlocked = isLessonUnlocked(lessonId, index);
                const actualStatus = unlocked ? status : 'locked';

                if (!lesson) return null;

                return (
                  <React.Fragment key={lessonId}>
                    {/* Lesson Node */}
                    <div
                      className={`pathway-node ${actualStatus} ${hoveredLesson === lessonId ? 'hovered' : ''}`}
                      onClick={() => handleLessonClick(lessonId, index)}
                      onMouseEnter={() => setHoveredLesson(lessonId)}
                      onMouseLeave={() => setHoveredLesson(null)}
                      style={{
                        borderColor: getDifficultyColor(lesson.difficulty),
                        background: actualStatus === 'locked' ? '#f3f4f6' : '#fff'
                      }}
                    >
                      {/* Status Icon */}
                      <div 
                        className="node-status-icon"
                        style={{ background: getStatusColor(actualStatus) }}
                      >
                        {actualStatus === 'completed' && '✓'}
                        {actualStatus === 'in-progress' && '●'}
                        {actualStatus === 'locked' && '🔒'}
                        {actualStatus === 'not-started' && (index + 1)}
                      </div>

                      {/* Lesson Info */}
                      <div className="node-content">
                        <div className="node-number">Lesson {index + 1}</div>
                        <h4 className="node-title">{lesson.label}</h4>
                        <div className="node-meta">
                          <span className="node-difficulty" style={{
                            color: getDifficultyColor(lesson.difficulty)
                          }}>
                            {lesson.difficulty}
                          </span>
                          {lesson.metadata?.duration && (
                            <span className="node-duration">
                              {lesson.metadata.duration} min
                            </span>
                          )}
                        </div>

                        {/* Progress Bar for In-Progress Lessons */}
                        {actualStatus === 'in-progress' && studentProgress[lessonId] && (
                          <div className="node-progress-bar">
                            <div 
                              className="node-progress-fill"
                              style={{
                                width: `${studentProgress[lessonId].progress * 100}%`
                              }}
                            />
                          </div>
                        )}
                      </div>

                      {/* Hover Tooltip */}
                      {hoveredLesson === lessonId && (
                        <div className="node-tooltip">
                          <strong>{lesson.label}</strong>
                          <p>Type: {lesson.type}</p>
                          <p>Subject: {lesson.subject}</p>
                          {lesson.metadata?.exercises && (
                            <p>Exercises: {lesson.metadata.exercises}</p>
                          )}
                          {actualStatus === 'locked' && (
                            <p className="locked-message">
                              🔒 Complete previous lesson to unlock
                            </p>
                          )}
                        </div>
                      )}
                    </div>

                    {/* Connector Arrow */}
                    {index < selectedPath.nodes.length - 1 && (
                      <div className="pathway-connector">
                        <svg width="40" height="80" viewBox="0 0 40 80">
                          <defs>
                            <marker
                              id="arrowhead"
                              markerWidth="10"
                              markerHeight="10"
                              refX="5"
                              refY="5"
                              orient="auto"
                            >
                              <polygon
                                points="0 0, 10 5, 0 10"
                                fill={getStatusColor(status)}
                              />
                            </marker>
                          </defs>
                          <line
                            x1="20"
                            y1="0"
                            x2="20"
                            y2="80"
                            stroke={getStatusColor(status)}
                            strokeWidth="3"
                            strokeDasharray={actualStatus === 'locked' ? '5,5' : 'none'}
                            markerEnd="url(#arrowhead)"
                          />
                        </svg>
                      </div>
                    )}
                  </React.Fragment>
                );
              })}

              {/* Completion Badge */}
              {calculatePathProgress(selectedPath) === 100 && (
                <div className="pathway-completion">
                  <div className="completion-badge">
                    <span className="completion-icon">🎉</span>
                    <h3>Pathway Complete!</h3>
                    <p>Congratulations on completing {selectedPath.name}</p>
                  </div>
                </div>
              )}
            </div>
          </>
        )}
      </div>
    </div>
  );
};

export default LearningPathwayVisualization;
