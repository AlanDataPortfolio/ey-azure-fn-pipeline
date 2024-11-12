// pages/api/getOpenClaimsCount.js

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

      // Count the number of claims where claimStatus is 'open' and claimOutcome is 'pending'
      const openPendingClaims = jsonArray.filter(
        (claim) =>
          claim.claimStatus.toLowerCase() === 'open' &&
          claim.claimOutcome.toLowerCase() === 'pending'
      );

      res.status(200).json({ count: openPendingClaims.length });
    } catch (error) {
      console.error('Error reading claims:', error);
      res.status(500).json({ error: 'Failed to retrieve claims count.' });
    }
  } else {
    res.status(405).json({ error: 'Method not allowed' });
  }
}
