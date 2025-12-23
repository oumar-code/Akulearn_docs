#!/bin/bash
# Neo4j Setup Script for Akulearn Knowledge Graph
# This script helps set up Neo4j for the educational platform

set -e

echo "🧠 Akulearn Neo4j Knowledge Graph Setup"
echo "========================================"

# Check if Docker is available
if command -v docker &> /dev/null; then
    echo "✅ Docker found"

    # Check if docker-compose is available
    if command -v docker-compose &> /dev/null || docker compose version &> /dev/null; then
        echo "✅ Docker Compose found"

        echo "🚀 Starting Neo4j with Docker Compose..."
        echo "This will start Neo4j on:"
        echo "  - HTTP: http://localhost:7474"
        echo "  - Bolt: bolt://localhost:7687"
        echo "  - User: neo4j"
        echo "  - Password: password"
        echo ""

        # Use docker compose (newer syntax) if available, otherwise docker-compose
        if docker compose version &> /dev/null; then
            docker compose -f docker-compose-neo4j.yaml up -d
        else
            docker-compose -f docker-compose-neo4j.yaml up -d
        fi

        echo "⏳ Waiting for Neo4j to be ready..."
        sleep 30

        # Check if Neo4j is healthy
        if docker ps | grep -q akulearn-neo4j; then
            echo "✅ Neo4j container is running"
            echo ""
            echo "🌐 Neo4j Browser: http://localhost:7474"
            echo "🔌 Bolt Connection: bolt://localhost:7687"
            echo "👤 Username: neo4j"
            echo "🔑 Password: password"
            echo ""
        else
            echo "❌ Failed to start Neo4j container"
            exit 1
        fi

    else
        echo "❌ Docker Compose not found"
        echo "Please install Docker Compose to continue"
        exit 1
    fi

else
    echo "❌ Docker not found"
    echo ""
    echo "📦 Installing Neo4j locally..."
    echo "Please download and install Neo4j Desktop from:"
    echo "https://neo4j.com/download/"
    echo ""
    echo "After installation:"
    echo "1. Start Neo4j Desktop"
    echo "2. Create a new project"
    echo "3. Start a database instance"
    echo "4. Note the Bolt URL (usually bolt://localhost:7687)"
    echo "5. Default credentials: neo4j / password"
    echo ""
    echo "Then run: python knowledge_graph_neo4j.py"
    exit 1
fi

echo "🔧 Setting up Python environment..."
pip install neo4j

echo ""
echo "🚀 Running knowledge graph implementation..."
python knowledge_graph_neo4j.py

echo ""
echo "🎉 Setup complete!"
echo ""
echo "📊 To explore your knowledge graph:"
echo "1. Open http://localhost:7474 in your browser"
echo "2. Login with neo4j/password"
echo "3. Try queries like: MATCH (n) RETURN n LIMIT 25"
echo ""
echo "🔍 Useful Cypher queries:"
echo "  - MATCH (s:Subject) RETURN s.name, s.description"
echo "  - MATCH (r:Resource) RETURN count(r)"
echo "  - MATCH (t:Topic)-[:BELONGS_TO]->(s:Subject) RETURN s.name, count(t)"
echo ""
echo "📚 Next steps:"
echo "1. Integrate with your content service"
echo "2. Add student profiles and personalization"
echo "3. Implement recommendation algorithms"
echo "4. Add analytics and monitoring"