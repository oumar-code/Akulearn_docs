import React, { useEffect, useRef, useState } from 'react';
import * as d3 from 'd3';
import './KnowledgeGraphVisualization.css';

const KnowledgeGraphVisualization = ({ graphData, studentProgress, onNodeClick }) => {
  const svgRef = useRef();
  const [selectedNode, setSelectedNode] = useState(null);
  const [filterSubject, setFilterSubject] = useState('all');
  const [filterDifficulty, setFilterDifficulty] = useState('all');
  const [showTopics, setShowTopics] = useState(true);
  const [layout, setLayout] = useState('force');

  useEffect(() => {
    if (!graphData || !graphData.nodes) return;

    // Clear previous visualization
    d3.select(svgRef.current).selectAll('*').remove();

    // Filter data
    let filteredNodes = graphData.nodes.filter(node => {
      if (!showTopics && node.type === 'topic') return false;
      if (filterSubject !== 'all' && node.subject !== filterSubject) return false;
      if (filterDifficulty !== 'all' && node.difficulty !== filterDifficulty) return false;
      return true;
    });

    const nodeIds = new Set(filteredNodes.map(n => n.id));
    let filteredEdges = graphData.edges.filter(
      edge => nodeIds.has(edge.source) && nodeIds.has(edge.target)
    );

    // Setup SVG
    const width = 1200;
    const height = 800;
    const svg = d3.select(svgRef.current)
      .attr('width', width)
      .attr('height', height)
      .attr('viewBox', [0, 0, width, height]);

    // Add zoom behavior
    const g = svg.append('g');
    const zoom = d3.zoom()
      .scaleExtent([0.1, 4])
      .on('zoom', (event) => {
        g.attr('transform', event.transform);
      });
    svg.call(zoom);

    // Create arrow markers for directed edges
    svg.append('defs').selectAll('marker')
      .data(['prerequisite', 'related', 'follows', 'contains'])
      .join('marker')
      .attr('id', d => `arrow-${d}`)
      .attr('viewBox', '0 -5 10 10')
      .attr('refX', 20)
      .attr('refY', 0)
      .attr('markerWidth', 6)
      .attr('markerHeight', 6)
      .attr('orient', 'auto')
      .append('path')
      .attr('d', 'M0,-5L10,0L0,5')
      .attr('fill', d => {
        const colors = {
          prerequisite: '#ef4444',
          related: '#3b82f6',
          follows: '#8b5cf6',
          contains: '#10b981'
        };
        return colors[d] || '#6b7280';
      });

    // Force simulation
    const simulation = d3.forceSimulation(filteredNodes)
      .force('link', d3.forceLink(filteredEdges)
        .id(d => d.id)
        .distance(d => d.type === 'prerequisite' ? 150 : 100))
      .force('charge', d3.forceManyBody().strength(-300))
      .force('center', d3.forceCenter(width / 2, height / 2))
      .force('collision', d3.forceCollide().radius(40));

    // Draw edges
    const links = g.append('g')
      .selectAll('line')
      .data(filteredEdges)
      .join('line')
      .attr('class', d => `link link-${d.type}`)
      .attr('stroke', d => {
        const colors = {
          prerequisite: '#ef4444',
          related: '#3b82f6',
          follows: '#8b5cf6',
          contains: '#10b981'
        };
        return colors[d.type] || '#6b7280';
      })
      .attr('stroke-width', d => Math.sqrt(d.weight) * 2)
      .attr('stroke-opacity', 0.6)
      .attr('marker-end', d => `url(#arrow-${d.type})`);

    // Draw nodes
    const nodes = g.append('g')
      .selectAll('g')
      .data(filteredNodes)
      .join('g')
      .attr('class', 'node')
      .call(drag(simulation));

    // Node circles
    nodes.append('circle')
      .attr('r', d => d.type === 'lesson' ? 25 : 15)
      .attr('fill', d => getNodeColor(d, studentProgress))
      .attr('stroke', d => selectedNode?.id === d.id ? '#000' : '#fff')
      .attr('stroke-width', d => selectedNode?.id === d.id ? 3 : 2)
      .on('click', (event, d) => {
        event.stopPropagation();
        setSelectedNode(d);
        if (onNodeClick) onNodeClick(d);
      })
      .on('mouseover', function(event, d) {
        d3.select(this).attr('r', d.type === 'lesson' ? 30 : 18);
        showTooltip(event, d);
      })
      .on('mouseout', function(event, d) {
        d3.select(this).attr('r', d.type === 'lesson' ? 25 : 15);
        hideTooltip();
      });

    // Node labels
    nodes.append('text')
      .text(d => d.label.length > 20 ? d.label.substring(0, 20) + '...' : d.label)
      .attr('text-anchor', 'middle')
      .attr('dy', d => d.type === 'lesson' ? 35 : 25)
      .attr('font-size', d => d.type === 'lesson' ? '12px' : '10px')
      .attr('fill', '#1f2937')
      .attr('pointer-events', 'none');

    // Progress indicator (if lesson completed)
    nodes.filter(d => studentProgress && studentProgress[d.id]?.completed)
      .append('text')
      .text('✓')
      .attr('text-anchor', 'middle')
      .attr('dy', 5)
      .attr('font-size', '16px')
      .attr('fill', '#fff')
      .attr('font-weight', 'bold')
      .attr('pointer-events', 'none');

    // Update positions on simulation tick
    simulation.on('tick', () => {
      links
        .attr('x1', d => d.source.x)
        .attr('y1', d => d.source.y)
        .attr('x2', d => d.target.x)
        .attr('y2', d => d.target.y);

      nodes.attr('transform', d => `translate(${d.x},${d.y})`);
    });

    // Drag behavior
    function drag(simulation) {
      function dragstarted(event) {
        if (!event.active) simulation.alphaTarget(0.3).restart();
        event.subject.fx = event.subject.x;
        event.subject.fy = event.subject.y;
      }

      function dragged(event) {
        event.subject.fx = event.x;
        event.subject.fy = event.y;
      }

      function dragended(event) {
        if (!event.active) simulation.alphaTarget(0);
        event.subject.fx = null;
        event.subject.fy = null;
      }

      return d3.drag()
        .on('start', dragstarted)
        .on('drag', dragged)
        .on('end', dragended);
    }

    // Tooltip functions
    function showTooltip(event, d) {
      const tooltip = d3.select('body')
        .append('div')
        .attr('class', 'graph-tooltip')
        .style('position', 'absolute')
        .style('background', '#fff')
        .style('border', '1px solid #ccc')
        .style('border-radius', '8px')
        .style('padding', '12px')
        .style('box-shadow', '0 4px 6px rgba(0,0,0,0.1)')
        .style('pointer-events', 'none')
        .style('z-index', '1000');

      tooltip.html(`
        <div>
          <strong>${d.label}</strong><br/>
          Type: ${d.type}<br/>
          Subject: ${d.subject}<br/>
          Difficulty: ${d.difficulty}
          ${d.metadata?.duration ? `<br/>Duration: ${d.metadata.duration} min` : ''}
          ${d.metadata?.exercises ? `<br/>Exercises: ${d.metadata.exercises}` : ''}
          ${studentProgress && studentProgress[d.id] ? 
            `<br/><span style="color: #10b981;">Progress: ${Math.round(studentProgress[d.id].progress * 100)}%</span>` : 
            ''}
        </div>
      `);

      tooltip
        .style('left', (event.pageX + 10) + 'px')
        .style('top', (event.pageY - 10) + 'px');
    }

    function hideTooltip() {
      d3.selectAll('.graph-tooltip').remove();
    }

    // Cleanup
    return () => {
      simulation.stop();
      hideTooltip();
    };

  }, [graphData, filterSubject, filterDifficulty, showTopics, studentProgress, selectedNode, onNodeClick]);

  // Get node color based on type, difficulty, and progress
  const getNodeColor = (node, progress) => {
    if (node.type === 'topic') {
      return '#d1d5db';
    }

    // Check if completed
    if (progress && progress[node.id]?.completed) {
      return '#10b981'; // Green for completed
    }

    // Check if in progress
    if (progress && progress[node.id]?.progress > 0) {
      return '#f59e0b'; // Orange for in progress
    }

    // Color by difficulty
    const difficultyColors = {
      beginner: '#60a5fa',
      intermediate: '#8b5cf6',
      advanced: '#ec4899',
      expert: '#ef4444'
    };

    return difficultyColors[node.difficulty] || '#6b7280';
  };

  const subjects = graphData?.stats?.subjects || [];
  const difficulties = graphData?.stats?.difficulty_levels || [];

  return (
    <div className="knowledge-graph-container">
      <div className="graph-controls">
        <h2>Knowledge Graph</h2>
        
        <div className="control-group">
          <label>Subject:</label>
          <select value={filterSubject} onChange={(e) => setFilterSubject(e.target.value)}>
            <option value="all">All Subjects</option>
            {subjects.map(subject => (
              <option key={subject} value={subject}>{subject}</option>
            ))}
          </select>
        </div>

        <div className="control-group">
          <label>Difficulty:</label>
          <select value={filterDifficulty} onChange={(e) => setFilterDifficulty(e.target.value)}>
            <option value="all">All Levels</option>
            {difficulties.map(diff => (
              <option key={diff} value={diff}>{diff}</option>
            ))}
          </select>
        </div>

        <div className="control-group">
          <label>
            <input 
              type="checkbox" 
              checked={showTopics} 
              onChange={(e) => setShowTopics(e.target.checked)}
            />
            Show Topics
          </label>
        </div>

        <div className="legend">
          <h4>Legend:</h4>
          <div className="legend-item">
            <span className="legend-color" style={{background: '#60a5fa'}}></span>
            Beginner
          </div>
          <div className="legend-item">
            <span className="legend-color" style={{background: '#8b5cf6'}}></span>
            Intermediate
          </div>
          <div className="legend-item">
            <span className="legend-color" style={{background: '#ec4899'}}></span>
            Advanced
          </div>
          <div className="legend-item">
            <span className="legend-color" style={{background: '#ef4444'}}></span>
            Expert
          </div>
          <div className="legend-item">
            <span className="legend-color" style={{background: '#10b981'}}></span>
            Completed
          </div>
          <div className="legend-item">
            <span className="legend-color" style={{background: '#f59e0b'}}></span>
            In Progress
          </div>
        </div>

        <div className="edge-legend">
          <h4>Connections:</h4>
          <div className="legend-item">
            <span className="legend-line" style={{background: '#ef4444'}}></span>
            Prerequisite
          </div>
          <div className="legend-item">
            <span className="legend-line" style={{background: '#3b82f6'}}></span>
            Related
          </div>
          <div className="legend-item">
            <span className="legend-line" style={{background: '#10b981'}}></span>
            Contains
          </div>
        </div>

        {selectedNode && (
          <div className="selected-node-info">
            <h4>Selected: {selectedNode.label}</h4>
            <p>Type: {selectedNode.type}</p>
            <p>Subject: {selectedNode.subject}</p>
            <p>Difficulty: {selectedNode.difficulty}</p>
            {selectedNode.metadata?.duration && (
              <p>Duration: {selectedNode.metadata.duration} min</p>
            )}
            <button onClick={() => setSelectedNode(null)}>Close</button>
          </div>
        )}
      </div>

      <svg ref={svgRef} className="graph-svg"></svg>
    </div>
  );
};

export default KnowledgeGraphVisualization;
