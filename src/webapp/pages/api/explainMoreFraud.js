// pages/api/explainMoreFraud.js
import axios from 'axios';

const openAIEndpoint = 'https://openaicalls.openai.azure.com/openai/deployments/gpt-4o-mini/chat/completions?api-version=2024-08-01-preview';
const apiKey = 'YOUR_AZURE_OPENAI_API_KEY'; // Replace with your Azure key

export default async function handler(req, res) {
    if (req.method === 'POST') {
        const { claimDetails, claimDescription } = req.body;

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
                openAIEndpoint,
                {
                    messages: [{ role: "system", content: secondaryPrompt }],
                },
                {
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${apiKey}`,
                    },
                }
            );

            const openAIResponse = response.data.choices[0].message.content;

            res.status(200).json({ explanation: openAIResponse });
        } catch (error) {
            console.error("Error calling Azure OpenAI:", error);
            res.status(500).json({ error: "Failed to retrieve detailed explanation." });
        }
    } else {
        res.status(405).json({ error: 'Method Not Allowed' });
    }
}
