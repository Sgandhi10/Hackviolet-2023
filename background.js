
require("dotenv").config();
const { Configuration, OpenAIApi } = require("openai");

const configuration = new Configuration({
  apiKey: process.env.OPENAI_API_KEY,
});

async function getAiResponse(topic) {
  const openai = new OpenAIApi(configuration);
  const completion = await openai.createCompletion({
    model: "text-davinci-003",
    prompt: topic,
    max_tokens: 1024,
    n: 1,
    stop: null,
    temperature: 0.7
  });
  console.log(completion.data.choices[0].text);
}
getAiResponse("Give me ice cream");