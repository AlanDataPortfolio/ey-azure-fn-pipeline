const axios = require('axios');

export default async function fraudCheck(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const { claimDetails, claimDescription } = req.body;

  if (!claimDetails || !claimDescription) {
    return res.status(400).json({ error: 'Missing claim details or description' });
  }

  const prompt = `
  Based on the following claim details, assess whether this claim is potentially fraudulent. Focus on key indicators such as claim amount, incident type, customer history, and consistency with the claim description. Keep your response brief, highlight only relevant details, and provide a percentage estimate of fraud likelihood.

  Claim Details:
  ${claimDetails}

  Claimant's Description:
  ${claimDescription}

  Provide a percentage likelihood of fraud and the reasoning.
  `;

  const endpoint = 'https://openaicalls.openai.azure.com/openai/deployments/gpt-4o-mini/chat/completions?api-version=2024-08-01-preview';
  const apiKey = '51d905fd22794937a2faf5e87c51f72e';  // Your actual API key here

  try {
    const response = await axios.post(
      endpoint,
      {
        messages: [{ role: 'user', content: prompt }]
      },
      {
        headers: {
          'Content-Type': 'application/json',
          'api-key': apiKey  // Use 'api-key' here instead of 'Authorization'
        }
      }
    );

    const aiResponse = response.data.choices[0].message.content;
    const fraudScoreMatch = aiResponse.match(/(\d+)%/);
    const fraudScore = fraudScoreMatch ? fraudScoreMatch[1] : 'N/A';

    return res.status(200).json({
      fraudScore,
      fraudAnalysis: aiResponse
    });
  } catch (error) {
    console.error('Error with OpenAI call:', error.response?.data || error.message);
    return res.status(500).json({ error: 'Failed to perform fraud analysis' });
  }
}
