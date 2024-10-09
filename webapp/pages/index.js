export default function Home() {
  return (
    <div style={{ padding: "20px", maxWidth: "600px", margin: "auto" }}>
      <h1>Insurance Claim Processing</h1>
      <form>
        {/* Get Claim Button */}
        <div style={{ marginBottom: "15px" }}>
          <button
            type="button"
            onClick={() => alert("Fetching the first open claim...")}
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
          <input
            type="text"
            id="claimDetails"
            name="claimDetails"
            placeholder="Claim details will be auto-filled"
            style={{ width: "100%", padding: "8px", marginTop: "5px" }}
            readOnly
          />
        </div>

        {/* Check Fraud Button */}
        <div style={{ marginBottom: "15px" }}>
          <button
            type="button"
            onClick={() => alert("Checking fraud analysis...")}
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
            placeholder="Auto-filled by AI"
            style={{ width: "100%", padding: "8px", marginTop: "5px", height: "80px" }}
            readOnly
          />
        </div>

        {/* Claim Status and Outcome (side by side) */}
        <div style={{ display: "flex", gap: "10px", marginBottom: "15px" }}>
          {/* Claim Status */}
          <div style={{ flex: 1 }}>
            <label htmlFor="claimStatus">Current Claim Status:</label>
            <select
              id="claimStatus"
              name="claimStatus"
              style={{ width: "100%", padding: "8px", marginTop: "5px" }}
            >
              <option value="open">Open</option>
              <option value="closed">Closed</option>
            </select>
          </div>

          {/* Claim Outcome */}
          <div style={{ flex: 1 }}>
            <label htmlFor="claimOutcome">Claim Decision:</label>
            <select
              id="claimOutcome"
              name="claimOutcome"
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
