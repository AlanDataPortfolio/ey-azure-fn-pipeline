// pages/api/explainMoreFraud.js

import axios from 'axios';

const endpoint = 'https://openaicalls.openai.azure.com/openai/deployments/gpt-4o-mini/chat/completions?api-version=2024-08-01-preview';
const apiKey = '51d905fd22794937a2faf5e87c51f72e'; // Replace with your actual API key

export default async function handler(req, res) {
  if (req.method === 'POST') {
    const { claimDetails, claimDescription, fraudScore, fraudAnalysis } = req.body;

    try {
      const systemPrompt = `
You are a fraud detection assistant who provides detailed explanations for fraud assessments in car insurance claims. Your task is to elaborate on the fraud likelihood and reasoning provided earlier, offering more in-depth analysis while referencing specific claim details. Format your response in markdown, starting with '**Further Reasoning:**' followed by your explanation.
      `;

      const userPrompt = `
Claim Details:
${claimDetails}

Claim Description:
${claimDescription}

Previously Provided Fraud Likelihood: ${fraudScore}%

Previously Provided Reasoning:
${fraudAnalysis}
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
        }
      );

      const explanation = response.data.choices[0].message.content;

      res.status(200).json({ explanation });
    } catch (error) {
      console.error('Error calling Azure OpenAI:', error.response ? error.response.data : error.message);
      res.status(500).json({ error: 'Failed to retrieve detailed explanation.' });
    }
  } else {
    res.status(405).json({ error: 'Method not allowed' });
  }
}