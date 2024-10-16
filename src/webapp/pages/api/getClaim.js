// pages/api/getClaim.js

import fs from 'fs';
import path from 'path';
import csvParser from 'csv-parser';

export default async function handler(req, res) {
  const { claimId } = req.query; // Get claimId from query params (if provided)
  const csvFilePath = path.join(process.cwd(), 'claims.csv'); // Path to the CSV file

  const claims = [];

  try {
    // Read the CSV file and parse the claims data
    fs.createReadStream(csvFilePath)
      .pipe(csvParser())
      .on('data', (row) => {
        claims.push(row);
      })
      .on('end', () => {
        let claim;

        // Check if a specific claimId is provided for fetching
        if (claimId) {
          claim = claims.find((row) => row.claimID === claimId);
        } else {
          // Find the first claim with "open" status and "pending" outcome
          claim = claims.find(
            (row) => row.claimStatus === 'open' && row.claimOutcome === 'pending'
          );
        }

        if (claim) {
          res.status(200).json(claim);
        } else {
          res.status(404).json({ message: 'No open/pending claim found' });
        }
      });
  } catch (error) {
    console.error('Error reading the CSV file:', error);
    res.status(500).json({ message: 'Error reading the claims data' });
  }
}
