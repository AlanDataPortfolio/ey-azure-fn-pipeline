// pages/landingPage.js

import { useState, useEffect } from 'react';
import { useRouter } from 'next/router';

export default function LandingPage() {
  const [currentClaimsCount, setCurrentClaimsCount] = useState(0);
  const router = useRouter();

  useEffect(() => {
    const isLoggedIn = localStorage.getItem('loggedIn');
    if (!isLoggedIn) {
      router.push('/login'); // Redirect to login page if not logged in
    } else {
      // Fetch the number of open & pending claims
      fetchCurrentClaimsCount();
    }
  }, []);

  const fetchCurrentClaimsCount = async () => {
    try {
      const response = await fetch('/api/getOpenClaimsCount'); // Assuming this endpoint exists
      const data = await response.json();
      if (response.ok) {
        setCurrentClaimsCount(data.count);
      } else {
        console.error('Failed to fetch claims count');
      }
    } catch (error) {
      console.error('Error fetching claims count:', error);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('loggedIn'); // Remove login session
    router.push('/login'); // Redirect to login page
  };

  return (
    <div className="bg-gray-100 min-h-screen">
      {/* Header */}
      <header className="bg-white shadow-md">
        <div className="max-w-7xl mx-auto px-6 py-4 flex justify-between items-center">
          {/* Logo */}
          <div className="flex items-center">
            <img src="/NRMA_logo2.png" alt="NRMA Logo" className="h-16 w-auto" />
          </div>

          {/* Search Box */}
          <div className="flex items-center flex-1 justify-center">
            <div className="relative w-full max-w-md">
              <input
                type="text"
                placeholder="Search NRMA..."
                className="p-2 border rounded-full w-full focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
              <button className="absolute right-2 top-1/2 transform -translate-y-1/2">
                <img src="/search_icon.png" alt="Search" className="h-5 w-5" />
              </button>
            </div>
          </div>

          {/* Profile and Account */}
          <div className="flex items-center space-x-4">
            <button
              className="flex items-center focus:outline-none"
              onClick={handleLogout}
            >
              <img src="/profile_icon.png" alt="Profile" className="h-8 w-8 rounded-full" />
            </button>
            <button
              className="px-4 py-2 bg-blue-600 text-white font-semibold rounded-full shadow-md hover:bg-blue-700 transition"
              onClick={() => alert('Account page coming soon!')}
            >
              Account
            </button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-6 py-8">
        {/* Number of Current Claims */}
        <div className="bg-white shadow-xl rounded-lg p-8 mb-8 text-center">
          <h1 className="text-3xl font-bold text-nrmaBlue mb-4">Number of Current Claims</h1>
          <p className="text-6xl font-bold text-gray-800">{currentClaimsCount}</p>
        </div>

        {/* Insurance Sections */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {/* Car Insurance Claims */}
          <div className="bg-white shadow-md rounded-lg p-6 text-center">
            <h2 className="text-xl font-bold text-nrmaBlue mb-4">Car Insurance Claims</h2>
            <button
              className="px-6 py-2 bg-blue-600 text-white font-semibold rounded-full shadow-md hover:bg-blue-700 transition"
              onClick={() => router.push('/')}
            >
              Review Claims
            </button>
          </div>

          {/* Home Insurance Claims */}
          <div className="bg-white shadow-md rounded-lg p-6 text-center">
            <h2 className="text-xl font-bold text-nrmaBlue mb-4">Home Insurance Claims</h2>
            <button
              className="px-6 py-2 bg-blue-600 text-white font-semibold rounded-full shadow-md hover:bg-blue-700 transition"
              onClick={() => alert('Home Insurance Claims coming soon!')}
            >
              Review Claims
            </button>
          </div>

          {/* CTP Insurance Claims */}
          <div className="bg-white shadow-md rounded-lg p-6 text-center">
            <h2 className="text-xl font-bold text-nrmaBlue mb-4">CTP Insurance Claims</h2>
            <button
              className="px-6 py-2 bg-blue-600 text-white font-semibold rounded-full shadow-md hover:bg-blue-700 transition"
              onClick={() => alert('CTP Insurance Claims coming soon!')}
            >
              Review Claims
            </button>
          </div>

          {/* Landlord Insurance Claims */}
          <div className="bg-white shadow-md rounded-lg p-6 text-center">
            <h2 className="text-xl font-bold text-nrmaBlue mb-4">Landlord Insurance Claims</h2>
            <button
              className="px-6 py-2 bg-blue-600 text-white font-semibold rounded-full shadow-md hover:bg-blue-700 transition"
              onClick={() => alert('Landlord Insurance Claims coming soon!')}
            >
              Review Claims
            </button>
          </div>

          {/* Travel Insurance Claims */}
          <div className="bg-white shadow-md rounded-lg p-6 text-center">
            <h2 className="text-xl font-bold text-nrmaBlue mb-4">Travel Insurance Claims</h2>
            <button
              className="px-6 py-2 bg-blue-600 text-white font-semibold rounded-full shadow-md hover:bg-blue-700 transition"
              onClick={() => alert('Travel Insurance Claims coming soon!')}
            >
              Review Claims
            </button>
          </div>

          {/* Boat Insurance Claims */}
          <div className="bg-white shadow-md rounded-lg p-6 text-center">
            <h2 className="text-xl font-bold text-nrmaBlue mb-4">Boat Insurance Claims</h2>
            <button
              className="px-6 py-2 bg-blue-600 text-white font-semibold rounded-full shadow-md hover:bg-blue-700 transition"
              onClick={() => alert('Boat Insurance Claims coming soon!')}
            >
              Review Claims
            </button>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-white shadow-inner">
        <div className="max-w-screen-2xl mx-auto px-4 py-4 flex items-center justify-center">
          <img src="/NRMA_logo.png" alt="NRMA Logo" className="h-8 w-auto mr-4" />
          <div className="text-center">
            <p className="text-sm text-gray-500 leading-tight">
              © {new Date().getFullYear()} EY & NRMA. All rights reserved. <br />
              Developed by{' '}
              <a
                href="https://www.linkedin.com/in/noorullah-khan"
                className="text-nrmaBlue hover:underline"
                target="_blank"
                rel="noopener noreferrer"
              >
                Noorullah Khan
              </a>{' '}
              for EY & NRMA.
            </p>
            <p className="text-xs text-gray-400 mt-1 leading-tight">
              The content and functionality of this site are confidential and proprietary to EY &
              NRMA.
            </p>
          </div>
          <img src="/NRMA_logo.png" alt="NRMA Logo" className="h-8 w-auto ml-4" />
        </div>
      </footer>
    </div>
  );
}
