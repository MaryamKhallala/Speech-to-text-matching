const { MongoClient } = require('mongodb');

const url = "mongodb://127.0.0.1:27017/";
const dbName = "mydb";
const client = new MongoClient(url);

async function insertDocument() {
  try {
    await client.connect();
    console.log("Connected successfully to server");

    const db = client.db(dbName);
    const collection = db.collection("CV");

    const myobj = { Name: Name, job_title: job_title, Phone: Phone, Email: Email, Adresse: Adresse, Birthday:Birthday, Skills: Skills, Education: Education, Experience: experience, Projects: projets, Interets: interets };

    const result = await collection.insertOne(myobj);
    console.log(`${result.insertedCount} document inserted`);
  } finally {
    await client.close();
  }
}

insertDocument().catch(err => console.error(err));
