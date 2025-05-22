/**
 * Main Chat Application
 * Handles WebSocket communication, UI interactions, and message management
 */

class ChatApp {
    constructor() {
        this.websocket = null;
        this.sessionId = null;
        this.isConnected = false;
        this.messageQueue = [];
        this.reconnectAttempts = 0;
        this.maxReconnectAttempts = 5;
        this.reconnectDelay = 1000;
        
        // DOM elements
        this.elements = {};
        
        // Bind methods
        this.handleMessage = this.handleMessage.bind(this);
        this.handleSendMessage = this.handleSendMessage.bind(this);
        this.handleKeyPress = this.handleKeyPress.bind(this);
        this.handleInputChange = this.handleInputChange.bind(this);
    }
    
    init() {
        this.initializeElements();
        this.setupEventListeners();
        this.initializeTheme();
        this.generateSessionId();
        this.connect();
    }
    
    initializeElements() {
        this.elements = {
            messageInput: document.getElementById('message-input'),
            sendButton: document.getElementById('send-button'),
            chatMessages: document.getElementById('chat-messages'),
            typingIndicator: document.getElementById('typing-indicator'),
            connectionStatus: document.getElementById('connection-status'),
            statusDot: document.querySelector('.status-dot'),
            statusText: document.querySelector('.status-text'),
            charCount: document.getElementById('char-count'),
            welcomeMessage: document.getElementById('welcome-message'),
            themeToggle: document.getElementById('theme-toggle'),
            exportChat: document.getElementById('export-chat'),
            clearChat: document.getElementById('clear-chat'),
            errorModal: document.getElementById('error-modal'),
            errorMessage: document.getElementById('error-message'),
            retryConnection: document.getElementById('retry-connection'),
            modalClose: document.querySelector('.modal-close')
        };
    }
    
    setupEventListeners() {
        // Message input and sending
        this.elements.sendButton.addEventListener('click', this.handleSendMessage);
        this.elements.messageInput.addEventListener('keypress', this.handleKeyPress);
        this.elements.messageInput.addEventListener('input', this.handleInputChange);
        
        // Header controls
        this.elements.themeToggle.addEventListener('click', () => this.toggleTheme());
        this.elements.exportChat.addEventListener('click', () => this.exportChat());
        this.elements.clearChat.addEventListener('click', () => this.clearChat());
        
        // Modal controls
        this.elements.retryConnection.addEventListener('click', () => this.retryConnection());
        this.elements.modalClose.addEventListener('click', () => this.hideErrorModal());
        
        // Auto-resize textarea
        this.elements.messageInput.addEventListener('input', this.autoResizeTextarea);
    }
    
    generateSessionId() {
        this.sessionId = 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    }
    
    connect() {
        if (this.websocket) {
            this.websocket.close();
        }
        
        this.updateConnectionStatus('connecting', 'Connecting...');
        
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const wsUrl = `${protocol}//${window.location.host}/ws/${this.sessionId}`;
        
        try {
            this.websocket = new WebSocket(wsUrl);
            this.websocket.onopen = () => this.handleConnectionOpen();
            this.websocket.onmessage = (event) => this.handleMessage(event);
            this.websocket.onclose = () => this.handleConnectionClose();
            this.websocket.onerror = (error) => this.handleConnectionError(error);
        } catch (error) {
            console.error('WebSocket connection error:', error);
            this.handleConnectionError(error);
        }
    }
    
    handleConnectionOpen() {
        console.log('WebSocket connected');
        this.isConnected = true;
        this.reconnectAttempts = 0;
        this.updateConnectionStatus('connected', 'Connected');
        this.hideErrorModal();
        
        // Process queued messages
        while (this.messageQueue.length > 0) {
            const message = this.messageQueue.shift();
            this.sendMessage(message);
        }
    }
    
    handleConnectionClose() {
        console.log('WebSocket disconnected');
        this.isConnected = false;
        this.updateConnectionStatus('disconnected', 'Disconnected');
        
        // Attempt to reconnect
        if (this.reconnectAttempts < this.maxReconnectAttempts) {
            setTimeout(() => {
                this.reconnectAttempts++;
                this.connect();
            }, this.reconnectDelay * Math.pow(2, this.reconnectAttempts));
        } else {
            this.showErrorModal('Connection lost. Please refresh the page to reconnect.');
        }
    }
    
    handleConnectionError(error) {
        console.error('WebSocket error:', error);
        this.updateConnectionStatus('error', 'Connection Error');
        this.showErrorModal('Unable to connect to the server. Please check your connection.');
    }
    
    handleMessage(event) {
        try {
            const data = JSON.parse(event.data);
            
            switch (data.type) {
                case 'message':
                    this.displayMessage(data.message);
                    break;
                case 'typing':
                    this.showTypingIndicator(data.is_typing);
                    break;
                case 'history':
                    this.loadChatHistory(data.data);
                    break;
                case 'session_info':
                    console.log('Session info:', data.data);
                    break;
                default:
                    console.log('Unknown message type:', data.type);
            }
        } catch (error) {
            console.error('Error parsing message:', error);
        }
    }
    
    handleSendMessage() {
        const message = this.elements.messageInput.value.trim();
        if (message) {
            this.sendChatMessage(message);
            this.elements.messageInput.value = '';
            this.updateCharCount();
            this.autoResizeTextarea();
            this.elements.sendButton.disabled = true;
        }
    }
    
    handleKeyPress(event) {
        if (event.key === 'Enter' && !event.shiftKey) {
            event.preventDefault();
            this.handleSendMessage();
        }
    }
    
