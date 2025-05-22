# Web Interface Guide

The chatbot includes a modern web interface that provides a user-friendly alternative to the terminal interface. This guide covers how to use and extend the web interface.

## Getting Started

### Running the Web Interface

1. **Start the web server:**
   ```bash
   ./run_web.sh
   ```

   Or run directly:
   ```bash
   python web_main.py
   ```

2. **Stop the web server:**
   ```bash
   ./run_web.sh --stop
   ```

3. **Check service status:**
   ```bash
   ./run_web.sh --status
   ```

4. **Start with fresh index:**
   ```bash
   ./run_web.sh --refresh
   ```

5. **View all options:**
   ```bash
   ./run_web.sh --help
   ```

6. **Open your browser** and navigate to:
   ```
   http://127.0.0.1:8080
   ```

7. **Start chatting** by typing your questions in the input field at the bottom of the page.

### Configuration

The web interface can be configured through `config.py`:

```python
# Web server settings
WEB_HOST = "127.0.0.1"        # Host to bind the web server to
WEB_PORT = 8080               # Port for the web server
WEB_DEBUG = False             # Enable debug mode for development
CORS_ORIGINS = ["*"]          # CORS origins for API access
```

## Features

### Real-time Communication
- **WebSocket Connection**: Real-time bidirectional communication between browser and server
- **Typing Indicators**: Shows when the chatbot is processing your query
- **Connection Status**: Visual indicator of connection health
- **Auto-reconnection**: Automatically attempts to reconnect if connection is lost

### User Interface
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Dark/Light Theme**: Toggle between themes with the moon/sun icon
- **Message History**: Persistent chat history within each session
- **Export Chat**: Download your conversation as a text file
- **Clear Chat**: Reset the conversation history

### Session Management
- **Unique Sessions**: Each browser tab gets its own chat session
- **Message Persistence**: Chat history is maintained during the session
- **Multiple Connections**: Multiple users can chat simultaneously

## Plugin System

The web interface includes an extensible plugin system that allows you to add custom features without modifying the core code.

### Built-in Plugins

#### Message Counter Plugin
Displays a counter showing the number of messages sent in the current session.

#### Keyboard Shortcuts Plugin
Adds keyboard shortcuts for common actions:
- `Ctrl/Cmd + K`: Clear chat
- `Ctrl/Cmd + E`: Export chat
- `Ctrl/Cmd + T`: Toggle theme

### Creating Custom Plugins

To create a custom plugin, extend the `BasePlugin` class:

```javascript
class MyCustomPlugin extends BasePlugin {
    constructor() {
        super('MyCustomPlugin');
    }

    init() {
        super.init();
        // Initialize your plugin here
        this.addHook('message-sent', (message) => {
            console.log('Message sent:', message);
        });
    }

    destroy() {
        super.destroy();
        // Clean up resources here
    }
}

// Register your plugin
window.PluginManager.register('myCustomPlugin', new MyCustomPlugin());
```

### Available Hooks

Plugins can listen to these events:
- `message-sending`: Before a message is sent
- `message-sent`: After a message is sent
- `message-displaying`: Before a message is displayed
- `message-displayed`: After a message is displayed
- `chat-cleared`: When chat history is cleared

## API Endpoints

The web interface provides REST API endpoints for integration:

### Chat Endpoints
- `POST /api/chat`: Send a chat message
- `POST /api/sessions`: Create a new chat session
- `GET /api/sessions/{session_id}`: Get session information
- `GET /api/sessions/{session_id}/history`: Get chat history

### WebSocket Endpoint
- `WS /ws/{session_id}`: Real-time chat communication

### Health Check
- `GET /api/health`: Server health status

## Customization

### Styling
The web interface uses CSS custom properties (variables) for easy theming. You can customize the appearance by modifying `static/style.css`:

```css
:root {
    --primary-color: #007bff;
    --bg-primary: #ffffff;
    --text-primary: #212529;
    /* ... other variables */
}
```

### Templates
The HTML template is located at `templates/index.html` and uses Jinja2 templating. You can modify the structure and add new elements as needed.

### JavaScript
The main application logic is in `static/app.js`. The code is organized into a `ChatApp` class that handles:
- WebSocket communication
- UI interactions
- Message management
- Theme switching
- Error handling

## Troubleshooting

### Connection Issues
If you can't connect to the web interface:

1. **Check if the server is running:**
   ```bash
   curl http://127.0.0.1:8080/api/health
   ```

2. **Verify the port is not in use:**
   ```bash
   lsof -i :8080
   ```

3. **Check firewall settings** if accessing from another machine

### WebSocket Issues
If real-time features aren't working:

1. **Check browser console** for WebSocket errors
2. **Verify WebSocket support** in your browser
3. **Check proxy/firewall settings** that might block WebSocket connections

### Performance Issues
For better performance with large document collections:

1. **Increase server resources** (CPU, RAM)
2. **Optimize chunk size** in `config.py`
3. **Use a faster embedding model** if needed
4. **Consider running on a dedicated server**

## Security Considerations

### Production Deployment
When deploying to production:

1. **Change the host binding:**
   ```python
   WEB_HOST = "0.0.0.0"  # Allow external connections
   ```

2. **Configure CORS properly:**
   ```python
   CORS_ORIGINS = ["https://yourdomain.com"]
   ```

3. **Use HTTPS** with a reverse proxy like nginx
4. **Implement authentication** if needed
5. **Set up proper logging** and monitoring

### Data Privacy
- Chat sessions are stored in memory only
- No chat data is persisted to disk by default
- Sessions are automatically cleaned up after 24 hours of inactivity

## Advanced Usage

### Custom Message Processing
You can extend the `WebInterface` class to add custom message processing:

```python
class CustomWebInterface(WebInterface):
    async def process_query_async(self, session_id: str, query: str) -> Dict:
        # Add custom preprocessing
        processed_query = self.preprocess_query(query)

        # Call parent method
        result = await super().process_query_async(session_id, processed_query)

        # Add custom postprocessing
        if 'assistant_message' in result:
            result['assistant_message']['content'] = self.postprocess_response(
                result['assistant_message']['content']
            )

        return result
```

### Integration with External Services
The web interface can be extended to integrate with external services like Slack, Discord, or custom APIs by creating plugins or modifying the server endpoints.

## Contributing

To contribute to the web interface:

1. **Follow the existing code structure**
2. **Add tests for new features**
3. **Update documentation**
4. **Ensure responsive design**
5. **Test across different browsers**

The web interface is designed to be extensible and maintainable, making it easy to add new features while keeping the core functionality stable.
