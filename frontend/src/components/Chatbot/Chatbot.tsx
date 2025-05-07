import React, { useState, useRef, useEffect } from 'react';
import { MessageSquare } from 'lucide-react';
import ChatMessage from './ChatMessage';
import ChatInput from './ChatInput';
import ChatbotHeader from './ChatbotHeader';
import { useChat } from '../../hooks/useChat';

const Chatbot: React.FC = () => {
  const [isExpanded, setIsExpanded] = useState(false);
  const { messages, isLoading, sendMessage, clearMessages } = useChat();
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Scroll to bottom when messages change
  useEffect(() => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages]);

  // Initial greeting when component mounts
  useEffect(() => {
    if (messages.length === 0) {
      sendMessage('Hello');
    }
  }, [messages.length, sendMessage]);

  const toggleExpand = () => {
    setIsExpanded(!isExpanded);
  };

  const closeChat = () => {
    clearMessages();
  };

  return (
    <div className="fixed inset-0 flex items-center justify-center p-4">
      <div
        className={`bg-white rounded-lg shadow-xl overflow-hidden transition-all duration-300 ease-in-out flex flex-col ${
          isExpanded ? 'w-full h-full' : 'w-full max-w-2xl h-[600px]'
        }`}
      >
        <ChatbotHeader
          isExpanded={isExpanded}
          onToggleExpand={toggleExpand}
          onClose={closeChat}
        />

        {/* Messages Container */}
        <div className="flex-1 overflow-y-auto p-4 bg-gray-50">
          {messages.length === 0 ? (
            <div className="flex items-center justify-center h-full text-gray-400">
              <div className="text-center">
                <MessageSquare className="mx-auto h-12 w-12 mb-2" />
                <p>Start a conversation!</p>
              </div>
            </div>
          ) : (
            messages.map((msg) => <ChatMessage key={msg.id} message={msg} />)
          )}
          {isLoading && (
            <div className="flex justify-start mb-4">
              <div className="bg-gray-200 text-gray-800 rounded-2xl rounded-tl-none px-4 py-2">
                <div className="flex space-x-1">
                  <div className="h-2 w-2 rounded-full bg-gray-400 animate-bounce" style={{ animationDelay: '0ms' }}></div>
                  <div className="h-2 w-2 rounded-full bg-gray-400 animate-bounce" style={{ animationDelay: '150ms' }}></div>
                  <div className="h-2 w-2 rounded-full bg-gray-400 animate-bounce" style={{ animationDelay: '300ms' }}></div>
                </div>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Input Area */}
        <ChatInput onSendMessage={sendMessage} isLoading={isLoading} />
      </div>
    </div>
  );
};

export default Chatbot;