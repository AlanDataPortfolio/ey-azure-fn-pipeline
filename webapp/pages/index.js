// pages/index.js

import { useState } from 'react';

export default function Home() {
  const [claimDetails, setClaimDetails] = useState('');
  const [fraudScore, setFraudScore] = useState('');
  const [fraudEvaluation, setFraudEvaluation] = useState('');
  const [claimStatus, setClaimStatus] = useState('open');
  const [claimOutcome, setClaimOutcome] = useState('pending');

  // Function to fetch the first open and pending claim from the API
  const getClaim = async () => {
    try {
      const response = await fetch('/api/getClaim');
      const data = await response.json();
      if (response.ok) {
        // Populate the form with the fetched data
        setClaimDetails(
          `ClaimID: ${data.ClaimID}\n` +
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
          `License Type: ${data.licenseType}\n` +
          `First Name: ${data.firstName}\n` +
          `Last Name: ${data.lastName}\n`
        );
        setClaimStatus(data.claimStatus || 'open');
        setClaimOutcome(data.claimOutcome || 'pending');
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

  return (
    <div style={{ padding: "20px", maxWidth: "600px", margin: "auto" }}>
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

        {/* Claim Details */}
        <div style={{ marginBottom: "15px" }}>
          <label htmlFor="claimDetails">Claim Information:</label>
          <textarea
            id="claimDetails"
            name="claimDetails"
            value={claimDetails}
            placeholder="Claim details will be auto-filled"
            style={{ width: "100%", padding: "8px", marginTop: "5px", height: "200px" }}
            readOnly
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

        {/* Claim Status and Outcome (side by side) */}
        <div style={{ display: "flex", gap: "10px", marginBottom: "15px" }}>
          <div style={{ flex: 1 }}>
            <label htmlFor="claimStatus">Current Claim Status:</label>
            <select
              id="claimStatus"
              name="claimStatus"
              value={claimStatus}
              onChange={(e) => setClaimStatus(e.target.value)}
              style={{ width: "100%", padding: "8px", marginTop: "5px" }}
            >
              <option value="open">Open</option>
              <option value="closed">Closed</option>
            </select>
          </div>

          <div style={{ flex: 1 }}>
            <label htmlFor="claimOutcome">Claim Decision:</label>
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

        <div style={{ marginTop: "20px" }}>
          <button
            type="button"
            style={{
              padding: "10px 20px",
              backgroundColor: "#0070f3",
              color: "white",
              border: "none",
              cursor: "pointer",
              marginRight: "10px",
            }}
          >
            Escalate to Manager
          </button>
          <button
            type="button"
            style={{
              padding: "10px 20px",
              backgroundColor: "#28a745",
              color: "white",
              border: "none",
              cursor: "pointer",
            }}
          >
            Close Case
          </button>
        </div>
      </form>
    </div>
  );
}
