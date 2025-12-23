# 🧠 Akulearn Neo4j Knowledge Graph

Production-ready Neo4j implementation for intelligent educational content relationships in the Akulearn platform.

## 🎯 Overview

This implementation provides a comprehensive knowledge graph system that connects educational content, creates intelligent learning paths, and enables personalized recommendations for Nigerian students preparing for WAEC examinations.

### Key Features

- **Graph Database**: Neo4j-powered knowledge representation
- **Subject Hierarchy**: Complete WAEC subject-topic-subtopic structure
- **Prerequisite Mapping**: Intelligent dependency relationships
- **Content Integration**: CSV import from existing educational materials
- **Learning Paths**: Predefined career-focused learning trajectories
- **Personalization**: Student profile-based recommendations
- **Platform Integration**: Seamless connection with existing content service

## 🚀 Quick Start

### Option 1: Automated Setup (Recommended)

**Windows:**
```bash
setup_neo4j.bat
```

**Linux/Mac:**
```bash
chmod +x setup_neo4j.sh
./setup_neo4j.sh
```

### Option 2: Manual Setup

1. **Start Neo4j:**
   ```bash
   # Using Docker
   docker-compose -f docker-compose-neo4j.yaml up -d

   # Or install Neo4j Desktop from https://neo4j.com/download/
   ```

2. **Install Dependencies:**
   ```bash
   pip install neo4j
   ```

3. **Run Implementation:**
   ```bash
   python knowledge_graph_neo4j.py
   ```

## 📊 Architecture

### Node Types
- **Subject**: Main academic disciplines (Mathematics, Physics, Chemistry, etc.)
- **Topic**: Subject subdivisions (Algebra, Geometry, Mechanics, etc.)
- **Subtopic**: Detailed learning units
- **Concept**: Fundamental ideas and principles
- **Resource**: Educational materials and content
- **LearningPath**: Structured learning trajectories
- **Student**: User profiles and progress tracking

### Relationship Types
- **BELONGS_TO**: Hierarchical containment
- **PREREQUISITE_FOR**: Learning dependencies
- **RELATED_TO**: Cross-subject connections
- **ASSESSES**: Evaluation relationships
- **RECOMMENDS**: Personalized suggestions

## 🔧 Configuration

### Environment Variables
```bash
# Neo4j Connection
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=password
NEO4J_DATABASE=neo4j
```

### Docker Configuration
The `docker-compose-neo4j.yaml` provides:
- Neo4j 5.15 with Graph Data Science plugin
- Persistent data volumes
- Health checks and automatic restarts
- Network isolation for security

## 📈 Implementation Phases

### Phase 1: Foundation ✅
- Neo4j schema creation
- Subject hierarchy establishment
- Basic constraints and indexes
- Prerequisite relationship mapping

### Phase 2: Content Integration ✅
- CSV content import system
- Learning path creation
- Query system implementation
- Cross-subject relationship mapping

### Phase 3: Platform Integration ✅
- Content service integration
- API endpoint extensions
- Student profile management
- Recommendation engine

## 🔍 Query Examples

### Basic Exploration
```cypher
// View all subjects
MATCH (s:Subject) RETURN s.name, s.description

// Count resources by subject
MATCH (s:Subject)<-[:BELONGS_TO]-(r:Resource)
RETURN s.name, count(r) as resources
ORDER BY resources DESC

// Find prerequisites for a topic
MATCH (t:Topic {name: "Calculus"})<-[:PREREQUISITE_FOR]-(prereq:Topic)
RETURN prereq.name, prereq.subject
```

### Advanced Queries
```cypher
// Learning path progress
MATCH (lp:LearningPath {id: "waec_science_track"})
MATCH (lp)-[:RECOMMENDS]->(s:Subject)
MATCH (s)<-[:BELONGS_TO]-(t:Topic)
RETURN s.name, count(t) as topics

// Personalized recommendations
MATCH (r:Resource)
WHERE r.subject IN ["Mathematics", "Physics"]
AND r.difficulty = "intermediate"
RETURN r.title, r.subject, r.estimated_read_time
ORDER BY r.subject
```

## 🎓 Educational Features

### Subject Coverage
- **Mathematics**: Algebra, Geometry, Calculus, Statistics
- **Physics**: Mechanics, Electricity, Waves, Modern Physics
- **Chemistry**: Physical, Organic, Inorganic Chemistry
- **Biology**: Cell Biology, Genetics, Ecology
- **English**: Literature, Language, Communication
- **Additional**: Geography, Economics, History, Computer Science

