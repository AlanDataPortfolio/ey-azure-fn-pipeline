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
    // Read the existing claims from the CSV file
    fs.createReadStream(csvFilePath)
      .pipe(csvParser())
      .on('data', (row) => {
        claims.push(row);
      })
      .on('end', () => {
        // Find the claim by claimId and update the claim's data
        const claimIndex = claims.findIndex((claim) => claim.claimID === claimId);
        if (claimIndex !== -1) {
          claims[claimIndex].claimStatus = claimStatus || claims[claimIndex].claimStatus;
          claims[claimIndex].claimOutcome = claimOutcome || claims[claimIndex].claimOutcome;
          claims[claimIndex].claimNotes = claimNotes || claims[claimIndex].claimNotes;
          claims[claimIndex].fraudChance = fraudChance || claims[claimIndex].fraudChance;
          claims[claimIndex].fraudAnalysis = fraudAnalysis || claims[claimIndex].fraudAnalysis;

          // Convert updated claims array to CSV format
          const csv = parse(claims, { fields: Object.keys(claims[0]) });

          // Write the updated data back to the CSV file
          fs.writeFileSync(csvFilePath, csv);
          res.status(200).json({ message: 'Claim updated successfully' });
        } else {
          res.status(404).json({ message: 'Claim not found' });
        }
      });
  } catch (error) {
    console.error('Error updating claim:', error);
    res.status(500).json({ message: 'Error updating the claim' });
  }
}
