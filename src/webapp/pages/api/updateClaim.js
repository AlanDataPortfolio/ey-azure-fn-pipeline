// pages/api/updateClaim.js

import fs from 'fs';
import path from 'path';
import csvParser from 'csv-parser';
import { parse } from 'json2csv';

export default async function handler(req, res) {
  const { claimId, claimStatus, claimOutcome, claimNotes, fraudChance, fraudAnalysis } = req.body;
  const csvFilePath = path.join(process.cwd(), 'claims.csv'); // Path to the CSV file

  const claims = [];

  try {
    // Read and parse the existing CSV data
    fs.createReadStream(csvFilePath)
      .pipe(csvParser())
      .on('data', (row) => {
        claims.push(row);
      })
      .on('end', () => {
        let updated = false;

        // Update the claim with the matching claimId
        const updatedClaims = claims.map((claim) => {
          if (claim.claimID === claimId) {
            updated = true;
            return {
              ...claim,
              claimStatus: claimStatus || claim.claimStatus,
              claimOutcome: claimOutcome || claim.claimOutcome,
              claimNotes: claimNotes || claim.claimNotes,
              fraudChance: fraudChance || claim.fraudChance,
              fraudAnalysis: fraudAnalysis || claim.fraudAnalysis,
            };
          }
          return claim;
        });

        if (!updated) {
          return res.status(404).json({ message: 'Claim not found' });
        }

        // Convert updated claims data back to CSV format
        const csv = parse(updatedClaims, { fields: Object.keys(updatedClaims[0]) });

        // Write the updated CSV back to file
        fs.writeFileSync(csvFilePath, csv);

        res.status(200).json({ message: 'Claim updated successfully' });
      });
  } catch (error) {
    console.error('Error updating the claim:', error);
    res.status(500).json({ message: 'Error updating the claim' });
  }
}
