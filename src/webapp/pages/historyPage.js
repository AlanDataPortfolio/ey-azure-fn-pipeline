import { useState, useEffect } from 'react';

export default function HistoryPage() {
  const [claims, setClaims] = useState([]);

  useEffect(() => {
    // Fetch past claims from API or CSV
    fetch('/api/getPastClaims')
      .then((res) => res.json())
      .then((data) => setClaims(data))
      .catch((error) => console.error('Error fetching past claims:', error));
  }, []);

  const handleClaimClick = (claimId) => {
    // Redirect to full claim details page or display modal
    window.location.href = `/claim/${claimId}`;
  };

  return (
    <div className="max-w-7xl mx-auto p-8">
      <h1 className="text-2xl font-bold text-nrmaBlue mb-4">Claim History</h1>
      <table className="min-w-full bg-white shadow-xl rounded-lg">
        <thead>
          <tr>
            <th className="border px-4 py-2">Claim ID</th>
            <th className="border px-4 py-2">Claim Notes</th>
            <th className="border px-4 py-2">Claim Outcome</th>
          </tr>
        </thead>
        <tbody>
          {claims.map((claim) => (
            <tr key={claim.claimID} onClick={() => handleClaimClick(claim.claimID)} className="cursor-pointer hover:bg-gray-100">
              <td className="border px-4 py-2">{claim.claimID}</td>
              <td className="border px-4 py-2">{claim.claimNotes}</td>
              <td className="border px-4 py-2">{claim.claimOutcome}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
