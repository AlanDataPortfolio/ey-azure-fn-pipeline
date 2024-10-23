export default function LandingPage() {
    return (
      <div className="bg-nrmaBlue min-h-screen flex items-center justify-center">
        <div className="bg-white shadow-xl rounded-lg p-8 max-w-4xl mx-auto">
          <div className="text-center">
            <img src="/NRMA_logo.png" alt="NRMA Logo" className="h-16 mx-auto mb-4" />
            <h1 className="text-3xl font-bold text-nrmaBlue mb-8">Number of Claims to Check: #</h1>
            <button
              className="w-full md:w-auto px-8 py-3 bg-gradient-to-r from-blue-500 to-blue-700 text-white font-semibold rounded-full shadow-lg hover:shadow-2xl transition transform hover:-translate-y-1"
              onClick={() => window.location.href = '/login'} // Redirect to login
            >
              Review Car Insurance Claims
            </button>
          </div>
        </div>
      </div>
    );
  }
  