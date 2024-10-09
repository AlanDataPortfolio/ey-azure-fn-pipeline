// pages/index.js

import { useState } from 'react';

export default function Home() {
  const [claimDetails, setClaimDetails] = useState('');
  const [fraudScore, setFraudScore] = useState('');
  const [fraudEvaluation, setFraudEvaluation] = useState('');
  const [claimOutcome, setClaimOutcome] = useState('');
  const [claimDescription, setClaimDescription] = useState('');
  const [claimId, setClaimId] = useState(null); // Store the current Claim ID

  // Function to fetch the first open and pending claim from the API
  const getClaim = async () => {
    try {
      const response = await fetch('/api/getClaim');
      const data = await response.json();
      if (response.ok) {
        setClaimId(data.claimid); // Save Claim ID for updates
        setClaimDetails(
          `Claim ID: ${data.claimid}\n` +
          `First Name: ${data.firstname}\n` +
          `Last Name: ${data.lastname}\n` +
          `Claim Status: ${data.claimstatus}\n` +
          `Claim Outcome: ${data.claimoutcome}\n` +
          `Time as Customer: ${data.timeascustomer}\n` +
          `Driver Age: ${data.driverage}\n` +
          `Insurance Access: ${data.insuranceaccess}\n` +
          `Insurance Premium: ${data.insurancepremium}\n` +
          `Driver Gender: ${data.drivergender}\n` +
          `Education Level: ${data.educationlevel}\n` +
          `Accident Type: ${data.accidenttype}\n` +
          `Incident Severity: ${data.incidentseverity}\n` +
          `Authorities Involved: ${data.authoritiesinvolved}\n` +
          `Incident Time: ${data.incidenttime}\n` +
          `Num Vehicles Involved: ${data.numvehiclesinvolved}\n` +
          `Num Bodily Injuries: ${data.numbodilyinjuries}\n` +
          `Police Report: ${data.policereportbool}\n` +
          `Total Claim Amount: ${data.totalclaimamount}\n` +
          `Vehicle Age: ${data.vehicleage}\n` +
          `Driver Experience: ${data.driverexperience}\n` +
          `License Type: ${data.licensetype}\n`
        );
        setClaimOutcome(data.claimoutcome || 'pending');
        setClaimDescription(data.claimdescription || 'No description provided');
        setFraudScore('N/A');
        setFraudEvaluation('N/A');
        alert('Claim data fetched successfully');
      } else {
        alert(data.message);
      }
    } catch (error) {
      console.error('Error fetching claim:', error);
      alert('An error occurred while fetching the claim');
    }
  };

  // Function to update the claim outcome and status
  const updateClaim = async (newOutcome) => {
    if (!claimId) {
      alert('No claim selected to update');
      return;
    }

    let newStatus = 'open';
    if (newOutcome === 'approved' || newOutcome === 'denied') {
      newStatus = 'closed'; // Automatically close the claim if approved or denied
    }

    try {
      const response = await fetch('/api/updateClaim', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          claimId,
          claimStatus: newStatus,
          claimOutcome: newOutcome,
        }),
      });

      const result = await response.json();
      if (response.ok) {
        alert(result.message);
        // Clear the form fields after closing the case
        clearFormFields();
      } else {
        alert(result.message);
      }
    } catch (error) {
      console.error('Error updating claim:', error);
      alert('An error occurred while updating the claim');
    }
  };

  // Function to clear the form fields
  const clearFormFields = () => {
    setClaimDetails('');
    setClaimDescription('');
    setFraudScore('');
    setFraudEvaluation('');
    setClaimId(null);
    setClaimOutcome('pending');
  };

  return (
    <div style={{ padding: "20px", maxWidth: "800px", margin: "auto" }}>
      <h1>Insurance Claim Processing</h1>
      <form>
        {/* Get Claim Button */}
        <div style={{ marginBottom: "15px" }}>
          <button
            type="button"
            onClick={getClaim}
            style={{
              padding: "10px 20px",
              backgroundColor: "#0070f3",
              color: "white",
              border: "none",
              cursor: "pointer",
              marginBottom: "10px",
            }}
          >
            Get Claim
          </button>
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

        {/* Check Fraud Button */}
        <div style={{ marginBottom: "15px" }}>
          <button
            type="button"
            style={{
              padding: "10px 20px",
              backgroundColor: "#ff6347",
              color: "white",
              border: "none",
              cursor: "pointer",
            }}
          >
            Check Fraud
          </button>
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

        {/* Fraud Evaluation Summary */}
        <div style={{ marginBottom: "15px" }}>
          <label htmlFor="fraudEvaluation">Fraud Analysis Summary:</label>
          <textarea
            id="fraudEvaluation"
            name="fraudEvaluation"
            value={fraudEvaluation}
            placeholder="Auto-filled by AI"
            style={{ width: "100%", padding: "8px", marginTop: "5px", height: "80px" }}
            readOnly
          />
        </div>

        {/* Claim Outcome */}
        <div style={{ marginBottom: "15px" }}>
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

        <div style={{ marginTop: "20px" }}>
          <button
            type="button"
            onClick={() => updateClaim(claimOutcome)}
            style={{
              padding: "10px 20px",
              backgroundColor: "#28a745",
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
            onClick={() => updateClaim("escalated")}
            style={{
              padding: "10px 20px",
              backgroundColor: "#0070f3",
              color: "white",
              border: "none",
              cursor: "pointer",
            }}
          >
            Escalate to Manager
          </button>
        </div>
      </form>
    </div>
  );
}
