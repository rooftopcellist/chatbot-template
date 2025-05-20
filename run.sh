#!/bin/bash

# Import configuration
OLLAMA_MODEL=$(python3 -c "import config; print(config.OLLAMA_MODEL)")
OLLAMA_BASE_URL=$(python3 -c "import config; print(config.OLLAMA_BASE_URL)")

# Check if Ollama is running
if ! curl -s ${OLLAMA_BASE_URL}/api/tags > /dev/null; then
    echo "Ollama is not running. Starting Ollama..."
    ollama serve &
    # Wait for Ollama to start
    sleep 5
fi

# Check if the model is available
if ! curl -s ${OLLAMA_BASE_URL}/api/tags | grep -q "${OLLAMA_MODEL}"; then
    echo "${OLLAMA_MODEL} model not found. Pulling model..."
    ollama pull ${OLLAMA_MODEL}
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Creating one..."
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
else
    # Activate virtual environment
    source venv/bin/activate
fi

# Run the chatbot
python main.py
