import { useState, useEffect } from 'react';
import { useRouter } from 'next/router';

export default function Home() {
  const [claimDetails, setClaimDetails] = useState('');
  const [fraudScore, setFraudScore] = useState('');
  const [fraudAnalysis, setFraudAnalysis] = useState('');
  const [claimOutcome, setClaimOutcome] = useState('');
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
  };

  return (
    <div className="container">
      {/* NRMA Header */}
      <header className="nrma-header">
        <img src="/nrma-logo.png" alt="NRMA Logo" className="nrma-logo" />
        <button
          onClick={handleLogout}
          className="btn-secondary absolute top-2 right-2"
        >
          Logout
        </button>
      </header>

      <h1 className="text-2xl font-bold text-nrmaBlue my-4">Insurance Claim Processing</h1>

      {/* Claim Search and Fetch Section */}
      <div className="flex justify-between items-center mb-4">
        <button
          type="button"
          onClick={getFirstOpenClaim}
          className="btn-primary"
        >
          Get First Open Claim
        </button>

        <div className="flex gap-4">
          <input
            type="text"
            id="searchClaimId"
            name="searchClaimId"
            value={searchClaimId}
            onChange={(e) => setSearchClaimId(e.target.value)}
            placeholder="Enter claim number"
            className="input-field"
          />
          <button
            type="button"
            onClick={getClaimById}
            className="btn-primary"
          >
            Get Claim
          </button>
        </div>
      </div>

      {/* Claim Information */}
      <div className="mb-4">
        <label htmlFor="claimDetails" className="font-bold text-nrmaBlue">Claim Information:</label>
        <div
          id="claimDetails"
          className="border border-nrmaGrey p-4 mt-2 h-52 overflow-y-auto grid grid-cols-2 gap-4"
        >
          {claimDetails.split('\n').map((line, index) => (
            <span key={index}>{line}</span>
          ))}
        </div>
      </div>

      {/* Claim Description */}
      <div className="mb-4">
        <label htmlFor="claimDescription" className="font-bold text-nrmaBlue">Claim Description:</label>
        <textarea
          id="claimDescription"
          name="claimDescription"
          value={claimDescription}
          placeholder="Description of the claim"
          className="input-field h-24"
          readOnly
        />
      </div>

      {/* Claim Processing Notes */}
      <div className="mb-4">
        <label htmlFor="claimNotes" className="font-bold text-nrmaBlue">Claim Processing Notes:</label>
        <textarea
          id="claimNotes"
          name="claimNotes"
          value={claimNotes}
          onChange={(e) => setClaimNotes(e.target.value)}
          placeholder="Add or update claim processing notes"
          className="input-field h-24"
        />
      </div>

      {/* Fraud Probability */}
      <div className="mb-4">
        <label htmlFor="fraudScore" className="font-bold text-nrmaBlue">Fraud Risk Score (%):</label>
        <input
          type="text"
          id="fraudScore"
          name="fraudScore"
          value={fraudScore}
          placeholder="Auto-filled by AI"
          className="input-field"
          readOnly
        />
      </div>

      {/* Fraud Analysis Summary with "Explain More" Button */}
      <div className="mb-4 relative">
        <label htmlFor="fraudAnalysis" className="font-bold text-nrmaBlue">Fraud Analysis Summary:</label>
        <textarea
          id="fraudAnalysis"
          name="fraudAnalysis"
          value={fraudAnalysis}
          placeholder="Auto-filled by AI"
          className="input-field h-32"
          readOnly
        />
        <button
          type="button"
          className="btn-secondary absolute right-2 bottom-2"
        >
          Explain More
        </button>
      </div>

      {/* Claim Outcome */}
      <div className="flex gap-4 mb-4">
        <div className="w-1/2">
          <label htmlFor="claimOutcome" className="font-bold text-nrmaBlue">Claim Outcome:</label>
          <select
            id="claimOutcome"
            name="claimOutcome"
            value={claimOutcome}
            onChange={(e) => setClaimOutcome(e.target.value)}
            className="input-field"
          >
            <option value="pending">Pending</option>
            <option value="escalated">Escalated</option>
            <option value="approved">Approved</option>
            <option value="denied">Denied</option>
          </select>
        </div>
      </div>

      {/* Action Buttons */}
      <div className="mt-4 flex gap-4">
        <button
          type="button"
          onClick={closeCase}
          className="btn-primary"
        >
          Close Case
        </button>
        <button
          type="button"
          onClick={escalateClaim}
          className="btn-secondary"
        >
          Escalate to Manager
        </button>
      </div>

      {/* Footer */}
      <footer className="mt-8 text-center text-sm text-gray-600">
        Developed by Macquarie University's Team 14 Data Team for EY & NRMA.
        Chief Developer: Noorullah Khan
      </footer>
    </div>
  );
}
