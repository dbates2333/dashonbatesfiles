#!/usr/bin/env bash
set -e

# DealFlow AI — Start Backend + Frontend
echo "🚀 Starting DealFlow AI..."

# Check for .env file
if [ ! -f .env ]; then
  if [ -f .env.example ]; then
    echo "⚠️  No .env file found. Copying from .env.example — set your ANTHROPIC_API_KEY!"
    cp .env.example .env
  else
    echo "❌ No .env file found. Create one with ANTHROPIC_API_KEY=your_key_here"
    exit 1
  fi
fi

# Install backend deps if needed
if [ ! -d backend/.venv ]; then
  echo "📦 Installing backend dependencies..."
  cd backend
  python3 -m venv .venv
  .venv/bin/pip install -r requirements.txt --quiet
  cd ..
fi

# Install frontend deps if needed
if [ ! -d frontend/node_modules ]; then
  echo "📦 Installing frontend dependencies..."
  cd frontend
  npm install --quiet
  cd ..
fi

# Start backend
echo "🔧 Starting backend on http://localhost:8000"
cd backend
../.venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!
cd ..

# Wait a moment for backend to start
sleep 2

# Start frontend
echo "🎨 Starting frontend on http://localhost:5173"
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo ""
echo "✅ DealFlow AI running:"
echo "   Backend:  http://localhost:8000"
echo "   Frontend: http://localhost:5173"
echo "   API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop both services."

# Cleanup on exit
cleanup() {
  echo ""
  echo "Stopping services..."
  kill $BACKEND_PID 2>/dev/null || true
  kill $FRONTEND_PID 2>/dev/null || true
  exit 0
}

trap cleanup INT TERM

# Wait for either process to exit
wait
