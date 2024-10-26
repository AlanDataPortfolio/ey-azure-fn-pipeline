// pages/api/fraudCheck.js

import axios from 'axios';

const endpoint = 'https://openaicalls.openai.azure.com/openai/deployments/gpt-4o-mini/chat/completions?api-version=2024-08-01-preview';
const apiKey = '51d905fd22794937a2faf5e87c51f72e'; // Replace with your actual API key

export default async function handler(req, res) {
  if (req.method === 'POST') {
    const { claimDetails, claimDescription } = req.body;

    try {
      const systemPrompt = `
You are a fraud detection assistant who assists claim agents with processing car insurance claims. Your task is to assess the likelihood of fraud based on the provided claim details and by comparing them to the claim description. Return a percentage indicating the fraud likelihood and provide a concise but accurate reasoning to justify this percentage. Reference only the most relevant claim details.
      `;

      const userPrompt = `
Claim Details:
${claimDetails}

Claim Description:
${claimDescription}
      `;

      const response = await axios.post(
        endpoint,
        {
          messages: [
            { role: 'system', content: systemPrompt },
            { role: 'user', content: userPrompt },
          ],
        },
        {
          headers: {
            'Content-Type': 'application/json',
            'api-key': apiKey,
        },
      });

      const aiResponse = response.data.choices[0].message.content;

      res.status(200).json({ aiResponse });
    } catch (error) {
      console.error('Error calling Azure OpenAI:', error.response ? error.response.data : error.message);
      res.status(500).json({ error: 'Failed to retrieve fraud analysis.' });
    }
  } else {
    res.status(405).json({ error: 'Method not allowed' });
  }
}
