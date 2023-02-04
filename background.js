
async function getCommittee(){

    const { Configuration, OpenAIApi } = require("openai");

    const configuration = new Configuration({
    apiKey: process.env.OPENAI_API_KEY,
    });
    const openai = new OpenAIApi(configuration);

    const response = await openai.createCompletion("text-curie-001", {
    prompt: "Write a blog post on vadala onions",
    temperature: 0.7,
    max_tokens: 256,
    top_p: 1,
    frequency_penalty: 0,
    presence_penalty: 0,
    });

    

    console.log(response.choices[0].text);
}

function sendtoAI(domContent) {
    console.log(domContent)
    // let json_data = {
    //     title: JSON.parse(domContent).title,
    //     h1: JSON.parse(domContent).h1,
    //     body: JSON.parse(domContent).body,
    // };

}

startNavigation.onclick.addListener(function(element) {

    chrome.tabs.sendMessage(tab.id, {text: 'report_back'}, sendtoAI)

})