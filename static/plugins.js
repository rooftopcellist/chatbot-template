/**
 * Plugin System for Chat Application
 * Provides extensible architecture for adding custom features
 */

class PluginManager {
    constructor() {
        this.plugins = new Map();
        this.hooks = new Map();
        this.initialized = false;
    }
    
    /**
     * Register a plugin
     * @param {string} name - Plugin name
     * @param {Object} plugin - Plugin object with init method
     */
    register(name, plugin) {
        if (this.plugins.has(name)) {
            console.warn(`Plugin ${name} is already registered`);
            return false;
        }
        
        this.plugins.set(name, plugin);
        
        // Initialize plugin if manager is already initialized
        if (this.initialized && typeof plugin.init === 'function') {
            try {
                plugin.init();
                console.log(`Plugin ${name} initialized`);
            } catch (error) {
                console.error(`Error initializing plugin ${name}:`, error);
            }
        }
        
        return true;
    }
    
    /**
     * Unregister a plugin
     * @param {string} name - Plugin name
     */
    unregister(name) {
        const plugin = this.plugins.get(name);
        if (plugin && typeof plugin.destroy === 'function') {
            try {
                plugin.destroy();
            } catch (error) {
                console.error(`Error destroying plugin ${name}:`, error);
            }
        }
        
        return this.plugins.delete(name);
    }
    
    /**
     * Get a plugin by name
     * @param {string} name - Plugin name
     */
    get(name) {
        return this.plugins.get(name);
    }
    
    /**
     * Initialize all registered plugins
     */
    init() {
        this.initialized = true;
        
        for (const [name, plugin] of this.plugins) {
            if (typeof plugin.init === 'function') {
                try {
                    plugin.init();
                    console.log(`Plugin ${name} initialized`);
                } catch (error) {
                    console.error(`Error initializing plugin ${name}:`, error);
                }
            }
        }
    }
    
    /**
     * Register a hook
     * @param {string} hookName - Name of the hook
     * @param {Function} callback - Callback function
     * @param {string} pluginName - Name of the plugin registering the hook
     */
    addHook(hookName, callback, pluginName = 'unknown') {
        if (!this.hooks.has(hookName)) {
            this.hooks.set(hookName, []);
        }
        
        this.hooks.get(hookName).push({
            callback,
            pluginName
        });
    }
    
    /**
     * Execute all callbacks for a hook
     * @param {string} hookName - Name of the hook
     * @param {...any} args - Arguments to pass to callbacks
     */
    executeHook(hookName, ...args) {
        const hooks = this.hooks.get(hookName);
        if (!hooks) return;
        
        for (const hook of hooks) {
            try {
                hook.callback(...args);
            } catch (error) {
                console.error(`Error executing hook ${hookName} from plugin ${hook.pluginName}:`, error);
            }
        }
    }
    
    /**
     * Remove hooks for a specific plugin
     * @param {string} pluginName - Name of the plugin
     */
    removePluginHooks(pluginName) {
        for (const [hookName, hooks] of this.hooks) {
            const filteredHooks = hooks.filter(hook => hook.pluginName !== pluginName);
            this.hooks.set(hookName, filteredHooks);
        }
    }
}

// Global plugin manager instance
window.PluginManager = new PluginManager();

/**
 * Base Plugin Class
 * Extend this class to create new plugins
 */
class BasePlugin {
    constructor(name) {
        this.name = name;
        this.enabled = true;
    }
    
    /**
     * Initialize the plugin
     * Override this method in your plugin
     */
    init() {
        console.log(`${this.name} plugin initialized`);
    }
    
    /**
     * Destroy the plugin
     * Override this method to clean up resources
     */
    destroy() {
        console.log(`${this.name} plugin destroyed`);
        window.PluginManager.removePluginHooks(this.name);
    }
    
    /**
     * Enable the plugin
     */
    enable() {
        this.enabled = true;
    }
    
    /**
     * Disable the plugin
     */
    disable() {
        this.enabled = false;
    }
    
    /**
     * Add a hook
     * @param {string} hookName - Name of the hook
     * @param {Function} callback - Callback function
     */
    addHook(hookName, callback) {
        window.PluginManager.addHook(hookName, callback, this.name);
    }
}

/**
 * Example Plugin: Message Counter
 * Counts and displays the number of messages sent
 */
class MessageCounterPlugin extends BasePlugin {
    constructor() {
        super('MessageCounter');
        this.messageCount = 0;
        this.counterElement = null;
    }
    
