document.addEventListener('DOMContentLoaded', function() {
    const chatButton = document.getElementById('chat-button');
    const chatWidget = document.getElementById('chat-widget');
    const chatClose = document.getElementById('chat-close');
    const chatMessages = document.getElementById('chat-messages');
    const chatInput = document.getElementById('chat-input');
    const chatForm = document.getElementById('chat-form');
    const chatLoading = document.getElementById('chat-loading');
    const emojiButton = document.getElementById('emoji-button');
    const suggestionsContainer = document.getElementById('chat-suggestions');
    const emojiPicker = document.getElementById('emoji-picker');

    // Quick replies for common questions
    const quickReplies = [
        "What is MetabolX?",
        "How does the analysis work?",
        "What are the benefits?",
        "Is my data secure?",
        "How accurate is the analysis?",
        "Can I get a detailed report?",
        "What biomarkers are analyzed?",
        "How often should I get analyzed?"
    ];

    // Emoji categories and emojis
    const emojiCategories = {
        "Health": ["❤️", "💪", "🏃", "🧘", "🥗", "💊", "🏥", "👨‍⚕️"],
        "Emotions": ["😊", "😌", "😅", "😓", "😢", "😡", "😴", "😇"],
        "Actions": ["👍", "👎", "🙏", "💪", "🤔", "💭", "📝", "📊"],
        "Time": ["⏰", "📅", "🕒", "📆", "⏳", "⌛", "🕐", "🕑"]
    };

    // Initialize quick replies
    function initializeQuickReplies() {
        const quickRepliesContainer = document.createElement('div');
        quickRepliesContainer.className = 'quick-replies';
        quickReplies.forEach(reply => {
            const button = document.createElement('button');
            button.className = 'quick-reply';
            button.textContent = reply;
            button.onclick = () => {
                chatInput.value = reply;
                chatInput.focus();
            };
            quickRepliesContainer.appendChild(button);
        });
        chatMessages.insertBefore(quickRepliesContainer, chatMessages.firstChild);
    }

    // Initialize emoji picker
    function initializeEmojiPicker() {
        const emojiGrid = document.createElement('div');
        emojiGrid.className = 'emoji-grid';
        
        Object.entries(emojiCategories).forEach(([category, emojis]) => {
            const categoryTitle = document.createElement('div');
            categoryTitle.className = 'emoji-category-title';
            categoryTitle.textContent = category;
            emojiGrid.appendChild(categoryTitle);
            
            emojis.forEach(emoji => {
                const emojiButton = document.createElement('div');
                emojiButton.className = 'emoji-item';
                emojiButton.textContent = emoji;
                emojiButton.onclick = () => {
                    insertEmoji(emoji);
                    emojiPicker.classList.remove('visible');
                };
                emojiGrid.appendChild(emojiButton);
            });
        });
        
        emojiPicker.appendChild(emojiGrid);
    }

    // Insert emoji at cursor position
    function insertEmoji(emoji) {
        const start = chatInput.selectionStart;
        const end = chatInput.selectionEnd;
        const text = chatInput.value;
        chatInput.value = text.substring(0, start) + emoji + text.substring(end);
        chatInput.selectionStart = chatInput.selectionEnd = start + emoji.length;
        chatInput.focus();
    }

    // Show typing indicator
    const showTyping = () => {
        const typingDiv = document.createElement('div');
        typingDiv.className = 'chat-message ai-message typing-message';
        typingDiv.innerHTML = `
            <div class="message-icon">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/>
                </svg>
            </div>
            <div class="typing-indicator">
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
            </div>
        `;
        chatMessages.appendChild(typingDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
        return typingDiv;
    };

    // Add message to chat
    function addMessage(type, content, save = true) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `chat-message ${type}-message`;
        
        const timestamp = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        
        messageDiv.innerHTML = `
            <div class="message-icon">
                ${type === 'user' ? `
                    <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/>
                    </svg>
                ` : `
                    <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/>
                    </svg>
                `}
            </div>
            <div class="message-content">
                ${content}
                <div class="message-timestamp">${timestamp}</div>
                ${type === 'user' ? `
                    <div class="message-status">
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
                        </svg>
                        Sent
                    </div>
                ` : ''}
            </div>
        `;
        
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
        
        if (save) {
            saveChatHistory();
        }
    }

    // Handle form submission
    chatForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const message = chatInput.value.trim();
        if (!message) return;

        // Add user message
        addMessage('user', message);
        chatInput.value = '';
        
        // Show typing indicator
        const typingIndicator = showTyping();
        
        try {
            const response = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message }),
            });
            
            const data = await response.json();
            
            // Remove typing indicator
            typingIndicator.remove();
            
            // Add AI response
            addMessage('ai', data.response);
            
            // Update suggestions based on context
            updateSuggestions(data.response);
        } catch (error) {
            console.error('Error:', error);
            typingIndicator.remove();
            addMessage('ai', 'I apologize, but I encountered an error. Please try again.');
        }
    });

    // Update suggestions based on context
    function updateSuggestions(context) {
        const relevantSuggestions = quickReplies.filter(reply => 
            context.toLowerCase().includes(reply.toLowerCase())
        );
        
        if (relevantSuggestions.length > 0) {
            suggestionsContainer.innerHTML = '';
            relevantSuggestions.forEach(suggestion => {
                const item = document.createElement('div');
                item.className = 'suggestion-item';
                item.textContent = suggestion;
                item.onclick = () => {
                    chatInput.value = suggestion;
                    chatInput.focus();
                    suggestionsContainer.classList.remove('visible');
                };
                suggestionsContainer.appendChild(item);
            });
            suggestionsContainer.classList.add('visible');
        } else {
            suggestionsContainer.classList.remove('visible');
        }
    }

    // Toggle chat widget
    chatButton.addEventListener('click', () => {
        chatWidget.classList.toggle('visible');
        if (chatWidget.classList.contains('visible')) {
            chatInput.focus();
        }
    });

    chatClose.addEventListener('click', () => {
        chatWidget.classList.remove('visible');
    });

    // Toggle emoji picker
    emojiButton.addEventListener('click', () => {
        emojiPicker.classList.toggle('visible');
    });

    // Close emoji picker when clicking outside
    document.addEventListener('click', (e) => {
        if (!emojiPicker.contains(e.target) && !emojiButton.contains(e.target)) {
            emojiPicker.classList.remove('visible');
        }
    });

    // Handle input changes for suggestions
    chatInput.addEventListener('input', () => {
        const value = chatInput.value.toLowerCase();
        const matchingSuggestions = quickReplies.filter(reply => 
            reply.toLowerCase().includes(value)
        );
        
        if (matchingSuggestions.length > 0 && value.length > 0) {
            suggestionsContainer.innerHTML = '';
            matchingSuggestions.forEach(suggestion => {
                const item = document.createElement('div');
                item.className = 'suggestion-item';
                item.textContent = suggestion;
                item.onclick = () => {
                    chatInput.value = suggestion;
                    chatInput.focus();
                    suggestionsContainer.classList.remove('visible');
                };
                suggestionsContainer.appendChild(item);
            });
            suggestionsContainer.classList.add('visible');
        } else {
            suggestionsContainer.classList.remove('visible');
        }
    });

    // Initialize features
    initializeQuickReplies();
    initializeEmojiPicker();
    loadChatHistory();
}); 