'use client'

import { useState, useEffect, useRef } from 'react'

// WebSocket connection utility
class WebSocketService {
  private ws: WebSocket | null = null
  private reconnectAttempts = 0
  private maxReconnectAttempts = 5

  connect(url: string, onMessage: (data: any) => void, onOpen?: () => void, onClose?: () => void) {
    this.ws = new WebSocket(url)
    
    this.ws.onopen = () => {
      this.reconnectAttempts = 0
      onOpen?.()
    }
    
    this.ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data)
        onMessage(data)
      } catch (error) {
        console.error('Failed to parse WebSocket message:', error)
      }
    }
    
    this.ws.onclose = () => {
      onClose?.()
      this.attemptReconnect(url, onMessage, onOpen, onClose)
    }
    
    this.ws.onerror = (error) => {
      console.error('WebSocket error:', error)
    }
  }

  private attemptReconnect(url: string, onMessage: (data: any) => void, onOpen?: () => void, onClose?: () => void) {
    if (this.reconnectAttempts < this.maxReconnectAttempts) {
      this.reconnectAttempts++
      setTimeout(() => {
        this.connect(url, onMessage, onOpen, onClose)
      }, 1000 * this.reconnectAttempts)
    }
  }

  send(data: any) {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify(data))
    }
  }

  close() {
    this.ws?.close()
    this.ws = null
  }
}

interface Message {
  id: string
  sender: string
  content: string
  timestamp: Date
  isOwn: boolean
}

interface User {
  id: string
  name: string
  isOnline: boolean
  avatar: string
}

