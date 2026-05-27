'use client';

import { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Bot, Send, Sparkles, Copy, MoreVertical, Trash2,
  Edit2, Search, Settings, X, Loader2, User, ArrowLeft
} from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import { Avatar, AvatarFallback } from '@/components/ui/avatar';

interface Message {
  id: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
  timestamp: Date;
  actions?: string[];
}

const initialMessages: Message[] = [
  {
    id: '1',
    role: 'assistant',
    content: 'Hello! I\'m your AI assistant. How can I help you today? I can assist with tasks like:\n\n• Analyzing data and generating reports\n• Answering questions\n• Helping with automation workflows\n• Customer support inquiries',
    timestamp: new Date(),
  },
];

const suggestions = [
  'Analyze Q4 sales data',
  'Create a report on customer feedback',
  'Help me set up an automation',
  'Summarize this week\'s metrics',
];

export default function ChatPage() {
  const [messages, setMessages] = useState<Message[]>(initialMessages);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [showSuggestions, setShowSuggestions] = useState(true);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim() || isLoading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: input,
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);
    setShowSuggestions(false);

    // Simulate AI response
    setTimeout(() => {
      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: 'I understand you want to ' + input.toLowerCase() + '. Let me help you with that. Here\'s what I found...',
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, assistantMessage]);
      setIsLoading(false);
    }, 2000);
  };

  const handleSuggestionClick = (suggestion: string) => {
    setInput(suggestion);
    setShowSuggestions(false);
  };

  const copyMessage = (content: string) => {
    navigator.clipboard.writeText(content);
  };

  return (
    <div className="flex flex-col h-screen bg-background">
      {/* Header */}
      <header className="flex items-center justify-between px-6 py-4 border-b border-white/5">
        <div className="flex items-center gap-4">
          <Button variant="ghost" size="icon">
            <ArrowLeft className="w-5 h-5" />
          </Button>
          <div className="flex items-center gap-3">
            <Avatar size="md">
              <AvatarFallback className="bg-gradient-to-br from-violet-500 to-fuchsia-500">
                <Bot className="w-5 h-5" />
              </AvatarFallback>
            </Avatar>
            <div>
              <h1 className="font-semibold">AI Assistant</h1>
              <div className="flex items-center gap-2">
                <div className="w-2 h-2 rounded-full bg-green-500" />
                <span className="text-sm text-muted-foreground">Online</span>
              </div>
            </div>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <Button variant="ghost" size="icon">
            <Search className="w-5 h-5" />
          </Button>
          <Button variant="ghost" size="icon">
            <Settings className="w-5 h-5" />
          </Button>
          <Button variant="ghost" size="icon">
            <MoreVertical className="w-5 h-5" />
          </Button>
        </div>
      </header>

      {/* Messages */}
      <main className="flex-1 overflow-y-auto p-6">
        <div className="max-w-3xl mx-auto space-y-6">
          {messages.map((message, index) => (
            <motion.div
              key={message.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1 }}
              className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div className={`flex gap-3 max-w-[80%] ${message.role === 'user' ? 'flex-row-reverse' : ''}`}>
                {message.role !== 'user' && (
                  <Avatar size="sm" className="mt-1">
                    <AvatarFallback className="bg-gradient-to-br from-violet-500 to-fuchsia-500">
                      <Bot className="w-4 h-4" />
                    </AvatarFallback>
                  </Avatar>
                )}
                
                <div className="relative group">
                  <div className={`p-4 rounded-2xl ${
                    message.role === 'user'
                      ? 'bg-gradient-to-br from-violet-600 to-fuchsia-600 text-white'
                      : 'bg-white/5 border border-white/10'
                  }`}>
                    <p className="whitespace-pre-wrap">{message.content}</p>
                  </div>
                  
                  {/* Message Actions */}
                  <div className={`absolute top-2 ${message.role === 'user' ? 'left-2' : 'right-2'} opacity-0 group-hover:opacity-100 transition-opacity flex gap-1`}>
                    <Button variant="ghost" size="icon" className="h-8 w-8" onClick={() => copyMessage(message.content)}>
                      <Copy className="w-4 h-4" />
                    </Button>
                    <Button variant="ghost" size="icon" className="h-8 w-8">
                      <Edit2 className="w-4 h-4" />
                    </Button>
                    <Button variant="ghost" size="icon" className="h-8 w-8 text-red-400 hover:text-red-300">
                      <Trash2 className="w-4 h-4" />
                    </Button>
                  </div>
                  
                  <p className="text-xs text-muted-foreground mt-1 px-1">
                    {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                  </p>
                </div>
              </div>
            </motion.div>
          ))}

          {/* Loading State */}
          {isLoading && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="flex justify-start"
            >
              <div className="flex gap-3">
                <Avatar size="sm">
                  <AvatarFallback className="bg-gradient-to-br from-violet-500 to-fuchsia-500">
                    <Bot className="w-4 h-4" />
                  </AvatarFallback>
                </Avatar>
                <div className="p-4 rounded-2xl bg-white/5 border border-white/10">
                  <div className="flex items-center gap-2">
                    <Loader2 className="w-4 h-4 animate-spin text-violet-400" />
                    <span className="text-muted-foreground">Thinking...</span>
                  </div>
                </div>
              </div>
            </motion.div>
          )}

          {/* Suggestions */}
          <AnimatePresence>
            {showSuggestions && messages.length === 1 && (
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                className="flex flex-wrap gap-2 justify-center"
              >
                {suggestions.map((suggestion, index) => (
                  <Button
                    key={index}
                    variant="outline"
                    size="sm"
                    className="glass"
                    onClick={() => handleSuggestionClick(suggestion)}
                  >
                    <Sparkles className="w-4 h-4 mr-2 text-violet-400" />
                    {suggestion}
                  </Button>
                ))}
              </motion.div>
            )}
          </AnimatePresence>

          <div ref={messagesEndRef} />
        </div>
      </main>

      {/* Input Area */}
      <footer className="p-6 border-t border-white/5">
        <div className="max-w-3xl mx-auto">
          <form onSubmit={(e) => { e.preventDefault(); handleSend(); }} className="relative">
            <Input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask me anything..."
              className="pr-12 h-12 bg-white/5 border-white/10 focus:border-violet-500"
              disabled={isLoading}
            />
            <Button
              type="submit"
              size="icon"
              variant="gradient"
              className="absolute right-2 top-1/2 -translate-y-1/2"
              disabled={!input.trim() || isLoading}
            >
              {isLoading ? (
                <Loader2 className="w-4 h-4 animate-spin" />
              ) : (
                <Send className="w-4 h-4" />
              )}
            </Button>
          </form>
          
          <p className="text-xs text-muted-foreground text-center mt-3">
            AI Nexus uses AI. Always verify important information.
          </p>
        </div>
      </footer>
    </div>
  );
}