    handleInputChange() {
        this.updateCharCount();
        const hasText = this.elements.messageInput.value.trim().length > 0;
        this.elements.sendButton.disabled = !hasText || !this.isConnected;
    }
    
    sendChatMessage(message) {
        if (this.isConnected) {
            this.sendMessage({
                type: 'chat',
                message: message
            });
        } else {
            // Queue message for when connection is restored
            this.messageQueue.push({
                type: 'chat',
                message: message
            });
            this.showErrorModal('Not connected. Message will be sent when connection is restored.');
        }
    }
    
    sendMessage(data) {
        if (this.websocket && this.websocket.readyState === WebSocket.OPEN) {
            this.websocket.send(JSON.stringify(data));
        }
    }
    
    displayMessage(message) {
        const messageElement = this.createMessageElement(message);
        this.elements.chatMessages.appendChild(messageElement);
        this.scrollToBottom();
        this.hideWelcomeMessage();
    }
    
    createMessageElement(message) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${message.role} fade-in`;
        messageDiv.setAttribute('data-message-id', message.id);
        
        const avatar = document.createElement('div');
        avatar.className = 'message-avatar';
        avatar.textContent = message.role === 'user' ? '👤' : '🤖';
        
        const content = document.createElement('div');
        content.className = 'message-content';
        
        const text = document.createElement('div');
        text.className = 'message-text';
        text.textContent = message.content;
        
        const time = document.createElement('div');
        time.className = 'message-time';
        time.textContent = this.formatTime(message.timestamp);
        
        content.appendChild(text);
        content.appendChild(time);
        messageDiv.appendChild(avatar);
        messageDiv.appendChild(content);
        
        return messageDiv;
    }
    
    showTypingIndicator(isTyping) {
        if (isTyping) {
            this.elements.typingIndicator.classList.remove('hidden');
            this.scrollToBottom();
        } else {
            this.elements.typingIndicator.classList.add('hidden');
        }
    }
    
    loadChatHistory(messages) {
        this.elements.chatMessages.innerHTML = '';
        messages.forEach(message => {
            this.displayMessage(message);
        });
        
        if (messages.length > 0) {
            this.hideWelcomeMessage();
        }
    }
    
    updateConnectionStatus(status, text) {
        this.elements.statusText.textContent = text;
        this.elements.statusDot.className = `status-dot ${status}`;
    }
    
    updateCharCount() {
        const count = this.elements.messageInput.value.length;
        const maxLength = this.elements.messageInput.maxLength;
        this.elements.charCount.textContent = `${count}/${maxLength}`;
        
        if (count > maxLength * 0.9) {
            this.elements.charCount.style.color = 'var(--warning-color)';
        } else {
            this.elements.charCount.style.color = 'var(--text-muted)';
        }
    }
    
    autoResizeTextarea() {
        const textarea = this.elements.messageInput;
        textarea.style.height = 'auto';
        textarea.style.height = Math.min(textarea.scrollHeight, 120) + 'px';
    }
    
    scrollToBottom() {
        this.elements.chatMessages.scrollTop = this.elements.chatMessages.scrollHeight;
    }
    
    hideWelcomeMessage() {
        if (this.elements.welcomeMessage) {
            this.elements.welcomeMessage.style.display = 'none';
        }
    }
    
    formatTime(timestamp) {
        const date = new Date(timestamp);
        return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    }
    
    // Theme management
    initializeTheme() {
        const savedTheme = localStorage.getItem('chat-theme') || 'light';
        this.setTheme(savedTheme);
    }
    
    toggleTheme() {
        const currentTheme = document.documentElement.getAttribute('data-theme') || 'light';
        const newTheme = currentTheme === 'light' ? 'dark' : 'light';
        this.setTheme(newTheme);
    }
    
    setTheme(theme) {
        document.documentElement.setAttribute('data-theme', theme);
        localStorage.setItem('chat-theme', theme);
        
        const themeIcon = this.elements.themeToggle.querySelector('.theme-icon');
        themeIcon.textContent = theme === 'light' ? '🌙' : '☀️';
    }
    
    // Chat management
    exportChat() {
        const messages = Array.from(this.elements.chatMessages.children).map(messageEl => {
            const role = messageEl.classList.contains('user') ? 'User' : window.CHATBOT_CONFIG.name;
            const content = messageEl.querySelector('.message-text').textContent;
            const time = messageEl.querySelector('.message-time').textContent;
            return `[${time}] ${role}: ${content}`;
        });
        
        const chatText = messages.join('\n\n');
        const blob = new Blob([chatText], { type: 'text/plain' });
        const url = URL.createObjectURL(blob);
        
        const a = document.createElement('a');
        a.href = url;
        a.download = `chat-export-${new Date().toISOString().split('T')[0]}.txt`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    }
    
    clearChat() {
        if (confirm('Are you sure you want to clear the chat history?')) {
            this.elements.chatMessages.innerHTML = '';
            this.elements.welcomeMessage.style.display = 'block';
        }
    }
    
    // Error handling
    showErrorModal(message) {
        this.elements.errorMessage.textContent = message;
        this.elements.errorModal.classList.remove('hidden');
    }
    
    hideErrorModal() {
        this.elements.errorModal.classList.add('hidden');
    }
    
    retryConnection() {
        this.hideErrorModal();
        this.reconnectAttempts = 0;
        this.connect();
    }
}

// Global instance
window.ChatApp = new ChatApp();
