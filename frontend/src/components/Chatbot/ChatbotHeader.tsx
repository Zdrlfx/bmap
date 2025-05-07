import React from 'react';
import { X, Minimize, Maximize } from 'lucide-react';

interface ChatbotHeaderProps {
  isExpanded: boolean;
  onToggleExpand: () => void;
  onClose: () => void;
}

const ChatbotHeader: React.FC<ChatbotHeaderProps> = ({
  isExpanded,
  onToggleExpand,
  onClose,
}) => {
  return (
    <div className="bg-blue-600 text-white p-3 rounded-t-lg flex items-center justify-between">
      <div className="flex items-center">
        <div className="w-8 h-8 rounded-full bg-white flex items-center justify-center mr-2">
          <span className="text-blue-600 font-bold">AI</span>
        </div>
        <h3 className="font-medium">Support Assistant</h3>
      </div>
      <div className="flex space-x-2">
        <button
          onClick={onToggleExpand}
          className="text-blue-100 hover:text-white transition-colors duration-200"
          aria-label={isExpanded ? "Minimize chat" : "Maximize chat"}
        >
          {isExpanded ? <Minimize size={18} /> : <Maximize size={18} />}
        </button>
        <button
          onClick={onClose}
          className="text-blue-100 hover:text-white transition-colors duration-200"
          aria-label="Close chat"
        >
          <X size={18} />
        </button>
      </div>
    </div>
  );
};

export default ChatbotHeader;