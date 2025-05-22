/**
 * Example Plugin: Word Count Display
 * Shows the word count of messages in real-time
 * 
 * This is an example of how to create custom plugins for the chat interface.
 * To enable this plugin, include this script in your HTML template.
 */

class WordCountPlugin extends BasePlugin {
    constructor() {
        super('WordCount');
        this.wordCountElement = null;
        this.totalWords = 0;
    }
    
    init() {
        super.init();
        console.log('Word Count Plugin initialized');
        
        // Create the word count display
        this.createWordCountDisplay();
        
        // Listen to message events
        this.addHook('message-displayed', (message) => this.updateWordCount(message));
        this.addHook('chat-cleared', () => this.resetWordCount());
        
        // Add input event listener for real-time word count
        this.setupInputWordCount();
    }
    
    createWordCountDisplay() {
        // Create word count container
        this.wordCountElement = document.createElement('div');
        this.wordCountElement.id = 'word-count-display';
        this.wordCountElement.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: var(--bg-secondary);
            border: 1px solid var(--border-color);
            border-radius: var(--border-radius);
            padding: 0.75rem 1rem;
            font-size: 0.85rem;
            color: var(--text-secondary);
            z-index: 100;
            min-width: 150px;
            box-shadow: var(--shadow);
        `;
        
        this.updateDisplay();
        document.body.appendChild(this.wordCountElement);
    }
    
    updateWordCount(message) {
        if (message && message.content) {
            const words = this.countWords(message.content);
            this.totalWords += words;
            this.updateDisplay();
        }
    }
    
    resetWordCount() {
        this.totalWords = 0;
        this.updateDisplay();
    }
    
    countWords(text) {
        if (!text || typeof text !== 'string') return 0;
        return text.trim().split(/\s+/).filter(word => word.length > 0).length;
    }
    
    updateDisplay() {
        if (this.wordCountElement) {
            this.wordCountElement.innerHTML = `
                <div style="font-weight: 600; margin-bottom: 0.25rem;">Word Count</div>
                <div>Total: ${this.totalWords}</div>
                <div id="current-input-words">Input: 0</div>
            `;
        }
    }
    
    setupInputWordCount() {
        const messageInput = document.getElementById('message-input');
        if (messageInput) {
            messageInput.addEventListener('input', () => {
                const currentWords = this.countWords(messageInput.value);
                const currentInputElement = document.getElementById('current-input-words');
                if (currentInputElement) {
                    currentInputElement.textContent = `Input: ${currentWords}`;
                }
            });
        }
    }
    
    destroy() {
        super.destroy();
        if (this.wordCountElement) {
            this.wordCountElement.remove();
        }
    }
}

/**
 * Example Plugin: Message Timestamps
 * Adds more detailed timestamp information to messages
 */
class TimestampPlugin extends BasePlugin {
    constructor() {
        super('Timestamp');
    }
    
    init() {
        super.init();
        console.log('Timestamp Plugin initialized');
        
        // Hook into message display to enhance timestamps
        this.addHook('message-displayed', (message) => this.enhanceTimestamp(message));
    }
    
    enhanceTimestamp(message) {
        // Find the message element
        const messageElement = document.querySelector(`[data-message-id="${message.id}"]`);
        if (messageElement) {
            const timeElement = messageElement.querySelector('.message-time');
            if (timeElement && message.timestamp) {
                const date = new Date(message.timestamp);
                const enhancedTime = this.formatEnhancedTime(date);
                
                // Add tooltip with full timestamp
                timeElement.title = date.toLocaleString();
                timeElement.textContent = enhancedTime;
            }
        }
    }
    
    formatEnhancedTime(date) {
        const now = new Date();
        const diffMs = now - date;
        const diffMins = Math.floor(diffMs / 60000);
        const diffHours = Math.floor(diffMs / 3600000);
        const diffDays = Math.floor(diffMs / 86400000);
        
        if (diffMins < 1) return 'Just now';
        if (diffMins < 60) return `${diffMins}m ago`;
        if (diffHours < 24) return `${diffHours}h ago`;
        if (diffDays < 7) return `${diffDays}d ago`;
        
        return date.toLocaleDateString();
    }
}

/**
 * Example Plugin: Message Search
 * Adds search functionality to find messages in the chat history
 */
class MessageSearchPlugin extends BasePlugin {
    constructor() {
        super('MessageSearch');
        this.searchContainer = null;
        this.searchInput = null;
        this.isSearchVisible = false;
    }
    
    init() {
        super.init();
        console.log('Message Search Plugin initialized');
        
        this.createSearchInterface();
        this.setupKeyboardShortcut();
    }
    
    createSearchInterface() {
        // Create search container
        this.searchContainer = document.createElement('div');
        this.searchContainer.id = 'message-search';
        this.searchContainer.style.cssText = `
            position: fixed;
            top: 80px;
            right: 20px;
            background: var(--bg-primary);
            border: 1px solid var(--border-color);
            border-radius: var(--border-radius);
            padding: 1rem;
            z-index: 200;
            min-width: 300px;
            box-shadow: var(--shadow-lg);
            display: none;
        `;
        
        // Create search input
        this.searchInput = document.createElement('input');
        this.searchInput.type = 'text';
        this.searchInput.placeholder = 'Search messages...';
        this.searchInput.style.cssText = `
            width: 100%;
            padding: 0.5rem;
            border: 1px solid var(--border-color);
            border-radius: var(--border-radius);
            background: var(--bg-secondary);
            color: var(--text-primary);
            font-size: 0.9rem;
        `;
        
        // Create close button
        const closeButton = document.createElement('button');
        closeButton.textContent = '×';
        closeButton.style.cssText = `
            position: absolute;
            top: 0.5rem;
            right: 0.5rem;
            background: none;
            border: none;
            font-size: 1.2rem;
            cursor: pointer;
            color: var(--text-secondary);
        `;
        
        // Create results container
        const resultsContainer = document.createElement('div');
        resultsContainer.id = 'search-results';
        resultsContainer.style.cssText = `
            margin-top: 0.5rem;
            max-height: 200px;
            overflow-y: auto;
        `;
        
        // Assemble search interface
        this.searchContainer.appendChild(closeButton);
        this.searchContainer.appendChild(this.searchInput);
        this.searchContainer.appendChild(resultsContainer);
        document.body.appendChild(this.searchContainer);
        
        // Event listeners
        this.searchInput.addEventListener('input', () => this.performSearch());
        closeButton.addEventListener('click', () => this.hideSearch());
    }
    
    setupKeyboardShortcut() {
        document.addEventListener('keydown', (event) => {
            // Ctrl/Cmd + F to open search
            if ((event.ctrlKey || event.metaKey) && event.key === 'f') {
                event.preventDefault();
                this.toggleSearch();
            }
            
            // Escape to close search
            if (event.key === 'Escape' && this.isSearchVisible) {
                this.hideSearch();
            }
        });
    }
    
    toggleSearch() {
        if (this.isSearchVisible) {
            this.hideSearch();
        } else {
            this.showSearch();
        }
    }
    
    showSearch() {
        this.searchContainer.style.display = 'block';
        this.isSearchVisible = true;
        this.searchInput.focus();
    }
    
    hideSearch() {
        this.searchContainer.style.display = 'none';
        this.isSearchVisible = false;
        this.clearSearchResults();
    }
    
    performSearch() {
        const query = this.searchInput.value.toLowerCase().trim();
        const resultsContainer = document.getElementById('search-results');
        
        if (!query) {
            this.clearSearchResults();
            return;
        }
        
        // Search through all messages
        const messages = document.querySelectorAll('.message');
        const results = [];
        
        messages.forEach((messageEl, index) => {
            const textEl = messageEl.querySelector('.message-text');
            if (textEl && textEl.textContent.toLowerCase().includes(query)) {
                results.push({
                    element: messageEl,
                    text: textEl.textContent,
                    index: index
                });
            }
        });
        
        this.displaySearchResults(results, query);
    }
    
    displaySearchResults(results, query) {
        const resultsContainer = document.getElementById('search-results');
        resultsContainer.innerHTML = '';
        
        if (results.length === 0) {
            resultsContainer.innerHTML = '<div style="color: var(--text-muted); font-style: italic;">No results found</div>';
            return;
        }
        
        results.forEach((result, index) => {
            const resultEl = document.createElement('div');
            resultEl.style.cssText = `
                padding: 0.5rem;
                border-bottom: 1px solid var(--border-color);
                cursor: pointer;
                font-size: 0.85rem;
            `;
            
            // Highlight the search term
            const highlightedText = this.highlightSearchTerm(result.text, query);
            resultEl.innerHTML = highlightedText;
            
            // Click to scroll to message
            resultEl.addEventListener('click', () => {
                result.element.scrollIntoView({ behavior: 'smooth', block: 'center' });
                this.highlightMessage(result.element);
                this.hideSearch();
            });
            
            resultsContainer.appendChild(resultEl);
        });
    }
    
    highlightSearchTerm(text, query) {
        const regex = new RegExp(`(${query})`, 'gi');
        return text.replace(regex, '<mark style="background-color: var(--warning-color); padding: 0.1rem;">$1</mark>');
    }
    
    highlightMessage(messageEl) {
        // Temporarily highlight the message
        const originalBg = messageEl.style.backgroundColor;
        messageEl.style.backgroundColor = 'var(--info-color)';
        messageEl.style.transition = 'background-color 0.3s ease';
        
        setTimeout(() => {
            messageEl.style.backgroundColor = originalBg;
        }, 2000);
    }
    
    clearSearchResults() {
        const resultsContainer = document.getElementById('search-results');
        if (resultsContainer) {
            resultsContainer.innerHTML = '';
        }
    }
    
    destroy() {
        super.destroy();
        if (this.searchContainer) {
            this.searchContainer.remove();
        }
    }
}

// Auto-register example plugins when DOM is ready
// Note: These are examples and can be removed or modified as needed
document.addEventListener('DOMContentLoaded', function() {
    // Uncomment the plugins you want to enable:
    
    // window.PluginManager.register('wordCount', new WordCountPlugin());
    // window.PluginManager.register('timestamp', new TimestampPlugin());
    // window.PluginManager.register('messageSearch', new MessageSearchPlugin());
});
