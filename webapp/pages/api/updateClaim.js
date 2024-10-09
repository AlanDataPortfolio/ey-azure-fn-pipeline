// pages/api/updateClaim.js

import fs from 'fs';
import path from 'path';
import csvParser from 'csv-parser';
import { parse } from 'json2csv';

// Function to update the claim in the CSV file
async function updateCSV(claimId, newStatus, newOutcome) {
  const filePath = path.resolve('./claims.csv');
  const updatedRows = [];
  let headers;

  // Read the CSV file and update the relevant claim
  return new Promise((resolve, reject) => {
    fs.createReadStream(filePath)
      .pipe(csvParser())
      .on('headers', (headerArray) => {
        headers = headerArray; // Store header row
      })
      .on('data', (row) => {
        if (row.claimID === claimId) {
          // Update the claim's status and outcome
          row.claimStatus = newStatus;
          row.claimOutcome = newOutcome;
        }
        updatedRows.push(row);
      })
      .on('end', () => {
        // Write the updated rows back to the CSV file
        const csvData = parse(updatedRows, { fields: headers });
        fs.writeFileSync(filePath, csvData);
        resolve('Claim updated successfully');
      })
      .on('error', (error) => {
        reject(error);
      });
  });
}

export default async function handler(req, res) {
  if (req.method === 'POST') {
    const { claimId, claimStatus, claimOutcome } = req.body;

    try {
      const message = await updateCSV(claimId, claimStatus, claimOutcome);
      res.status(200).json({ message });
    } catch (error) {
      res.status(500).json({ message: 'Error updating claim', error: error.message });
    }
  } else {
    res.status(405).json({ message: 'Method not allowed' });
  }
}
