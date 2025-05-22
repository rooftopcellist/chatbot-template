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
WEB_HOST=$(python3 -c "import config; print(config.WEB_HOST)")
WEB_PORT=$(python3 -c "import config; print(config.WEB_PORT)")

# Check if Ollama is running
if ! curl -s ${OLLAMA_BASE_URL}/api/tags > /dev/null; then
    echo "Ollama is not running. Starting Ollama..."
    ollama serve &
    # Wait for Ollama to start
    sleep 5
fi

# Check if the model exists
if ! curl -s ${OLLAMA_BASE_URL}/api/tags | grep -q ${OLLAMA_MODEL}; then
    echo "Model ${OLLAMA_MODEL} not found. Pulling..."
    ollama pull ${OLLAMA_MODEL}
fi

# Refresh index if requested
if [ "$REFRESH_INDEX" = true ]; then
    echo "Refreshing index..."
    if [ -d "$INDEX_PERSIST_DIR" ]; then
        rm -rf "$INDEX_PERSIST_DIR"
        echo "Deleted existing index directory: $INDEX_PERSIST_DIR"
    fi
fi

# Check if virtual environment is activated
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "Warning: No virtual environment detected."
    echo "Consider activating your virtual environment first:"
    echo "  source venv/bin/activate"
    echo ""
fi

# Run the web interface
echo "Starting web interface..."
echo "Web interface will be available at: http://${WEB_HOST}:${WEB_PORT}"
echo "Press Ctrl+C to stop the server"
echo ""

python3 web_main.py
