// pages/api/updateClaim.js

import csv from 'csvtojson';
import json2csv from 'json2csv';
import path from 'path';
import fs from 'fs';

export default async function handler(req, res) {
  if (req.method === 'POST') {
    const {
      claimId,
      claimStatus,
      claimOutcome,
      claimNotes,
      fraudChance,
      fraudAnalysis,
    } = req.body;

    try {
      const csvFilePath = path.join(process.cwd(), 'claims.csv');

      if (!fs.existsSync(csvFilePath)) {
        res.status(404).json({ error: 'Claims file not found.' });
        return;
      }

      let jsonArray = await csv().fromFile(csvFilePath);

      const claimIndex = jsonArray.findIndex((c) => c.claimID === claimId);

      if (claimIndex !== -1) {
        // Update claim details
        jsonArray[claimIndex].claimStatus = claimStatus;
        jsonArray[claimIndex].claimOutcome = claimOutcome;
        jsonArray[claimIndex].claimNotes = claimNotes;
        jsonArray[claimIndex].fraudChance = fraudChance;
        jsonArray[claimIndex].fraudAnalysis = fraudAnalysis;

        // If the claim is being closed (status changes from pending)
        if (claimStatus === 'closed' && claimOutcome !== 'pending') {
          // Record the current date as outcomeDate
          const currentDate = new Date().toISOString().split('T')[0];
          jsonArray[claimIndex].outcomeDate = currentDate;
        }

        // Convert back to CSV
        const csvData = json2csv.parse(jsonArray, { fields: Object.keys(jsonArray[0]) });

        // Write to CSV file
        fs.writeFileSync(csvFilePath, csvData);

        res.status(200).json({ message: 'Claim updated successfully.' });
      } else {
        res.status(404).json({ message: 'Claim not found.' });
      }
    } catch (error) {
      console.error('Error updating claim:', error);
      res.status(500).json({ error: 'Failed to update claim.' });
    }
  } else {
    res.status(405).json({ error: 'Method not allowed' });
  }
}

