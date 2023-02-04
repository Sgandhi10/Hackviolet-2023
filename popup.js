'use strict'


startNavigation.onclick = function (element) {
  console.log("startNavigation clicked")

  chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {

    fetch("http://127.0.0.1:5000", {
      method: "POST",
      body: JSON.stringify({
        url: tabs[0].url
      }),
      headers: {
        "Content-type": "application/json; charset=UTF-8"
      }
    });
    //sendtoAI( tabs[0].url);
  })
}



async function sendtoAI(taburl) {

  console.log("sendtoAI called")
  let page_title = document.title, page_h1_tag = '';

  if (document.querySelector("h1") !== null)
    page_h1_tag = document.querySelector("h1").textContent;

  // prepare JSON data with page title & first h1 tag
  let data = JSON.stringify({ title: page_title, h1: page_h1_tag });

  // // send message back to popup script
  let json_data = {
    title: JSON.parse(data).title,
    h1: JSON.parse(data).h1,
    url: taburl
  };

  let blob = new Blob([JSON.stringify(json_data)], { type: "application/json;charset=utf-8" });
  let objectURL = URL.createObjectURL(blob);
  chrome.downloads.download({ url: objectURL, filename: ('content/test/data.json'), conflictAction: 'overwrite' });
  console.log("json")




}


			// wait for 5 seconds







