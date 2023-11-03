const OpenAIApi  = require('openai');
const fs = require('fs');
const axios = require('axios');
require('dotenv').config();

const openai = new OpenAIApi({
  apiKey: process.env.OPENAI_API_KEY, // Provide your API key here
});
async function transcribe(file) {
  const response = await axios.post(
    'https://api.openai.com/v1/audio/transcriptions',
    {
      file,
      model: 'whisper-1'
    },
    {
      headers: {
        'Content-Type': 'multipart/form-data',
        Authorization: `Bearer ${process.env.OPENAI_API_KEY}`
      }
    }
  );

  return response.data.text;
}

async function main() {
  const file = fs.createReadStream('education.mp3');
  const transcript = await transcribe(file);

  console.log(transcript);
  
  const chatCompletion = await openai.chat.completions.create({
    model: 'gpt-3.5-turbo',
    messages: [
        {"role": "system", "content": "Please extract the Education levels with dates (start and end) and a description of each from this text" + transcript}
        
    ]
})

  const education = chatCompletion.choices[0].message.content
  console.log(education);


  

}

main();