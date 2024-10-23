import { useState } from 'react';
import { useRouter } from 'next/router';

export default function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [rememberMe, setRememberMe] = useState(false);
  const router = useRouter();

  const handleLogin = (e) => {
    e.preventDefault();

    // Simple authentication simulation
    if (email === 'noor@ey.com' && password === '123') {
      localStorage.setItem('loggedIn', true); // Store login state
      router.push('/'); // Redirect to the home page after login
    } else {
      alert('Invalid login credentials.');
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center">
      <div className="bg-white p-8 rounded-lg shadow-2xl max-w-md w-full relative">
        {/* Background circles (for design purpose) */}
        <div className="absolute -left-12 -top-12 w-40 h-40 bg-gradient-to-r from-blue-400 to-blue-600 rounded-full opacity-20"></div>
        <div className="absolute -right-12 -bottom-12 w-40 h-40 bg-gradient-to-r from-blue-400 to-blue-600 rounded-full opacity-20"></div>

        {/* Logo */}
        <div className="text-center mb-8">
          <img src="/NRMA_logo2.png" alt="NRMA Logo" className="h-16 w-auto mx-auto" />
          <h2 className="text-2xl font-bold text-gray-700 mt-4">Log in to your NRMA Insurance Online Account</h2>
          <p className="text-gray-500 text-sm mt-2">Log in with your NRMA email or Employee ID number</p>
        </div>

        {/* Form */}
        <form onSubmit={handleLogin}>
          <div className="mb-6">
            <label htmlFor="email" className="block text-gray-700 mb-1">NRMA email or Employee ID number</label>
            <input
              type="email"
              id="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full px-4 py-2 border rounded-full focus:outline-none focus:ring-2 focus:ring-blue-500"
              required
            />
          </div>

          <div className="mb-6">
            <label htmlFor="password" className="block text-gray-700 mb-1">Password</label>
            <input
              type="password"
              id="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full px-4 py-2 border rounded-full focus:outline-none focus:ring-2 focus:ring-blue-500"
              required
            />
          </div>

          <div className="flex items-center justify-between mb-6">
            <div className="flex items-center">
              <input
                type="checkbox"
                id="rememberMe"
                checked={rememberMe}
                onChange={() => setRememberMe(!rememberMe)}
                className="w-4 h-4 text-blue-500 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
              <label htmlFor="rememberMe" className="ml-2 text-gray-700">Remember me</label>
            </div>
            <a href="#" className="text-sm text-blue-600 hover:underline">Forgot password?</a>
          </div>

          <button
            type="submit"
            className="w-full py-3 bg-gradient-to-r from-blue-500 to-blue-700 text-white font-semibold rounded-full shadow-xl hover:shadow-2xl transition transform hover:-translate-y-1"
          >
            Log in
          </button>
        </form>

        <div className="text-center mt-8">
          <a href="#" className="text-sm text-blue-600 hover:underline">Having trouble logging in?</a>
        </div>
      </div>
    </div>
  );
}