    init() {
        super.init();
        this.createCounterDisplay();
        this.addHook('message-sent', () => this.incrementCounter());
        this.addHook('chat-cleared', () => this.resetCounter());
    }
    
    createCounterDisplay() {
        this.counterElement = document.createElement('div');
        this.counterElement.id = 'message-counter';
        this.counterElement.style.cssText = `
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: var(--bg-secondary);
            border: 1px solid var(--border-color);
            border-radius: var(--border-radius);
            padding: 0.5rem 1rem;
            font-size: 0.8rem;
            color: var(--text-secondary);
            z-index: 100;
        `;
        this.updateDisplay();
        document.body.appendChild(this.counterElement);
    }
    
    incrementCounter() {
        this.messageCount++;
        this.updateDisplay();
    }
    
    resetCounter() {
        this.messageCount = 0;
        this.updateDisplay();
    }
    
    updateDisplay() {
        if (this.counterElement) {
            this.counterElement.textContent = `Messages: ${this.messageCount}`;
        }
    }
    
    destroy() {
        super.destroy();
        if (this.counterElement) {
            this.counterElement.remove();
        }
    }
}

/**
 * Example Plugin: Keyboard Shortcuts
 * Adds keyboard shortcuts for common actions
 */
class KeyboardShortcutsPlugin extends BasePlugin {
    constructor() {
        super('KeyboardShortcuts');
        this.shortcuts = new Map();
        this.handleKeyDown = this.handleKeyDown.bind(this);
    }
    
    init() {
        super.init();
        this.registerShortcuts();
        document.addEventListener('keydown', this.handleKeyDown);
    }
    
    registerShortcuts() {
        // Ctrl/Cmd + K: Clear chat
        this.shortcuts.set('ctrl+k', () => {
            if (window.ChatApp) {
                window.ChatApp.clearChat();
            }
        });
        
        // Ctrl/Cmd + E: Export chat
        this.shortcuts.set('ctrl+e', () => {
            if (window.ChatApp) {
                window.ChatApp.exportChat();
            }
        });
        
        // Ctrl/Cmd + T: Toggle theme
        this.shortcuts.set('ctrl+t', () => {
            if (window.ChatApp) {
                window.ChatApp.toggleTheme();
            }
        });
    }
    
    handleKeyDown(event) {
        if (!this.enabled) return;
        
        const key = event.key.toLowerCase();
        const ctrl = event.ctrlKey || event.metaKey;
        
        if (ctrl) {
            const shortcut = `ctrl+${key}`;
            const action = this.shortcuts.get(shortcut);
            
            if (action) {
                event.preventDefault();
                action();
            }
        }
    }
    
    destroy() {
        super.destroy();
        document.removeEventListener('keydown', this.handleKeyDown);
    }
}

/**
 * Plugin Hook Integration
 * Integrate plugin hooks with the main chat application
 */
function integratePluginHooks() {
    // Override ChatApp methods to trigger hooks
    if (window.ChatApp) {
        const originalSendChatMessage = window.ChatApp.sendChatMessage;
        window.ChatApp.sendChatMessage = function(message) {
            window.PluginManager.executeHook('message-sending', message);
            const result = originalSendChatMessage.call(this, message);
            window.PluginManager.executeHook('message-sent', message);
            return result;
        };
        
        const originalClearChat = window.ChatApp.clearChat;
        window.ChatApp.clearChat = function() {
            const result = originalClearChat.call(this);
            window.PluginManager.executeHook('chat-cleared');
            return result;
        };
        
        const originalDisplayMessage = window.ChatApp.displayMessage;
        window.ChatApp.displayMessage = function(message) {
            window.PluginManager.executeHook('message-displaying', message);
            const result = originalDisplayMessage.call(this, message);
            window.PluginManager.executeHook('message-displayed', message);
            return result;
        };
    }
}

// Auto-initialize plugins when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    // Register example plugins (can be disabled by removing these lines)
    window.PluginManager.register('messageCounter', new MessageCounterPlugin());
    window.PluginManager.register('keyboardShortcuts', new KeyboardShortcutsPlugin());
    
    // Initialize plugin system
    window.PluginManager.init();
    
    // Integrate hooks with main app (after ChatApp is initialized)
    setTimeout(integratePluginHooks, 100);
});

// Export for use in other scripts
window.BasePlugin = BasePlugin;
