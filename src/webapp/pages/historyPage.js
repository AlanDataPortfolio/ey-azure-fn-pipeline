// pages/historyPage.js

import { useState, useEffect } from 'react';
import { useRouter } from 'next/router';

export default function HistoryPage() {
  const [claims, setClaims] = useState([]);
  const router = useRouter();

  useEffect(() => {
    const isLoggedIn = localStorage.getItem('loggedIn');
    if (!isLoggedIn) {
      router.push('/login');
    } else {
      fetchClaims();
    }
  }, []);

  const handleLogout = () => {
    localStorage.removeItem('loggedIn');
    router.push('/login');
  };

  const handleAccount = () => {
    alert('Account page coming soon!');
  };

  const fetchClaims = async () => {
    try {
      const response = await fetch('/api/getHistoryClaims');
      const data = await response.json();
      if (response.ok) {
        setClaims(data.claims);
      } else {
        alert('Failed to fetch claims.');
      }
    } catch (error) {
      console.error('Error fetching claims:', error);
      alert('An error occurred while fetching claims.');
    }
  };

  const handleClaimClick = (claimID) => {
    router.push(`/?claimId=${claimID}`);
  };

  return (
    <div className="bg-gray-100 min-h-screen">
      {/* Header */}
      <header className="bg-white shadow-md">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex justify-between items-center">
            {/* Logo */}
            <div className="flex items-center">
              <button onClick={() => router.push('/landingPage')}>
                <img src="/NRMA_logo2.png" alt="NRMA Logo" className="h-16 w-auto" />
              </button>
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
                onClick={handleAccount}
              >
                Account
              </button>
            </div>
          </div>

          {/* Navigation Bar */}
          <nav className="mt-4">
            <div className="flex justify-center space-x-8">
              <a
                href="/landingPage"
                className="text-gray-700 hover:text-blue-600 font-medium"
              >
                Home
              </a>
              <a
                href="/historyPage"
                className="text-gray-700 hover:text-blue-600 font-medium"
              >
                Insights
              </a>
              <a
                href="#"
                className="text-gray-700 hover:text-blue-600 font-medium"
              >
                Support
              </a>
            </div>
          </nav>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-6 py-8">
        <div className="flex justify-between items-center mb-6">
          <h1 className="text-2xl font-bold text-nrmaBlue">Claims History</h1>
          <button
            onClick={fetchClaims}
            className="px-4 py-2 bg-blue-600 text-white font-semibold rounded-full shadow-md hover:bg-blue-700 transition"
          >
            Refresh
          </button>
        </div>
        <div className="bg-white shadow-md rounded-lg overflow-hidden">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th
                  scope="col"
                  className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                >
                  Claim ID
                </th>
                <th
                  scope="col"
                  className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                >
                  Claim Outcome
                </th>
                <th
                  scope="col"
                  className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                >
                  Claim Notes
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {claims.length > 0 ? (
                claims.map((claim) => (
                  <tr key={claim.claimID} className="hover:bg-gray-50 cursor-pointer">
                    <td
                      className="px-6 py-4 whitespace-nowrap text-sm text-blue-600 underline"
                      onClick={() => handleClaimClick(claim.claimID)}
                    >
                      {claim.claimID}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {claim.claimOutcome}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {claim.claimNotes}
                    </td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td
                    className="px-6 py-4 whitespace-nowrap text-sm text-gray-500"
                    colSpan="3"
                  >
                    No claims found.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-white shadow-inner">
        <div className="max-w-7xl mx-auto px-4 py-4 flex items-center justify-center">
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
