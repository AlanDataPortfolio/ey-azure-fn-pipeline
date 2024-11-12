const axios = require('axios');

const endpoint = 'https://openaicalls.openai.azure.com/openai/deployments/gpt-4o-mini/chat/completions?api-version=2024-08-01-preview';
const apiKey = '51d905fd22794937a2faf5e87c51f72e';

async function callOpenAI() {
    try {
        const response = await axios.post(
            endpoint,
            {
                messages: [{ role: "system", content: "What's the distance from Sydney to Melbourne" }]
            },
            {
                headers: {
                    'Content-Type': 'application/json',
                    'api-key': apiKey 
                }
            }
        );
        // Print the actual AI response message
        console.log("AI Response:", response.data.choices[0].message);
    } catch (error) {
        console.error("Error calling Azure OpenAI:", error.response ? error.response.data : error.message);
    }
}

callOpenAI();
