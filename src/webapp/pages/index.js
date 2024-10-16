import { useState } from 'react';

export default function Home() {
  const [claimDetails, setClaimDetails] = useState('');
  const [fraudScore, setFraudScore] = useState('');
  const [fraudAnalysis, setFraudAnalysis] = useState('');
  const [claimOutcome, setClaimOutcome] = useState('');
  const [claimNotes, setClaimNotes] = useState(''); // Field for claim notes
  const [claimDescription, setClaimDescription] = useState('');
  const [claimId, setClaimId] = useState(null); // Store the current Claim ID for saving
  const [searchClaimId, setSearchClaimId] = useState(''); // Field for searching by claim ID

  // Fetch the first open and pending claim
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

  // Fetch a specific claim by claim ID
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

  // Function to populate the form with fetched claim data
  const populateClaimDetails = (data) => {
    setClaimId(data.claimID); // Save Claim ID for updates
    setClaimDetails(
      `Claim ID: ${data.claimID}\n` +
      `First Name: ${data.firstname}\n` +
      `Last Name: ${data.lastname}\n` +
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

  // Update the claim on close case
  const closeCase = async () => {
    if (!claimId) {
      alert('No claim selected to close');
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
          claimStatus: 'closed',
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

  // Escalate the claim
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

  // Clear all fields after processing
  const clearFields = () => {
    setClaimDetails('');
    setClaimOutcome('pending');
    setClaimNotes('');
    setFraudScore('');
    setFraudAnalysis('');
    setClaimDescription('');
  };

  return (
    <div style={{ padding: "20px", maxWidth: "800px", margin: "auto" }}>
      <h1>Insurance Claim Processing</h1>

      {/* Claim Search and Fetch Section */}
      <div style={{ display: "flex", justifyContent: "space-between", marginBottom: "15px" }}>
        {/* Left side: Get First Open Claim Button */}
        <button
          type="button"
          onClick={getFirstOpenClaim}
          style={{
            padding: "10px 20px",
            backgroundColor: "#0070f3",
            color: "white",
            border: "none",
            cursor: "pointer",
          }}
        >
          Get First Open Claim
        </button>

        {/* Right side: Search by Claim Number */}
        <div style={{ display: "flex", gap: "10px" }}>
          <input
            type="text"
            id="searchClaimId"
            name="searchClaimId"
            value={searchClaimId}
            onChange={(e) => setSearchClaimId(e.target.value)}
            placeholder="Enter claim number"
            style={{ width: "200px", padding: "8px" }}
          />
          <button
            type="button"
            onClick={getClaimById}
            style={{
              padding: "10px 20px",
              backgroundColor: "#0070f3",
              color: "white",
              border: "none",
              cursor: "pointer",
            }}
          >
            Get Claim
          </button>
        </div>
      </div>

      {/* Claim Information */}
      <div style={{ marginBottom: "15px" }}>
        <label htmlFor="claimDetails">Claim Information:</label>
        <div
          id="claimDetails"
          style={{
            border: "1px solid #ccc",
            padding: "10px",
            marginTop: "5px",
            height: "200px",
            overflowY: "auto",
            display: "grid",
            gridTemplateColumns: "1fr 1fr",
            gap: "20px",
            fontFamily: "monospace",
            whiteSpace: "pre-wrap",
          }}
        >
          {claimDetails.split('\n').map((line, index) => (
            <span key={index}>{line}</span>
          ))}
        </div>
      </div>

      {/* Claim Description */}
      <div style={{ marginBottom: "15px" }}>
        <label htmlFor="claimDescription">Claim Description:</label>
        <textarea
          id="claimDescription"
          name="claimDescription"
          value={claimDescription}
          placeholder="Description of the claim"
          style={{ width: "100%", padding: "8px", marginTop: "5px", height: "60px" }}
          readOnly
        />
      </div>

      {/* Claim Processing Notes */}
      <div style={{ marginBottom: "15px" }}>
        <label htmlFor="claimNotes">Claim Processing Notes:</label>
        <textarea
          id="claimNotes"
          name="claimNotes"
          value={claimNotes}
          onChange={(e) => setClaimNotes(e.target.value)}
          placeholder="Add or update claim processing notes"
          style={{ width: "100%", padding: "8px", marginTop: "5px", height: "60px" }}
        />
      </div>

      {/* Fraud Probability */}
      <div style={{ marginBottom: "15px" }}>
        <label htmlFor="fraudScore">Fraud Risk Score (%):</label>
        <input
          type="text"
          id="fraudScore"
          name="fraudScore"
          value={fraudScore}
          placeholder="Auto-filled by AI"
          style={{ width: "100%", padding: "8px", marginTop: "5px" }}
          readOnly
        />
      </div>

      {/* Fraud Analysis Summary with "Explain More" Button */}
      <div style={{ marginBottom: "15px", position: "relative" }}>
        <label htmlFor="fraudAnalysis">Fraud Analysis Summary:</label>
        <textarea
          id="fraudAnalysis"
          name="fraudAnalysis"
          value={fraudAnalysis}
          placeholder="Auto-filled by AI"
          style={{ width: "100%", padding: "8px", marginTop: "5px", height: "80px" }}
          readOnly
        />
        <button
          type="button"
          style={{
            position: "absolute",
            right: "10px",
            bottom: "10px",
            padding: "5px 10px",
            backgroundColor: "#ff6347",
            color: "white",
            border: "none",
            cursor: "pointer",
          }}
        >
          Explain More
        </button>
      </div>

      {/* Claim Outcome */}
      <div style={{ display: "flex", gap: "10px", marginBottom: "15px" }}>
        <div style={{ flex: 1 }}>
          <label htmlFor="claimOutcome">Claim Outcome:</label>
          <select
            id="claimOutcome"
            name="claimOutcome"
            value={claimOutcome}
            onChange={(e) => setClaimOutcome(e.target.value)}
            style={{ width: "100%", padding: "8px", marginTop: "5px" }}
          >
            <option value="pending">Pending</option>
            <option value="escalated">Escalated</option>
            <option value="approved">Approved</option>
            <option value="denied">Denied</option>
          </select>
        </div>
      </div>

      {/* Action Buttons */}
      <div style={{ marginTop: "20px" }}>
        <button
          type="button"
          onClick={closeCase}
          style={{
            padding: "10px 20px",
            backgroundColor: "#0070f3",
            color: "white",
            border: "none",
            cursor: "pointer",
            marginRight: "10px",
          }}
        >
          Close Case
        </button>
        <button
          type="button"
          onClick={escalateClaim}
          style={{
            padding: "10px 20px",
            backgroundColor: "#28a745",
            color: "white",
            border: "none",
            cursor: "pointer",
          }}
        >
          Escalate to Manager
        </button>
      </div>
    </div>
  );
}
