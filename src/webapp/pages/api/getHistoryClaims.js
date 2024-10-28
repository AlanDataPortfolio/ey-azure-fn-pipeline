// pages/api/getHistoryClaims.js

import csv from 'csvtojson';
import path from 'path';
import fs from 'fs';

export default async function handler(req, res) {
  if (req.method === 'GET') {
    try {
      const csvFilePath = path.join(process.cwd(), 'claims.csv');

      if (!fs.existsSync(csvFilePath)) {
        res.status(404).json({ error: 'Claims file not found.' });
        return;
      }

      const jsonArray = await csv().fromFile(csvFilePath);

      // Filter claims to include closed cases and open but escalated cases
      const filteredClaims = jsonArray.filter(
        (claim) =>
          claim.claimStatus === 'closed' ||
          (claim.claimStatus === 'open' && claim.claimOutcome === 'escalated')
      );

      // Include incidentDate, applicationDate, and outcomeDate in the response
      res.status(200).json({ claims: filteredClaims });
    } catch (error) {
      console.error('Error reading claims:', error);
      res.status(500).json({ error: 'Failed to retrieve claims.' });
    }
  } else {
    res.status(405).json({ error: 'Method not allowed' });
  }
}
