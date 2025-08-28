'use client'

import { useState } from 'react'

export default function Register() {
  const [formData, setFormData] = useState({
    firstName: '',
    lastName: '',
    email: '',
    password: '',
    confirmPassword: '',
    age: '',
    parentEmail: ''
  })

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData(prev => ({
      ...prev,
      [e.target.name]: e.target.value
    }))
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    console.log('Registration attempt:', formData)
  }

  return (
    <div className="scanlines min-h-screen flex items-center justify-center p-4">
      <div className="pixel-border bg-black/80 backdrop-blur-sm rounded-lg p-8 w-full max-w-md">
        <div className="text-center mb-8">
          <h1 className="neon-glow text-3xl font-bold mb-2">Join Pixel Pals!</h1>
          <p className="text-gray-300">Create your account to start the adventure</p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label htmlFor="firstName" className="block text-sm font-medium text-gray-300 mb-2">
                First Name
              </label>
              <input
                id="firstName"
                name="firstName"
                type="text"
                value={formData.firstName}
                onChange={handleChange}
                className="w-full px-4 py-3 bg-gray-900 border-2 border-neon-pink text-white rounded-md focus:outline-none focus:ring-2 focus:ring-neon-pink focus:border-transparent"
                placeholder="First name"
                required
                aria-required="true"
              />
            </div>

            <div>
              <label htmlFor="lastName" className="block text-sm font-medium text-gray-300 mb-2">
                Last Name
              </label>
              <input
                id="lastName"
                name="lastName"
                type="text"
                value={formData.lastName}
                onChange={handleChange}
                className="w-full px-4 py-3 bg-gray-900 border-2 border-neon-pink text-white rounded-md focus:outline-none focus:ring-2 focus:ring-neon-pink focus:border-transparent"
                placeholder="Last name"
                required
                aria-required="true"
              />
            </div>
          </div>

          <div>
            <label htmlFor="email" className="block text-sm font-medium text-gray-300 mb-2">
              Email Address
            </label>
            <input
              id="email"
              name="email"
              type="email"
              value={formData.email}
              onChange={handleChange}
              className="w-full px-4 py-3 bg-gray-900 border-2 border-neon-pink text-white rounded-md focus:outline-none focus:ring-2 focus:ring-neon-pink focus:border-transparent"
              placeholder="Enter your email"
              required
              aria-required="true"
            />
          </div>

          <div>
            <label htmlFor="age" className="block text-sm font-medium text-gray-300 mb-2">
              Age
            </label>
            <input
              id="age"
              name="age"
              type="number"
              value={formData.age}
              onChange={handleChange}
              className="w-full px-4 py-3 bg-gray-900 border-2 border-neon-pink text-white rounded-md focus:outline-none focus:ring-2 focus:ring-neon-pink focus:border-transparent"
              placeholder="Enter your age"
              min="5"
              max="18"
              required
              aria-required="true"
            />
          </div>

          <div>
            <label htmlFor="parentEmail" className="block text-sm font-medium text-gray-300 mb-2">
              Parent's Email
            </label>
            <input
              id="parentEmail"
              name="parentEmail"
              type="email"
              value={formData.parentEmail}
              onChange={handleChange}
              className="w-full px-4 py-3 bg-gray-900 border-2 border-neon-pink text-white rounded-md focus:outline-none focus:ring-2 focus:ring-neon-pink focus:border-transparent"
              placeholder="Parent's email for approval"
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
              name="password"
              type="password"
              value={formData.password}
              onChange={handleChange}
              className="w-full px-4 py-3 bg-gray-900 border-2 border-neon-pink text-white rounded-md focus:outline-none focus:ring-2 focus:ring-neon-pink focus:border-transparent"
              placeholder="Create a password"
              required
              aria-required="true"
            />
          </div>

          <div>
            <label htmlFor="confirmPassword" className="block text-sm font-medium text-gray-300 mb-2">
              Confirm Password
            </label>
            <input
              id="confirmPassword"
              name="confirmPassword"
              type="password"
              value={formData.confirmPassword}
              onChange={handleChange}
              className="w-full px-4 py-3 bg-gray-900 border-2 border-neon-pink text-white rounded-md focus:outline-none focus:ring-2 focus:ring-neon-pink focus:border-transparent"
              placeholder="Confirm your password"
              required
              aria-required="true"
            />
          </div>

          <button
            type="submit"
            className="pixel-button w-full py-3 text-lg font-semibold mt-6"
            aria-label="Create your account"
          >
            Create Account
          </button>
        </form>

        <div className="mt-6 text-center">
          <p className="text-gray-400">
            Already have an account?{' '}
            <a href="/login" className="text-neon-pink hover:underline font-semibold">
              Sign in here
            </a>
          </p>
        </div>

        <div className="mt-8 p-4 bg-gray-900/50 rounded-md">
          <p className="text-xs text-gray-400 text-center">
            Parental approval required for accounts under 13 years old
          </p>
        </div>
      </div>
    </div>
  )
}