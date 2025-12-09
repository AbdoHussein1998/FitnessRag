


# Start Ollama server in the background
ollama serve &

# Wait for Ollama server to be ready
sleep 5

# Pull the embedding model
ollama pull nomic-embed-text

# Keep container running
wait