export default function ChatInterface() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      sender: 'PixelBot',
      content: 'Welcome to Kids Pixel Pals! 👋 Start chatting with your friends!',
      timestamp: new Date(),
      isOwn: false
    }
  ])
  const [newMessage, setNewMessage] = useState('')
  const [onlineUsers, setOnlineUsers] = useState<User[]>([
    { id: '1', name: 'PixelKid123', isOnline: true, avatar: '👾' },
    { id: '2', name: 'GameMaster', isOnline: true, avatar: '🦄' },
    { id: '3', name: 'StarGazer', isOnline: false, avatar: '🌟' }
  ])
  const [typingUsers, setTypingUsers] = useState<string[]>([])
  const [isConnected, setIsConnected] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const wsServiceRef = useRef<WebSocketService | null>(null)
  const typingTimeoutRef = useRef<NodeJS.Timeout | null>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    // Initialize WebSocket connection
    const wsService = new WebSocketService()
    wsServiceRef.current = wsService
    
    // For demo purposes - in production, use actual authentication token
    const wsUrl = 'ws://localhost:8000/ws/chat?token=demo-token'
    
    wsService.connect(wsUrl, 
      (data) => {
        switch (data.type) {
          case 'message':
            setMessages(prev => [...prev, {
              id: data.id,
              sender: data.sender_display_name,
              content: data.content,
              timestamp: new Date(data.timestamp),
              isOwn: data.sender_id === 'current-user-id' // Replace with actual user ID
            }])
            break
          case 'typing':
            if (data.is_typing) {
              setTypingUsers(prev => [...prev.filter(u => u !== data.user_display_name), data.user_display_name])
            } else {
              setTypingUsers(prev => prev.filter(u => u !== data.user_display_name))
            }
            break
          case 'online':
            setOnlineUsers(prev => prev.map(user => 
              user.id === data.user_id ? { ...user, isOnline: data.is_online } : user
            ))
            break
        }
      },
      () => setIsConnected(true),
      () => setIsConnected(false)
    )
    
    return () => {
      wsService.close()
    }
  }, [])

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const handleTyping = () => {
    if (wsServiceRef.current) {
      wsServiceRef.current.send({
        type: 'typing',
        conversation_id: 'demo-conversation', // Replace with actual conversation ID
        is_typing: true
      })
      
      // Clear previous timeout
      if (typingTimeoutRef.current) {
        clearTimeout(typingTimeoutRef.current)
      }
      
      // Set timeout to stop typing indicator
      typingTimeoutRef.current = setTimeout(() => {
        wsServiceRef.current?.send({
          type: 'typing',
          conversation_id: 'demo-conversation',
          is_typing: false
        })
      }, 2000)
    }
  }

  const handleSendMessage = () => {
    if (newMessage.trim() && wsServiceRef.current) {
      // Send message via WebSocket
      wsServiceRef.current.send({
        type: 'message',
        conversation_id: 'demo-conversation', // Replace with actual conversation ID
        content: newMessage.trim()
      })
      
      // Add message locally for immediate feedback
      const message: Message = {
        id: Date.now().toString(),
        sender: 'You',
        content: newMessage.trim(),
        timestamp: new Date(),
        isOwn: true
      }
      setMessages([...messages, message])
      setNewMessage('')
    }
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    handleTyping() // Send typing indicator on key press
    
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSendMessage()
    }
  }

  return (
    <div className="flex h-screen bg-gray-900">
      {/* Online Users Sidebar - Hidden on mobile */}
      <div className="hidden md:block w-64 bg-gray-800 border-r-2 border-neon-pink p-4">
        <h2 className="text-neon-pink font-bold text-lg mb-4 pixel-border p-2 text-center">
          Online Friends
        </h2>
        <div className="space-y-2">
          {onlineUsers.map((user) => (
            <div
              key={user.id}
              className="flex items-center p-2 bg-gray-700/50 rounded pixel-border"
            >
              <div className="relative">
                <span className="text-2xl">{user.avatar}</span>
                <div
                  className={`absolute -top-1 -right-1 w-3 h-3 rounded-full border-2 border-gray-800 ${
                    user.isOnline ? 'bg-green-400' : 'bg-gray-400'
                  }`}
                />
              </div>
              <div className="ml-3">
                <p className="text-sm font-medium text-white">{user.name}</p>
                <p className={`text-xs ${user.isOnline ? 'text-green-300' : 'text-gray-400'}`}>
                  {user.isOnline ? 'Online' : 'Offline'}
                </p>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col">
        {/* Chat Header with mobile menu button */}
        <div className="bg-gray-800 p-4 border-b-2 border-neon-pink flex justify-between items-center">
          <div>
            <h1 className="text-neon-pink font-bold text-xl neon-glow">Pixel Chat</h1>
            <p className="text-gray-300 text-sm">Safe messaging for kids</p>
          </div>
          <button className="md:hidden pixel-button p-2">
            <span className="text-neon-pink">👥</span>
          </button>
        </div>

        {/* Messages Container */}
        <div className="flex-1 overflow-y-auto p-4 space-y-3 bg-gray-900/50">
          {messages.map((message) => (
            <div
              key={message.id}
              className={`flex ${message.isOwn ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`max-w-xs p-3 rounded-lg ${
                  message.isOwn
                    ? 'bg-neon-pink text-white'
                    : 'bg-gray-700 text-gray-200'
                } pixel-border`}
                style={{ imageRendering: 'pixelated' }}
              >
                {!message.isOwn && (
                  <p className="text-xs font-bold text-neon-pink mb-1">
                    {message.sender}
                  </p>
                )}
                <p className="text-sm break-words">{message.content}</p>
                <p className="text-xs opacity-70 mt-1">
                  {message.timestamp.toLocaleTimeString([], { 
                    hour: '2-digit', 
                    minute: '2-digit' 
                  })}
                </p>
              </div>
            </div>
          ))}
          
          {/* Typing Indicator */}
          {typingUsers.length > 0 && (
            <div className="flex justify-start">
              <div className="bg-gray-700 text-gray-200 p-3 rounded-lg pixel-border max-w-xs">
                <div className="flex items-center space-x-2">
                  <div className="flex space-x-1">
                    <div className="w-2 h-2 bg-neon-pink rounded-full animate-bounce" style={{animationDelay: '0ms'}}></div>
                    <div className="w-2 h-2 bg-neon-pink rounded-full animate-bounce" style={{animationDelay: '150ms'}}></div>
                    <div className="w-2 h-2 bg-neon-pink rounded-full animate-bounce" style={{animationDelay: '300ms'}}></div>
                  </div>
                  <span className="text-xs text-neon-pink">
                    {typingUsers.join(', ')} {typingUsers.length === 1 ? 'is' : 'are'} typing...
                  </span>
                </div>
              </div>
            </div>
          )}
          
          <div ref={messagesEndRef} />
        </div>

        {/* Message Input */}
        <div className="bg-gray-800 p-4 border-t-2 border-neon-pink">
          <div className="flex space-x-2">
            <input
              type="text"
              value={newMessage}
              onChange={(e) => setNewMessage(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Type a message..."
              className="flex-1 p-2 bg-gray-700 text-white border-2 border-neon-pink rounded pixel-button focus:outline-none focus:ring-2 focus:ring-neon-pink text-sm md:text-base"
              maxLength={200}
            />
            <button
              onClick={handleSendMessage}
              disabled={!newMessage.trim() || !isConnected}
              className="pixel-button bg-neon-pink hover:bg-neon-pink/90 disabled:opacity-50 disabled:cursor-not-allowed px-4"
            >
              {isConnected ? 'Send' : 'Connecting...'}
            </button>
          </div>
          <div className="flex items-center justify-between mt-2">
            <p className="text-xs text-gray-400">
              Messages are moderated for safety
            </p>
            <div className="flex items-center space-x-2">
              <div className={`w-2 h-2 rounded-full ${isConnected ? 'bg-green-400' : 'bg-red-400'}`}></div>
              <span className="text-xs text-gray-400">
                {isConnected ? 'Connected' : 'Disconnected'}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}