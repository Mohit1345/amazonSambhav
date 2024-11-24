import { Send } from 'lucide-react';
import { useState } from 'react';
import { api, ChatMessage } from '../services/api';

export default function Chat() {
  const [message, setMessage] = useState('');
  const [history, setHistory]=useState("");
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      role: 'assistant',
      content: 'Hello! How can I help you with your trade compliance questions?'
    }
  ]);
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!message.trim() || isLoading) return;

    const userMessage = message;
    setMessage('');
    
    // Add user message immediately
    setMessages(prev => [...prev, { role: 'user', content: userMessage }]);
    
    setIsLoading(true);
    try {
      const response = await fetch("https://example.com/api/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ message: userMessage, history: history }),
      });
      const data = await response.json();
      print(data)
      setMessages(prev => [...prev, { role: 'assistant', content: data.reply }]);
      setHistory(data.history);
    } catch (error) {
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: 'Sorry, I encountered an error. Please try again.'
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="fixed bottom-0 right-0 w-96 bg-white shadow-lg rounded-tl-2xl border-t border-l border-gray-200">
      <div className="p-4 border-b bg-gray-50 rounded-tl-2xl">
        <h3 className="text-lg font-semibold text-gray-800">Trade Assistant</h3>
      </div>
      
      <div className="h-96 overflow-y-auto p-4 space-y-4">
        {messages.map((msg, index) => (
          <div
            key={index}
            className={`p-4 rounded-lg max-w-[80%] ${
              msg.role === 'assistant'
                ? 'bg-blue-50 text-blue-800'
                : 'bg-gray-100 text-gray-800 ml-auto'
            }`}
          >
            <p>{msg.content}</p>
          </div>
        ))}
        {isLoading && (
          <div className="bg-blue-50 p-4 rounded-lg max-w-[80%]">
            <div className="flex space-x-2">
              <div className="w-2 h-2 bg-blue-600 rounded-full animate-bounce"></div>
              <div className="w-2 h-2 bg-blue-600 rounded-full animate-bounce delay-100"></div>
              <div className="w-2 h-2 bg-blue-600 rounded-full animate-bounce delay-200"></div>
            </div>
          </div>
        )}
      </div>

      <form onSubmit={handleSubmit} className="p-4 border-t bg-white">
        <div className="flex items-center space-x-2">
          <input
            type="text"
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            placeholder="Type your message..."
            className="flex-1 px-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            disabled={isLoading}
          />
          <button
            type="submit"
            disabled={isLoading}
            className="p-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50"
          >
            <Send className="h-5 w-5" />
          </button>
        </div>
      </form>
    </div>
  );
}