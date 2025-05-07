import { useState, useCallback } from 'react';
import { ChatMessage, ChatState } from '../types/chat';
import { sendMessageToRasa } from '../services/rasaService';
import { v4 as uuidv4 } from 'uuid';

export const useChat = () => {
  const [chatState, setChatState] = useState<ChatState>({
    messages: [],
    isLoading: false,
    error: null,
  });

  const addMessage = useCallback((text: string, sender: 'user' | 'bot') => {
    const newMessage: ChatMessage = {
      id: uuidv4(),
      text,
      sender,
      timestamp: new Date(),
    };

    setChatState((prevState) => ({
      ...prevState,
      messages: [...prevState.messages, newMessage],
    }));

    return newMessage;
  }, []);

  const sendMessage = useCallback(
    async (message: string) => {
      if (!message.trim()) return;

      // Add user message to chat
      addMessage(message, 'user');

      // Set loading state
      setChatState((prevState) => ({
        ...prevState,
        isLoading: true,
        error: null,
      }));

      try {
        // Send message to Rasa
        const responses = await sendMessageToRasa(message);

        // Process responses (could be multiple)
        if (responses.length === 0) {
          // Handle empty response
          addMessage("I'm not sure how to respond to that.", 'bot');
        } else {
          // Add each response as a separate message
          responses.forEach((response) => {
            if (response.text) {
              addMessage(response.text, 'bot');
            }
            // Handle other response types if needed
          });
        }
      } catch (error) {
        console.error('Error in sendMessage:', error);
        setChatState((prevState) => ({
          ...prevState,
          error: error instanceof Error ? error.message : 'An unknown error occurred',
        }));
        addMessage('Sorry, there was an error connecting to the assistant.', 'bot');
      } finally {
        setChatState((prevState) => ({
          ...prevState,
          isLoading: false,
        }));
      }
    },
    [addMessage]
  );

  const clearMessages = useCallback(() => {
    setChatState({
      messages: [],
      isLoading: false,
      error: null,
    });
  }, []);

  return {
    messages: chatState.messages,
    isLoading: chatState.isLoading,
    error: chatState.error,
    sendMessage,
    clearMessages,
  };
};