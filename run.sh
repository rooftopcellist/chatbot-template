#!/bin/bash

# Parse command line arguments
REFRESH_INDEX=false
while [[ $# -gt 0 ]]; do
    case $1 in
        --refresh)
            REFRESH_INDEX=true
            shift
            ;;
        *)
            echo "Unknown option: $1"
            echo "Usage: $0 [--refresh]"
            echo "  --refresh    Delete existing index to force recreation"
            exit 1
            ;;
    esac
done

# Import configuration
OLLAMA_MODEL=$(python3 -c "import config; print(config.OLLAMA_MODEL)")
OLLAMA_BASE_URL=$(python3 -c "import config; print(config.OLLAMA_BASE_URL)")
INDEX_PERSIST_DIR=$(python3 -c "import config; print(config.INDEX_PERSIST_DIR)")

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

# Handle --refresh flag: delete existing index
if [ "$REFRESH_INDEX" = true ]; then
    INDEX_FILE="${INDEX_PERSIST_DIR}/index.pkl"
    if [ -f "$INDEX_FILE" ]; then
        echo "Refreshing index: deleting existing index file..."
        rm -f "$INDEX_FILE"
        echo "Index file deleted successfully."
    else
        echo "No existing index file found to delete."
    fi
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
