// pages/api/getClaim.js

import csv from 'csvtojson';
import path from 'path';
import fs from 'fs';

export default async function handler(req, res) {
  if (req.method === 'GET') {
    const { claimId } = req.query;

    try {
      const csvFilePath = path.join(process.cwd(), 'claims.csv');

      if (!fs.existsSync(csvFilePath)) {
        res.status(404).json({ error: 'Claims file not found.' });
        return;
      }

      const jsonArray = await csv().fromFile(csvFilePath);

      let claim;
      if (claimId) {
        // Fetch claim by ID
        claim = jsonArray.find((c) => c.claimID === claimId);
      } else {
        // Fetch the first open/pending claim
        claim = jsonArray.find(
          (c) => c.claimStatus === 'open' && c.claimOutcome === 'pending'
        );
      }

      if (claim) {
        res.status(200).json(claim);
      } else {
        res.status(404).json({ message: 'Claim not found' });
      }
    } catch (error) {
      console.error('Error reading claims:', error);
      res.status(500).json({ error: 'Failed to retrieve claim.' });
    }
  } else {
    res.status(405).json({ error: 'Method not allowed' });
  }
}
