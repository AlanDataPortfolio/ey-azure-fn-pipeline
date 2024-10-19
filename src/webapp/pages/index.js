import { useState, useEffect } from 'react';
import { useRouter } from 'next/router';

export default function Home() {
  const [claimDetails, setClaimDetails] = useState('');
  const [fraudScore, setFraudScore] = useState('');
  const [fraudAnalysis, setFraudAnalysis] = useState('');
  const [claimOutcome, setClaimOutcome] = useState('pending');
  const [claimNotes, setClaimNotes] = useState('');
  const [claimDescription, setClaimDescription] = useState('');
  const [claimId, setClaimId] = useState(null);
  const [searchClaimId, setSearchClaimId] = useState('');
  const router = useRouter();

  useEffect(() => {
    const isLoggedIn = localStorage.getItem('loggedIn');
    if (!isLoggedIn) {
      router.push('/login'); // Redirect to login page if not logged in
    }
  }, []);

  const handleLogout = () => {
    localStorage.removeItem('loggedIn'); // Remove login session
    router.push('/login'); // Redirect to login page
  };

  const getFirstOpenClaim = async () => {
    try {
      const response = await fetch('/api/getClaim');
      const data = await response.json();
      if (response.ok) {
        populateClaimDetails(data);
        alert('First open/pending claim fetched successfully');
      } else {
        alert(data.message);
      }
    } catch (error) {
      console.error('Error fetching first open/pending claim:', error);
      alert('An error occurred while fetching the claim');
    }
  };

  const getClaimById = async () => {
    if (!searchClaimId) {
      alert('Please enter a Claim ID');
      return;
    }

    try {
      const response = await fetch(`/api/getClaim?claimId=${searchClaimId}`);
      const data = await response.json();
      if (response.ok) {
        populateClaimDetails(data);
        alert(`Claim ${searchClaimId} fetched successfully`);
      } else {
        alert(data.message);
      }
    } catch (error) {
      console.error('Error fetching claim by ID:', error);
      alert('An error occurred while fetching the claim');
    }
  };

  const checkFraud = async () => {
    if (!claimId) {
      alert('No claim selected to analyze for fraud');
      return;
    }

    try {
      const response = await fetch('/api/checkFraud', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ claimId }),
      });
      const data = await response.json();
      if (response.ok) {
        setFraudScore(data.fraudChance || 'N/A');
        setFraudAnalysis(data.fraudAnalysis || 'N/A');
        alert('Fraud analysis completed successfully');
      } else {
        alert(data.message);
      }
    } catch (error) {
      console.error('Error performing fraud analysis:', error);
      alert('An error occurred while performing fraud analysis');
    }
  };

  const populateClaimDetails = (data) => {
    setClaimId(data.claimID);
    setClaimDetails(
      `Claim ID: ${data.claimID}\n` +
        `First Name: ${data.firstName}\n` +
        `Last Name: ${data.lastName}\n` +
        `Claim Status: ${data.claimStatus}\n` +
        `Claim Outcome: ${data.claimOutcome}\n` +
        `Time as Customer: ${data.timeAsCustomer}\n` +
        `Driver Age: ${data.driverAge}\n` +
        `Insurance Access: ${data.insuranceAccess}\n` +
        `Insurance Premium: ${data.insurancePremium}\n` +
        `Driver Gender: ${data.driverGender}\n` +
        `Education Level: ${data.educationLevel}\n` +
        `Accident Type: ${data.accidentType}\n` +
        `Incident Severity: ${data.incidentSeverity}\n` +
        `Authorities Involved: ${data.authoritiesInvolved}\n` +
        `Incident Time: ${data.incidentTime}\n` +
        `Num Vehicles Involved: ${data.numVehiclesInvolved}\n` +
        `Num Bodily Injuries: ${data.numBodilyInjuries}\n` +
        `Police Report: ${data.policeReportBool}\n` +
        `Total Claim Amount: ${data.totalClaimAmount}\n` +
        `Vehicle Age: ${data.vehicleAge}\n` +
        `Driver Experience: ${data.driverExperience}\n` +
        `License Type: ${data.licenseType}\n`
    );
    setClaimOutcome(data.claimOutcome || 'pending');
    setClaimDescription(data.claimDescription || 'No description provided');
    setFraudScore(data.fraudChance || 'N/A');
    setFraudAnalysis(data.fraudAnalysis || 'N/A');
    setClaimNotes(data.claimNotes || 'No notes available');
  };

  const closeCase = async () => {
    if (!claimId) {
      alert('No claim selected to close');
      return;
    }

    let updatedClaimStatus = 'open';
    if (claimOutcome === 'approved' || claimOutcome === 'denied') {
      updatedClaimStatus = 'closed'; // Only close the case if approved or denied
    }

    try {
      const response = await fetch('/api/updateClaim', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          claimId,
          claimStatus: updatedClaimStatus,
          claimOutcome,
          claimNotes,
          fraudChance: fraudScore,
          fraudAnalysis,
        }),
      });

      if (response.ok) {
        alert('Claim closed successfully');
        clearFields();
      } else {
        alert('Error closing the claim');
      }
    } catch (error) {
      console.error('Error closing the claim:', error);
      alert('An error occurred while closing the claim');
    }
  };

  const escalateClaim = async () => {
    if (!claimId) {
      alert('No claim selected to escalate');
      return;
    }

    try {
      const response = await fetch('/api/updateClaim', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          claimId,
          claimStatus: 'open',
          claimOutcome: 'escalated',
          claimNotes,
          fraudChance: fraudScore,
          fraudAnalysis,
        }),
      });

      if (response.ok) {
        alert('Claim escalated to manager');
        clearFields();
      } else {
        alert('Error escalating the claim');
      }
    } catch (error) {
      console.error('Error escalating the claim:', error);
      alert('An error occurred while escalating the claim');
    }
  };

  const clearFields = () => {
    setClaimDetails('');
    setClaimOutcome('pending');
    setClaimNotes('');
    setFraudScore('');
    setFraudAnalysis('');
    setClaimDescription('');
    setClaimId(null);
    setSearchClaimId('');
  };

  return (
    <div className="bg-nrmaBlue min-h-screen">
      {/* Header */}
      <header className="bg-white shadow-md">
        <div className="max-w-7xl mx-auto px-6 py-4 flex justify-between items-center">
          <div className="flex items-center">
            <img src="/nrma-logo.png" alt="NRMA Logo" className="h-12 w-auto" />
            <h1 className="text-2xl font-bold text-nrmaBlue ml-4">
              Insurance Claim Processing
            </h1>
          </div>
          <button
            onClick={handleLogout}
            className="px-4 py-2 bg-red-500 text-white rounded-md hover:bg-red-600 transition"
          >
            Logout
          </button>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-6 py-8">
        {/* Claim Search Section */}
        <div className="bg-white shadow-md rounded-lg p-6 mb-8">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <button
              type="button"
              onClick={getFirstOpenClaim}
              className="w-full md:w-auto mb-4 md:mb-0 px-6 py-2 bg-nrmaBlue text-white font-semibold rounded-md shadow hover:bg-blue-700 transition"
            >
              Get First Open Claim
            </button>

            <div className="flex w-full md:w-auto items-center space-x-2">
              <input
                type="text"
                id="searchClaimId"
                name="searchClaimId"
                value={searchClaimId}
                onChange={(e) => setSearchClaimId(e.target.value)}
                placeholder="Enter Claim ID"
                className="input-field p-2 border rounded-md w-full md:w-64"
              />
              <button
                type="button"
                onClick={getClaimById}
                className="px-6 py-2 bg-nrmaBlue text-white font-semibold rounded-md shadow hover:bg-blue-700 transition"
              >
                Search
              </button>
            </div>
          </div>
        </div>

        {/* Main Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Left Column */}
          <div className="lg:col-span-2 space-y-8">
            {/* Claim Information */}
            <div className="bg-white shadow-md rounded-lg p-6">
              <h2 className="text-xl font-semibold text-nrmaBlue mb-4">
                Claim Information
              </h2>
              <div className="grid grid-cols-2 gap-4 max-h-64 overflow-y-auto">
                {claimDetails &&
                  claimDetails.split('\n').map((line, index) => {
                    const [key, value] = line.split(':');
                    if (key && value) {
                      return (
                        <div key={index} className="flex">
                          <span className="font-semibold">{key.trim()}:</span>&nbsp;
                          <span>{value.trim()}</span>
                        </div>
                      );
                    } else {
                      return null;
                    }
                  })}
              </div>
            </div>

            {/* Fraud Analysis */}
            <div className="bg-white shadow-md rounded-lg p-6">
              <h2 className="text-xl font-semibold text-nrmaBlue mb-4">
                Fraud Analysis
              </h2>
              <div className="mb-4">
                <label
                  htmlFor="fraudScore"
                  className="block text-sm font-medium text-gray-700 mb-1"
                >
                  Fraud Risk Score (%)
                </label>
                <input
                  type="text"
                  id="fraudScore"
                  name="fraudScore"
                  value={fraudScore}
                  placeholder="Auto-filled by AI"
                  className="input-field w-full p-3 border rounded-md"
                  readOnly
                />
              </div>
              <div className="relative">
                <label
                  htmlFor="fraudAnalysis"
                  className="block text-sm font-medium text-gray-700 mb-1"
                >
                  Fraud Analysis Summary
                </label>
                <textarea
                  id="fraudAnalysis"
                  name="fraudAnalysis"
                  value={fraudAnalysis}
                  placeholder="Auto-filled by AI"
                  className="input-field w-full h-32 p-3 border rounded-md"
                  readOnly
                />
                <button
                  type="button"
                  className="absolute right-4 bottom-4 px-3 py-2 bg-orange-500 text-white rounded-md shadow hover:bg-orange-600 transition"
                  onClick={() => alert('Detailed explanation coming soon!')}
                >
                  Explain More
                </button>
              </div>
              <button
                type="button"
                onClick={checkFraud}
                className="mt-4 w-full px-6 py-2 bg-purple-600 text-white font-semibold rounded-md shadow hover:bg-purple-700 transition"
              >
                Check Fraud
              </button>
            </div>
          </div>

          {/* Right Column */}
          <div className="space-y-8">
            {/* Claim Description */}
            <div className="bg-white shadow-md rounded-lg p-6">
              <h2 className="text-xl font-semibold text-nrmaBlue mb-4">
                Claim Description
              </h2>
              <textarea
                id="claimDescription"
                name="claimDescription"
                value={claimDescription}
                placeholder="Description of the claim"
                className="input-field w-full h-32 p-3 border rounded-md"
                readOnly
              />
            </div>

            {/* Claim Notes */}
            <div className="bg-white shadow-md rounded-lg p-6">
              <h2 className="text-xl font-semibold text-nrmaBlue mb-4">
                Claim Processing Notes
              </h2>
              <textarea
                id="claimNotes"
                name="claimNotes"
                value={claimNotes}
                onChange={(e) => setClaimNotes(e.target.value)}
                placeholder="Add or update claim processing notes"
                className="input-field w-full h-32 p-3 border rounded-md"
              />
            </div>

            {/* Claim Outcome */}
            <div className="bg-white shadow-md rounded-lg p-6">
              <label
                htmlFor="claimOutcome"
                className="block text-sm font-medium text-gray-700 mb-2"
              >
                Claim Outcome
              </label>
              <select
                id="claimOutcome"
                name="claimOutcome"
                value={claimOutcome}
                onChange={(e) => setClaimOutcome(e.target.value)}
                className="input-field w-full p-3 border rounded-md"
              >
                <option value="pending">Pending</option>
                <option value="escalated">Escalated</option>
                <option value="approved">Approved</option>
                <option value="denied">Denied</option>
              </select>
            </div>

            {/* Action Buttons */}
            <div className="flex flex-col space-y-4">
              <button
                type="button"
                onClick={closeCase}
                className="w-full px-6 py-3 bg-green-600 text-white font-semibold rounded-md shadow hover:bg-green-700 transition"
              >
                Close Case
              </button>
              <button
                type="button"
                onClick={escalateClaim}
                className="w-full px-6 py-3 bg-yellow-500 text-white font-semibold rounded-md shadow hover:bg-yellow-600 transition"
              >
                Escalate to Manager
              </button>
            </div>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-white shadow-inner mt-12">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <p className="text-center text-sm text-gray-500">
            Developed by Macquarie University's Team 14 Data Team for EY & NRMA. Chief Developer:
            Noorullah Khan
          </p>
        </div>
      </footer>
    </div>
  );
}
