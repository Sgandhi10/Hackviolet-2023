'use strict'


startNavigation.onclick = function(element) {
    console.log("startNavigation clicked")

    chrome.tabs.query({active: true, currentWindow: true}, function(tabs){
		
			// navigate to next url
		sendtoAI( tabs[0].url);
    })
}



async function sendtoAI(taburl) {
   
    console.log("sendtoAI called")
    await getDOM()
    //chrome.tabs.sendMessage(document[0].outerHTML);
    //getDOM();
    // chrome.runtime.onMessage.addListener(function getDOMInfo(message) {
    //     // remove onMessage event as it may get duplicated
    //     chrome.runtime.onMessage.removeListener(getDOMInfo);

    //     // save data from message to a JSON file and download
    //     let json_data = {
    //         title: JSON.parse(message).title,
    //         h1: JSON.parse(message).h1,
    //         url: url
    //     };

    //     let blob = new Blob([JSON.stringify(json_data)], {type: "application/json;charset=utf-8"});
    //     let objectURL = URL.createObjectURL(blob);
    //     chrome.downloads.download({ url: objectURL, filename: ('content/' + url_index + '/data.json'), conflictAction: 'overwrite' });
    // });


}

async function getDOM() {
    console.log("getDOM called")
    let page_title = document.title, page_h1_tag = '';

if(document.querySelector("h1") !== null)
	page_h1_tag = document.querySelector("h1").textContent;

// prepare JSON data with page title & first h1 tag
 let data = JSON.stringify({ title: page_title, h1: page_h1_tag });

// // send message back to popup script
 //chrome.runtime.sendMessage(null, data);
}
			
			// wait for 5 seconds
		
		





