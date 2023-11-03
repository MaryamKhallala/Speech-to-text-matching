require('dotenv').config();
const OpenAIApi  = require('openai');
const fs = require('fs');
const axios = require('axios');

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
  const file = fs.createReadStream('Presentation.mp3');
  const transcript = await transcribe(file);

  console.log(transcript);
  
  const chatCompletion = await openai.chat.completions.create({
    model: 'gpt-3.5-turbo',
    messages: [
        {"role": "system", "content": "Please extract the Name from this text" + transcript}
        
    ]
})

  const Name = chatCompletion.choices[0].message.content
  console.log(Name);

  // Title job 
  const chatCompletion1 = await openai.chat.completions.create({
    model: 'gpt-3.5-turbo',
    messages: [
        {"role": "system", "content": "Please extract the job title from this text" + transcript}
        
    ]
})

  const job_title  = chatCompletion1.choices[0].message.content
  console.log(job_title);
  // Phone
  const chatCompletion2 = await openai.chat.completions.create({
    model: 'gpt-3.5-turbo',
    messages: [
        {"role": "system", "content": "Please extract the Phone from this text" + transcript}
        
    ]
})

  const Phone = chatCompletion2.choices[0].message.content
  console.log(Phone);

  // Email
  const chatCompletion3 = await openai.chat.completions.create({
    model: 'gpt-3.5-turbo',
    messages: [
        {"role": "system", "content": "Please extract the Email from this text" + transcript}
        
    ]
})

  const Email = chatCompletion3.choices[0].message.content
  console.log(Email);

  // Birthday

  const chatCompletion4 = await openai.chat.completions.create({
    model: 'gpt-3.5-turbo',
    messages: [
        {"role": "system", "content": "Please extract the birthday from this text" + transcript}
        
    ]
})

  const Birthday = chatCompletion4.choices[0].message.content
  console.log(Birthday);

  // Adresse
  const chatCompletion5 = await openai.chat.completions.create({
    model: 'gpt-3.5-turbo',
    messages: [
        {"role": "system", "content": "Please extract the Adresse from this text" + transcript}
        
    ]
})

  const Adresse = chatCompletion5.choices[0].message.content
  console.log(Adresse);


}

main();