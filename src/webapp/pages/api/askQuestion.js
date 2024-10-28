// pages/api/askQuestion.js

import axios from 'axios';

const endpoint = 'https://openaicalls.openai.azure.com/openai/deployments/gpt-4o-mini/chat/completions?api-version=2024-08-01-preview';
const apiKey = '51d905fd22794937a2faf5e87c51f72e'; // Ensure you use environment variables

export default async function handler(req, res) {
    if (req.method === 'POST') {
      const { claimDetails, claimDescription, question } = req.body;
  
      try {
        const systemPrompt = `
  You are an assistant who helps claim agents with processing car insurance claims and with general information. Your task is to answer questions about a specific claim based on the provided claim details and description You may also provide general information to the user about other topics. Provide clear and concise answers. Format your response in markdown if necessary.
        `;
  
        const userPrompt = `
  Claim Details:
  ${claimDetails}
  
  Claim Description:
  ${claimDescription}
  
  Question:
  ${question}
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
  
        const aiResponse = response.data.choices[0].message.content;
  
        res.status(200).json({ answer: aiResponse });
      } catch (error) {
        console.error('Error calling Azure OpenAI:', error.response ? error.response.data : error.message);
        res.status(500).json({ error: 'Failed to get AI response.' });
      }
    } else {
      res.status(405).json({ error: 'Method not allowed' });
    }
  }