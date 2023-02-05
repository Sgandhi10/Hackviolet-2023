
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
const paragraph = "lil baby is the best rapper of all time"
const committee = getAiResponse("Given these political committees: Transportation and Infrastructure, Judiciary, Science, Space, and Technology, Commerce, Science and Transportation, Indian Affairs , Strategic Competition between the United States and the Chinese Communist Party , Ways and Means, Veterans Affairs, Ethics, Financial Services, Budget, Natural Resources, Banking, Housing and Urban Affairs, Rules and Administration, House Administration, Education and the Workforce, Aging , Energy and Commerce, Small Business and Entrepreneurship, Finance, Homeland Security, Small Business, Oversight and Accountability, Ethics , Homeland Security and Governmental Affairs, Foreign Affairs, Tom Lantos Human Rights Commission, International Narcotics Control , Foreign Relations, Energy and Natural Resources, Agriculture, Rules, Health, Education, Labor and Pensions, Environment and Public Works, Intelligence , Agriculture, Nutrition and Forestry, Appropriations, Armed Services. Tell me which 2 committees are most relevant to the following paragraph:" + paragraph);
const data = { committee: 'example' };

var subcommittee = fetch("http://127.0.0.1:5000/subcommittee", {
            method: "POST",
            body: JSON.stringify({
              committee : committee
            }),
            headers: {
              "Content-type": "application/json; charset=UTF-8"
            }
          });
		//sendtoAI( tabs[0].url);
   
