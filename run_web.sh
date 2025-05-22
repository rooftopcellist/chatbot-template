#!/bin/bash

# Function to show usage
show_usage() {
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "OPTIONS:"
    echo "  --refresh    Delete existing index to force recreation"
    echo "  --stop       Stop the web service and clean up"
    echo "  --cleanup    Same as --stop (alias)"
    echo "  --status     Check if web service is running"
    echo "  --help       Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0                 # Start the web interface"
    echo "  $0 --refresh       # Start with fresh index"
    echo "  $0 --stop          # Stop the web service"
    echo "  $0 --status        # Check service status"
}

# Function to stop web service and cleanup
cleanup_web_service() {
    echo "🛑 Stopping web service..."

    # Import configuration to get port
    WEB_PORT=$(python3 -c "import config; print(config.WEB_PORT)" 2>/dev/null || echo "8080")

    # Find and kill web service processes
    WEB_PIDS=$(pgrep -f "python.*web_main.py" 2>/dev/null)

    if [ -n "$WEB_PIDS" ]; then
        echo "Found web service processes: $WEB_PIDS"

        # Try graceful shutdown first
        echo "Attempting graceful shutdown..."
        kill $WEB_PIDS 2>/dev/null

        # Wait a few seconds for graceful shutdown
        sleep 3

        # Check if processes are still running
        REMAINING_PIDS=$(pgrep -f "python.*web_main.py" 2>/dev/null)

        if [ -n "$REMAINING_PIDS" ]; then
            echo "Processes still running, forcing shutdown..."
            kill -9 $REMAINING_PIDS 2>/dev/null
            sleep 1
        fi

        # Final check
        FINAL_CHECK=$(pgrep -f "python.*web_main.py" 2>/dev/null)
        if [ -z "$FINAL_CHECK" ]; then
            echo "✅ Web service stopped successfully"
        else
            echo "⚠️  Some processes may still be running: $FINAL_CHECK"
        fi
    else
        echo "ℹ️  No web service processes found running"
    fi

    # Check if port is still in use
    if command -v lsof >/dev/null 2>&1; then
        PORT_USAGE=$(lsof -ti:$WEB_PORT 2>/dev/null)
        if [ -n "$PORT_USAGE" ]; then
            echo "⚠️  Port $WEB_PORT is still in use by process(es): $PORT_USAGE"
            echo "You may need to manually kill these processes:"
            echo "  kill $PORT_USAGE"
        else
            echo "✅ Port $WEB_PORT is now free"
        fi
    fi

    # Clean up any temporary files if needed
    echo "🧹 Cleaning up temporary files..."

    # Remove any .pyc files in the current directory
    find . -name "*.pyc" -type f -delete 2>/dev/null || true
    find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true

    echo "✅ Cleanup completed"
    exit 0
}

# Function to check service status
check_status() {
    echo "🔍 Checking web service status..."

    # Import configuration
    WEB_HOST=$(python3 -c "import config; print(config.WEB_HOST)" 2>/dev/null || echo "127.0.0.1")
    WEB_PORT=$(python3 -c "import config; print(config.WEB_PORT)" 2>/dev/null || echo "8080")

    # Check for running processes
    WEB_PIDS=$(pgrep -f "python.*web_main.py" 2>/dev/null)

    if [ -n "$WEB_PIDS" ]; then
        echo "✅ Web service is running"
        echo "   Process IDs: $WEB_PIDS"
        echo "   URL: http://${WEB_HOST}:${WEB_PORT}"

        # Test if service responds
        if command -v curl >/dev/null 2>&1; then
            echo "   Testing connection..."
            if curl -s --connect-timeout 5 "http://${WEB_HOST}:${WEB_PORT}/api/health" >/dev/null 2>&1; then
                echo "   ✅ Service is responding"
            else
                echo "   ⚠️  Service is not responding (may still be starting up)"
            fi
        fi
    else
        echo "❌ Web service is not running"

        # Check if port is in use by something else
        if command -v lsof >/dev/null 2>&1; then
            PORT_USAGE=$(lsof -ti:$WEB_PORT 2>/dev/null)
            if [ -n "$PORT_USAGE" ]; then
                echo "   ⚠️  Port $WEB_PORT is in use by other process(es): $PORT_USAGE"
            else
                echo "   ✅ Port $WEB_PORT is available"
            fi
        fi
    fi

    exit 0
}

# Parse command line arguments
REFRESH_INDEX=false
ACTION="start"

while [[ $# -gt 0 ]]; do
    case $1 in
        --refresh)
            REFRESH_INDEX=true
            shift
            ;;
        --stop|--cleanup)
            ACTION="cleanup"
            shift
            ;;
        --status)
            ACTION="status"
            shift
            ;;
        --help|-h)
            show_usage
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            echo ""
            show_usage
            exit 1
            ;;
    esac
done

# Execute the requested action
case $ACTION in
    cleanup)
        cleanup_web_service
        ;;
    status)
        check_status
        ;;
    start)
        # Continue with the original start logic
        ;;
esac

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
