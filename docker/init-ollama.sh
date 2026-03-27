#!/bin/sh

echo "⏳ Waiting for Ollama..."

sleep 5

echo "📥 Pulling model..."
ollama pull mistral

echo "🚀 Starting Ollama..."
ollama serve