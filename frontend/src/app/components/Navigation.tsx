import Link from 'next/link'

export default function Navigation() {
  return (
    <nav className="pixel-border bg-black/80 backdrop-blur-sm p-4 mb-8">
      <div className="max-w-4xl mx-auto flex justify-between items-center">
        <Link href="/" className="neon-glow text-xl font-bold hover:text-neon-pink transition-colors">
          Kids Pixel Pals
        </Link>
        
        <div className="flex space-x-4">
          <Link 
            href="/login" 
            className="pixel-button px-4 py-2 text-sm hover:scale-105 transition-transform"
            aria-label="Sign in to your account"
          >
            Sign In
          </Link>
          
          <Link 
            href="/register" 
            className="pixel-button px-4 py-2 text-sm bg-neon-pink hover:bg-neon-pink/90 transition-colors"
            aria-label="Create a new account"
          >
            Sign Up
          </Link>
        </div>
      </div>
    </nav>
  )
}