import axios from 'axios';

const endpoint = 'https://openaicalls.openai.azure.com/openai/deployments/gpt-4o-mini/chat/completions?api-version=2024-08-01-preview';
const apiKey = '51d905fd22794937a2faf5e87c51f72e'; // Use your actual API key here

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method Not Allowed' });
  }

  const { claimDetails, claimDescription } = req.body;

  if (!claimDetails || !claimDescription) {
    return res.status(400).json({ error: 'Missing claim details or description' });
  }

  // Secondary prompt for more detailed explanation
  const secondaryPrompt = `
    Please provide a more detailed explanation for your fraud assessment.
    Given the following case details and the applicant's claim description, 
    explain in more depth why this claim is or isn't considered fraudulent:

    Case details: ${claimDetails}
    Applicant's claim description: ${claimDescription}
  `;

  try {
    const response = await axios.post(
      endpoint,
      {
        messages: [{ role: "user", content: secondaryPrompt }],
      },
      {
        headers: {
          'Content-Type': 'application/json',
          'api-key': apiKey,  // Correct header for API key
        },
      }
    );

    const openAIResponse = response.data.choices[0].message.content;

    res.status(200).json({ explanation: openAIResponse });
  } catch (error) {
    console.error("Error calling Azure OpenAI:", error.response?.data || error.message);
    res.status(500).json({ error: "Failed to retrieve detailed explanation." });
  }
}
