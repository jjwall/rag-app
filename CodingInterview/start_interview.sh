#!/bin/bash

echo "🚀 Starting AI Ticket Classification Interview Environment"
echo "=================================================="

# Check if .env file exists
if [ ! -f .env ]; then
    echo "❌ .env file not found!"
    echo "📝 Creating .env file from template..."
    
    if [ -f .env.template ]; then
        cp .env.template .env
        echo "✅ Created .env file from template"
        echo ""
    else
        echo "❌ .env.template file not found!"
        echo "📝 Please create a .env file with your OpenAI API key:"
        echo "   echo 'OPENAI_API_KEY=your_api_key_here' > .env"
        exit 1
    fi
fi

# Check if OpenAI API key is set
if ! grep -q "^OPENAI_API_KEY=sk-" .env; then
    echo "⚠️  Warning: OpenAI API key not found in .env file"
    echo "📝 Please edit .env and add your OpenAI API key"
    echo ""
fi

echo "🐳 Starting Docker containers..."
if ! docker-compose up -d; then
    echo "❌ Docker startup failed!"
    echo "🔍 Common fixes:"
    echo "   • Make sure Docker is running"
    echo "   • Try: docker-compose down && docker-compose up -d --build"
    echo "   • Check logs: docker-compose logs"
    exit 1
fi

echo "⏳ Waiting for services to initialize..."

# Wait for FastAPI to be ready
echo "🔍 Checking FastAPI health..."
for i in {1..30}; do
    if curl -s http://localhost:8000/health > /dev/null 2>&1; then
        echo "✅ FastAPI is ready!"
        break
    fi
    echo "⏳ Waiting for FastAPI... ($i/30)"
    sleep 2
done

# Wait for ChromaDB to be ready
echo "🔍 Checking ChromaDB health..."
for i in {1..30}; do
    if curl -s http://localhost:8001/api/v1/heartbeat > /dev/null 2>&1; then
        echo "✅ ChromaDB is ready!"
        break
    elif curl -s http://localhost:8001/ > /dev/null 2>&1; then
        echo "✅ ChromaDB is responding (no heartbeat endpoint, but server is up)!"
        break
    fi
    echo "⏳ Waiting for ChromaDB... ($i/30)"
    sleep 2
    
    # Debug info on first few attempts
    if [ $i -le 3 ]; then
        echo "   🔧 Debug: Testing ChromaDB connectivity..."
        curl -s http://localhost:8001/api/v1/heartbeat || echo "   ❌ Heartbeat failed"
        curl -s http://localhost:8001/ || echo "   ❌ Root endpoint failed"
    fi
done

echo ""
echo "🎉 Interview environment is ready!"
echo "=================================================="
echo "📋 Services:"
echo "   • FastAPI:  http://localhost:8000"
echo "   • ChromaDB: http://localhost:8001"
echo ""
echo "🧪 Test the setup:"
echo "   python test_requests.py"
echo ""
echo "📚 View API docs:"
echo "   http://localhost:8000/docs"
echo ""
echo "🔍 Check logs:"
echo "   docker-compose logs -f"
echo ""
echo "🛑 Stop services:"
echo "   docker-compose down"
echo ""
echo "🔧 Troubleshooting:"
echo "   • If Docker build fails: docker-compose down && docker-compose up -d --build"
echo "   • If dependencies fail: Use requirements-minimal.txt"
echo "   • Check logs: docker-compose logs -f"
echo "   • Reset everything: docker-compose down -v && docker-compose up -d --build"
echo "=================================================="