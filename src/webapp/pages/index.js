// pages/index.js

import { useState, useEffect } from 'react';
import { useRouter } from 'next/router';
import ReactMarkdown from 'react-markdown';
import remarkBreaks from 'remark-breaks';

export default function Home() {
  const [claimDetails, setClaimDetails] = useState({});
  const [fraudScore, setFraudScore] = useState('');
  const [fraudAnalysis, setFraudAnalysis] = useState('');
  const [claimOutcome, setClaimOutcome] = useState('pending');
  const [claimNotes, setClaimNotes] = useState('');
  const [claimDescription, setClaimDescription] = useState('');
  const [claimId, setClaimId] = useState(null);
  const [searchClaimId, setSearchClaimId] = useState('');
  const [customQuestion, setCustomQuestion] = useState('');
  const [customResponse, setCustomResponse] = useState('');
  const router = useRouter();

  useEffect(() => {
    const isLoggedIn = localStorage.getItem('loggedIn');
    if (!isLoggedIn) {
      router.push('/login');
    } else {
      const { claimId } = router.query;
      if (claimId) {
        // Fetch the claim by ID from query parameter
        fetchClaimById(claimId);
      }
    }
  }, [router.query]);

  const handleLogout = () => {
    localStorage.removeItem('loggedIn');
    router.push('/login');
  };

  const handleAccount = () => {
    alert('Account page coming soon!');
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
    fetchClaimById(searchClaimId);
  };

  const fetchClaimById = async (id) => {
    try {
      const response = await fetch(`/api/getClaim?claimId=${id}`);
      const data = await response.json();
      if (response.ok) {
        populateClaimDetails(data);
        alert(`Claim ${id} fetched successfully`);
      } else {
        alert(data.message);
      }
    } catch (error) {
      console.error('Error fetching claim by ID:', error);
      alert('An error occurred while fetching the claim');
    }
  };

  // Function to check fraud
  const checkFraud = async () => {
    if (!claimId) {
      alert('No claim selected to analyze for fraud');
      return;
    }

    try {
      const response = await fetch('/api/fraudCheck', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          claimDetails: formatClaimDetailsForAI(claimDetails),
          claimDescription,
        }),
      });

      const data = await response.json();

      if (response.ok) {
        const aiResponse = data.aiResponse;

        // Parse the AI response
        const fraudLikelihoodMatch = aiResponse.match(/Fraud Likelihood:\s*(\d+)%?/i);
        const reasoningMatch = aiResponse.match(/\*\*Reasoning:\*\*\s*([\s\S]*)/i);

        if (fraudLikelihoodMatch && reasoningMatch) {
          const fraudLikelihood = parseInt(fraudLikelihoodMatch[1]);
          const reasoning = reasoningMatch[1];

          setFraudScore(fraudLikelihood); // Populate Fraud Risk Score
          setFraudAnalysis(`**Reasoning:**\n\n${reasoning.trim()}`); // Include "Reasoning:" with double newline
          alert('Fraud analysis completed successfully.');
        } else {
          alert('Failed to parse fraud analysis response.');
        }
      } else {
        alert('Failed to perform fraud analysis.');
      }
    } catch (error) {
      console.error('Error performing fraud analysis:', error);
      alert('An error occurred while analyzing fraud.');
    }
  };

  // Function to handle "Explain More"
  const explainMore = async () => {
    if (!claimId) {
      alert('No claim selected to explain further');
      return;
    }

    try {
      const response = await fetch('/api/explainMoreFraud', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          claimDetails: formatClaimDetailsForAI(claimDetails),
          claimDescription,
          fraudScore,
          fraudAnalysis,
        }),
      });

      const data = await response.json();

      if (response.ok) {
        const furtherReasoningHeader = '\n\n**Further Reasoning:**\n\n';
        const explanationContent = data.explanation.trim();

        // Check if "Further Reasoning:" already exists
        if (fraudAnalysis.includes('**Further Reasoning:**')) {
          // Append only the new explanation
          setFraudAnalysis((prev) => `${prev}\n\n${explanationContent}`);
        } else {
          // Append the header and the explanation
          setFraudAnalysis(
            (prev) => `${prev}${furtherReasoningHeader}${explanationContent}`
          );
        }
      } else {
        alert('Failed to retrieve detailed explanation.');
      }
    } catch (error) {
      console.error('Error retrieving explanation:', error);
      alert('An error occurred while retrieving explanation.');
    }
  };

  const populateClaimDetails = (data) => {
    setClaimId(data.claimID);
    setClaimDetails({
      claimID: data.claimID,
      firstName: data.firstName,
      lastName: data.lastName,
      claimStatus: data.claimStatus,
      claimOutcome: data.claimOutcome || 'pending',
      applicationDate: data.applicationDate,
      outcomeDate: data.outcomeDate,
      timeAsCustomer: data.timeAsCustomer,
      driverAge: data.driverAge,
      insuranceAccess: data.insuranceAccess,
      insurancePremium: data.insurancePremium,
      driverGender: data.driverGender,
      educationLevel: data.educationLevel,
      accidentType: data.accidentType,
      incidentSeverity: data.incidentSeverity,
      authoritiesInvolved: data.authoritiesInvolved,
      incidentTime: data.incidentTime,
      incidentDate: data.incidentDate,
      numVehiclesInvolved: data.numVehiclesInvolved,
      numBodilyInjuries: data.numBodilyInjuries,
      policeReportBool: data.policeReportBool,
      totalClaimAmount: data.totalClaimAmount,
      vehicleAge: data.vehicleAge,
      driverExperience: data.driverExperience,
      licenseType: data.licenseType,
    });
    setClaimOutcome(data.claimOutcome || 'pending');
    setClaimDescription(data.claimDescription || 'No description provided');
    setFraudScore(data.fraudChance || 'N/A');
    setFraudAnalysis(data.fraudAnalysis || 'N/A');
    setClaimNotes(data.claimNotes || 'No notes available');
    setCustomQuestion('');
    setCustomResponse('');
  };

  const formatClaimDetailsForAI = (details) => {
    return Object.entries(details)
      .map(([key, value]) => `${key}: ${value}`)
      .join('\n');
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
    setClaimDetails({});
    setClaimOutcome('pending');
    setClaimNotes('');
    setFraudScore('');
    setFraudAnalysis('');
    setClaimDescription('');
    setClaimId(null);
    setSearchClaimId('');
    setCustomQuestion('');
    setCustomResponse('');
  };

  const getFraudScoreColor = (score) => {
    if (score === '' || score === 'N/A' || isNaN(score)) {
      return '';
    }
    const numericScore = parseInt(score);
    if (numericScore >= 70) {
      return 'bg-red-500 text-white';
    } else if (numericScore >= 40) {
      return 'bg-yellow-500 text-white';
    } else {
      return 'bg-green-500 text-white';
    }
  };

  const askCustomQuestion = async () => {
    if (!claimId) {
      alert('No claim selected to analyze');
      return;
    }

    if (!customQuestion) {
      alert('Please enter a question');
      return;
    }

    try {
      const response = await fetch('/api/askQuestion', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          claimDetails: formatClaimDetailsForAI(claimDetails),
          claimDescription,
          question: customQuestion,
        }),
      });

      const data = await response.json();

      if (response.ok) {
        setCustomResponse(data.answer);
      } else {
        alert('Failed to get answer from AI.');
      }
    } catch (error) {
      console.error('Error getting AI response:', error);
      alert('An error occurred while getting AI response.');
    }
  };

  return (
    <div className="bg-gray-100 min-h-screen">
      {/* Header */}
      <header className="bg-white shadow-md">
        <div className="max-w-screen-2xl mx-auto px-6 py-4">
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
      <main className="max-w-screen-2xl mx-auto px-6 py-4">
        {/* Claim Search Section */}
        <div className="bg-white rounded-full shadow-md px-6 py-4 mb-6 flex justify-between items-center">
          <button
            type="button"
            onClick={getFirstOpenClaim}
            className="w-full md:w-auto mb-2 md:mb-0 px-6 py-2 bg-blue-600 text-white font-semibold rounded-full shadow-md hover:bg-blue-700 transition"
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
              className="p-2 border rounded-full w-full md:w-64 focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <button
              type="button"
              onClick={getClaimById}
              className="px-6 py-2 bg-blue-600 text-white font-semibold rounded-full shadow-md hover:bg-blue-700 transition"
            >
              Search
            </button>
          </div>
        </div>

        {/* Main Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-5 gap-4">
          {/* Left Column */}
          <div className="lg:col-span-3 space-y-6">
            {/* Claim Information */}
            <div className="bg-white shadow-md rounded-lg p-6">
              {claimId ? (
                <>
                  <h2 className="text-xl font-bold text-nrmaBlue mb-4">
                    Claim Information - ID: {claimId}
                  </h2>
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                    {/* Driver Details */}
                    <div>
                      <h3 className="text-lg font-semibold text-gray-700 mb-2">
                        Driver Details
                      </h3>
                      <div className="space-y-1">
                        <div>
                          <span className="font-semibold">First Name:</span>{' '}
                          {claimDetails.firstName}
                        </div>
                        <div>
                          <span className="font-semibold">Last Name:</span>{' '}
                          {claimDetails.lastName}
                        </div>
                        <div>
                          <span className="font-semibold">Driver Age:</span>{' '}
                          {claimDetails.driverAge}
                        </div>
                        <div>
                          <span className="font-semibold">Driver Gender:</span>{' '}
                          {claimDetails.driverGender}
                        </div>
                        <div>
                          <span className="font-semibold">Education Level:</span>{' '}
                          {claimDetails.educationLevel}
                        </div>
                        <div>
                          <span className="font-semibold">Driver Experience:</span>{' '}
                          {claimDetails.driverExperience}
                        </div>
                        <div>
                          <span className="font-semibold">License Type:</span>{' '}
                          {claimDetails.licenseType}
                        </div>
                      </div>
                    </div>
                    {/* Incident Details */}
                    <div>
                      <h3 className="text-lg font-semibold text-gray-700 mb-2">
                        Incident Details
                      </h3>
                      <div className="space-y-1">
                        <div>
                          <span className="font-semibold">Incident Date:</span>{' '}
                          {claimDetails.incidentDate}
                        </div>
                        <div>
                          <span className="font-semibold">Accident Type:</span>{' '}
                          {claimDetails.accidentType}
                        </div>
                        <div>
                          <span className="font-semibold">Incident Severity:</span>{' '}
                          {claimDetails.incidentSeverity}
                        </div>
                        <div>
                          <span className="font-semibold">Authorities Involved:</span>{' '}
                          {claimDetails.authoritiesInvolved}
                        </div>
                        <div>
                          <span className="font-semibold">Incident Time:</span>{' '}
                          {claimDetails.incidentTime}
                        </div>
                        <div>
                          <span className="font-semibold">Number of Vehicles Involved:</span>{' '}
                          {claimDetails.numVehiclesInvolved}
                        </div>
                        <div>
                          <span className="font-semibold">Number of Bodily Injuries:</span>{' '}
                          {claimDetails.numBodilyInjuries}
                        </div>
                        <div>
                          <span className="font-semibold">Police Report:</span>{' '}
                          {claimDetails.policeReportBool}
                        </div>
                      </div>
                    </div>
                    {/* Claim Details */}
                    <div>
                      <h3 className="text-lg font-semibold text-gray-700 mb-2">
                        Claim Details
                      </h3>
                      <div className="space-y-1">
                        <div>
                          <span className="font-semibold">Application Date:</span>{' '}
                          {claimDetails.applicationDate}
                        </div>
                        <div>
                          <span className="font-semibold">Claim Status:</span>{' '}
                          {claimDetails.claimStatus}
                        </div>
                        <div>
                          <span className="font-semibold">Claim Outcome:</span>{' '}
                          {claimDetails.claimOutcome}
                        </div>
                        <div>
                          <span className="font-semibold">Total Claim Amount:</span>{' '}
                          {claimDetails.totalClaimAmount}
                        </div>
                        <div>
                          <span className="font-semibold">Outcome Date:</span>{' '}
                          {claimDetails.outcomeDate || 'N/A'}
                        </div>
                      </div>
                    </div>
                  </div>
                </>
              ) : (
                <p className="text-gray-500">
                  No claim selected. Please select a claim to view details.
                </p>
              )}
            </div>

            {/* Fraud Analysis */}
            <div className="bg-white shadow-md rounded-lg p-6">
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-xl font-bold text-nrmaBlue">Fraud Analysis</h2>
                <button
                  type="button"
                  onClick={checkFraud}
                  className="px-4 py-2 bg-blue-600 text-white font-semibold rounded-full shadow-md hover:bg-blue-700 transition"
                >
                  Check Fraud
                </button>
              </div>
              {/* Fraud Risk Score */}
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
                  className={`w-full p-3 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 ${getFraudScoreColor(
                    fraudScore
                  )}`}
                  readOnly
                />
              </div>
              {/* Fraud Analysis Reasoning */}
              <div className="relative">
                <label
                  htmlFor="fraudAnalysis"
                  className="block text-sm font-medium text-gray-700 mb-1"
                >
                  Fraud Analysis Reasoning
                </label>
                <div
                  id="fraudAnalysis"
                  className="w-full h-64 p-3 border rounded-md overflow-y-auto bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <ReactMarkdown remarkPlugins={[remarkBreaks]}>
                    {fraudAnalysis}
                  </ReactMarkdown>
                </div>
                <button
                  type="button"
                  className="absolute right-4 bottom-4 px-3 py-2 bg-blue-600 text-white rounded-full shadow-md hover:bg-blue-700 transition"
                  onClick={explainMore}
                >
                  Explain More
                </button>
              </div>
            </div>

            {/* Claim Outcome */}
            <div className="bg-white shadow-md rounded-lg p-6">
              <h2 className="text-xl font-bold text-nrmaBlue mb-4">Claim Outcome</h2>
              <label
                htmlFor="claimOutcome"
                className="block text-sm font-medium text-gray-700 mb-2"
              >
                Select Outcome
              </label>
              <select
                id="claimOutcome"
                name="claimOutcome"
                value={claimOutcome}
                onChange={(e) => setClaimOutcome(e.target.value)}
                className="w-full p-3 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="pending">Pending</option>
                <option value="escalated">Escalated</option>
                <option value="approved">Approved</option>
                <option value="denied">Denied</option>
              </select>
            </div>
          </div>

          {/* Right Column */}
          <div className="lg:col-span-2 space-y-6">
            {/* Claimant's Incident Description */}
            <div className="bg-white shadow-md rounded-lg p-6">
              <h2 className="text-xl font-bold text-nrmaBlue mb-4">
                Claimant's Incident Description
              </h2>
              <textarea
                id="claimDescription"
                name="claimDescription"
                value={claimDescription}
                placeholder="Description of the claim"
                className="w-full h-40 p-3 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                readOnly
              />
            </div>

            {/* Ask a Question */}
            <div className="bg-white shadow-md rounded-lg p-6">
              <h2 className="text-xl font-bold text-nrmaBlue mb-4">Ask a Question</h2>
              <textarea
                id="customQuestion"
                name="customQuestion"
                value={customQuestion}
                onChange={(e) => setCustomQuestion(e.target.value)}
                placeholder="Enter your question about this claim"
                className="w-full h-24 p-3 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
              <button
                type="button"
                onClick={askCustomQuestion}
                className="mt-2 px-4 py-2 bg-blue-600 text-white font-semibold rounded-full shadow-md hover:bg-blue-700 transition"
              >
                Ask AI
              </button>
              {customResponse && (
                <div className="mt-4">
                  <h3 className="text-lg font-semibold text-gray-700 mb-2">AI Response:</h3>
                  <div className="p-3 border rounded-md bg-gray-50 overflow-y-auto">
                    <ReactMarkdown remarkPlugins={[remarkBreaks]}>
                      {customResponse}
                    </ReactMarkdown>
                  </div>
                </div>
              )}
            </div>

            {/* Claim Processing Notes */}
            <div className="bg-white shadow-md rounded-lg p-6">
              <h2 className="text-xl font-bold text-nrmaBlue mb-4">Claim Processing Notes</h2>
              <textarea
                id="claimNotes"
                name="claimNotes"
                value={claimNotes}
                onChange={(e) => setClaimNotes(e.target.value)}
                placeholder="Add or update claim processing notes"
                className="w-full h-40 p-3 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>

            {/* Action Buttons */}
            <div className="flex flex-col space-y-4">
              <button
                type="button"
                onClick={closeCase}
                className="w-full px-6 py-3 bg-blue-600 text-white font-semibold rounded-full shadow-md hover:bg-blue-700 transition"
              >
                Close Case
              </button>
              <button
                type="button"
                onClick={escalateClaim}
                className="w-full px-6 py-3 bg-blue-600 text-white font-semibold rounded-full shadow-md hover:bg-blue-700 transition"
              >
                Escalate to Manager
              </button>
            </div>
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
