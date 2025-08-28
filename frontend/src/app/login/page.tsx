'use client'

import { useState } from 'react'

export default function Login() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    console.log('Login attempt:', { email, password })
  }

  return (
    <div className="scanlines min-h-screen flex items-center justify-center p-4">
      <div className="pixel-border bg-black/80 backdrop-blur-sm rounded-lg p-8 w-full max-w-md">
        <div className="text-center mb-8">
          <h1 className="neon-glow text-3xl font-bold mb-2">Kids Pixel Pals</h1>
          <p className="text-gray-300">Welcome back! Please sign in to continue</p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label htmlFor="email" className="block text-sm font-medium text-gray-300 mb-2">
              Email Address
            </label>
            <input
              id="email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full px-4 py-3 bg-gray-900 border-2 border-neon-pink text-white rounded-md focus:outline-none focus:ring-2 focus:ring-neon-pink focus:border-transparent"
              placeholder="Enter your email"
              required
              aria-required="true"
            />
          </div>

          <div>
            <label htmlFor="password" className="block text-sm font-medium text-gray-300 mb-2">
              Password
            </label>
            <input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full px-4 py-3 bg-gray-900 border-2 border-neon-pink text-white rounded-md focus:outline-none focus:ring-2 focus:ring-neon-pink focus:border-transparent"
              placeholder="Enter your password"
              required
              aria-required="true"
            />
          </div>

          <button
            type="submit"
            className="pixel-button w-full py-3 text-lg font-semibold"
            aria-label="Sign in to your account"
          >
            Sign In
          </button>
        </form>

        <div className="mt-6 text-center">
          <p className="text-gray-400">
            Don't have an account?{' '}
            <a href="/register" className="text-neon-pink hover:underline font-semibold">
              Sign up here
            </a>
          </p>
        </div>

        <div className="mt-8 p-4 bg-gray-900/50 rounded-md">
          <p className="text-xs text-gray-400 text-center">
            Demo credentials: test@example.com / password123
          </p>
        </div>
      </div>
    </div>
  )
}