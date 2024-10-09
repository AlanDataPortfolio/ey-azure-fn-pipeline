// pages/api/getClaim.js

import fs from 'fs';
import path from 'path';
import csv from 'csv-parser';

export default async function handler(req, res) {
  const claims = [];
  const filePath = path.join(process.cwd(), 'claims.csv');

  // Read the CSV file
  fs.createReadStream(filePath)
    .pipe(csv())
    .on('data', (row) => {
      claims.push(row);
    })
    .on('end', () => {
      // Find the first claim with status "open" and outcome "pending"
      const openClaim = claims.find(claim =>
        claim.claimStatus && claim.claimStatus.toLowerCase() === 'open' &&
        claim.claimOutcome && claim.claimOutcome.toLowerCase() === 'pending'
      );

      if (openClaim) {
        res.status(200).json(openClaim);
      } else {
        res.status(404).json({ message: 'No open and pending claim found' });
      }
    })
    .on('error', (error) => {
      console.error('Error reading the CSV file:', error);
      res.status(500).json({ message: 'Error reading the CSV file' });
    });
}