### Learning Paths
1. **WAEC Science Track**: Complete science subject preparation
2. **Engineering Foundation**: Technical university preparation
3. **Medical Sciences**: Health sciences foundation
4. **Business Studies**: Commerce and management preparation

### Cultural Integration
- Nigerian context and examples
- WAEC syllabus alignment
- Local cultural references
- Regional educational standards

## 🔗 API Integration

### Content Service Extensions
```python
# Get personalized recommendations
recommendations = content_service.get_knowledge_graph_recommendations(
    student_id="student_123",
    subject="Mathematics"
)

# Track learning path progress
progress = content_service.get_learning_path_progress(
    student_id="student_123",
    path_id="waec_science_track"
)
```

### Response Format
```json
{
  "recommendations": [
    {
      "title": "Quadratic Equations",
      "subject": "Mathematics",
      "topic": "Algebra",
      "difficulty": "intermediate",
      "read_time": "25",
      "summary": "Complete guide to solving quadratic equations..."
    }
  ],
  "prerequisites": ["Basic Algebra", "Linear Equations"],
  "related_topics": ["Functions", "Inequalities"],
  "learning_paths": ["waec_science_track", "engineering_foundation"]
}
```

## 📊 Analytics & Monitoring

### Graph Statistics
```python
from knowledge_graph_neo4j import AkulearnKnowledgeGraph

kg = AkulearnKnowledgeGraph()
stats = kg.get_graph_statistics()

print(f"Total Nodes: {stats['total_nodes']}")
print(f"Total Relationships: {stats['total_relationships']}")
print(f"Resources by Subject: {stats['subject_resources']}")
```

### Performance Metrics
- Query response times
- Node/relationship counts
- Learning path completion rates
- Student engagement analytics

## 🛠️ Development

### Project Structure
```
knowledge_graph_neo4j.py          # Main implementation
docker-compose-neo4j.yaml         # Neo4j container setup
setup_neo4j.sh                   # Linux/Mac setup script
setup_neo4j.bat                  # Windows setup script
content_service_integration.py   # Platform integration
```

### Testing
```bash
# Run basic connectivity test
python -c "from knowledge_graph_neo4j import AkulearnKnowledgeGraph; kg = AkulearnKnowledgeGraph(); print('✅ Connected' if kg.driver else '❌ Failed'); kg.close()"

# Test query functionality
python -c "from knowledge_graph_neo4j import AkulearnKnowledgeGraph; kg = AkulearnKnowledgeGraph(); prereqs = kg.find_prerequisites('Calculus'); print(f'Prerequisites: {prereqs}'); kg.close()"
```

### Debugging
- Enable Neo4j browser at `http://localhost:7474`
- Check container logs: `docker logs akulearn-neo4j`
- Monitor queries in Neo4j browser
- Use `kg.get_graph_statistics()` for data validation

## 🔒 Security

### Database Security
- Neo4j authentication enabled
- Bolt protocol encryption
- Container network isolation
- Environment variable configuration

### Data Protection
- Educational content integrity
- Student privacy compliance
- Audit logging for changes
- Backup and recovery procedures

## 📚 Documentation

### API Reference
- `AkulearnKnowledgeGraph()`: Main graph interface
- `find_prerequisites(topic)`: Get topic dependencies
- `recommend_content(profile)`: Personalized recommendations
- `get_learning_path(path_id)`: Learning path details

### Integration Guide
- Content service connection
- Student profile management
- Recommendation engine usage
- Analytics integration

## 🚀 Deployment

### Production Setup
1. Configure production Neo4j instance
2. Set environment variables
3. Run database migrations
4. Deploy application containers
5. Configure monitoring and backups

### Scaling Considerations
- Neo4j cluster configuration
- Load balancing for read queries
- Caching layer for frequent queries
- Database optimization and indexing

## 🤝 Contributing

### Development Workflow
1. Fork the repository
2. Create feature branch
3. Implement changes
4. Add tests and documentation
5. Submit pull request

### Code Standards
- Type hints for all functions
- Comprehensive docstrings
- Error handling and logging
- Performance optimization

## 📄 License

This implementation is part of the Akulearn educational platform.

## 🆘 Support

### Common Issues
- **Connection Failed**: Check Neo4j is running on correct port
- **Import Errors**: Ensure neo4j package is installed
- **Docker Issues**: Verify Docker Desktop is running

### Getting Help
- Check Neo4j logs: `docker logs akulearn-neo4j`
- Validate connection: `python -c "from neo4j import GraphDatabase; print('OK')"`
- Test queries in Neo4j Browser

---

**Built with ❤️ for Nigerian education**