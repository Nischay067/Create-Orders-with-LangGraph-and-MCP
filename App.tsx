import React, { useState, useRef, useEffect } from 'react';
import './App.css';

interface Message {
  sender: 'user' | 'bot';
  text: string;
  context?: Record<string, any>;
  bullets?: string[];
}

const GATEWAY_URL = 'http://localhost:5224/api/chat';
const sessionContext: Record<string, any> = {};

function App() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const chatEndRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const sendMessage = async () => {
    if (!input.trim()) return;
    setMessages((msgs) => [...msgs, { sender: 'user', text: input }]);
    setInput('');
    setLoading(true);
    try {
      const res = await fetch(GATEWAY_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: input, userId: "377488", context: sessionContext }),
      });
      const data = await res.json();
      // Only handle LangGraph output
      if (data.output) {
        let outputText: string;
        if (typeof data.output === 'string') {
          outputText = data.output;
        } else if (
          typeof data.output === 'object' &&
          data.output !== null &&
          Object.values(data.output).every((v) => v === null)
        ) {
          outputText = '';
        } else {
          outputText = JSON.stringify(data.output);
        }
        setMessages((msgs) => [
          ...msgs,
          { sender: 'bot', text: outputText, context: { ...sessionContext } },
        ]);
      } else if (data.reply) {
        // Fallback for reply field (should not be needed in new arch)
        setMessages((msgs) => [
          ...msgs,
          { sender: 'bot', text: data.reply, context: { ...sessionContext } },
        ]);
      } else {
        setMessages((msgs) => [
          ...msgs,
          { sender: 'bot', text: JSON.stringify(data), context: { ...sessionContext } },
        ]);
      }
    } catch (e) {
      setMessages((msgs) => [
        ...msgs,
        { sender: 'bot', text: 'Error connecting to Gateway.' },
      ]);
    }
    setLoading(false);
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') sendMessage();
  };

  return (
    <div className="chatbot-container">
      <div className="chatbot-header">Order Copilot</div>
      <div className="chatbot-messages">
        {messages.map((msg, i) => (
          <div key={i} className={`chatbot-msg ${msg.sender}`}>
            <div>{typeof msg.text === 'string' ? msg.text.replace(/order ID is\s*([0-9\s]+)/i, (match, p1) => {
              const cleanId = p1.replace(/\s+/g, '');
              return `order ID is ${cleanId}`;
            }) : msg.text}</div>
            {Array.isArray(msg.bullets) && msg.bullets.length > 0 && (
              <ul className="chatbot-bullets">
                {msg.bullets.map((b, idx) => (
                  <li key={idx}>{b}</li>
                ))}
              </ul>
            )}
          </div>
        ))}
        <div ref={chatEndRef} />
      </div>
      <div className="chatbot-input-row">
        <input
          type="text"
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Type your message..."
          disabled={loading}
        />
        <button onClick={sendMessage} disabled={loading || !input.trim()}>
          {loading ? '...' : 'Send'}
        </button>
      </div>
    </div>
  );
}

export default App;
