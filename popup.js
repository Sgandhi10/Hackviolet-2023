'use strict'


startNavigation.onclick = function(element) {

    chrome.tabs.query({
        active: true,
        currentWindow: true
    }, async function(tabs) {
        getText(tabs[0].url)
    });

}

async function getText(url){

    chrome.tabs.update({url: url});
    chrome.runtime.onMessage.addListener(function getDOMInfo(message) {
        // remove onMessage event as it may get duplicated
        chrome.runtime.onMessage.removeListener(getDOMInfo);

        // save data from message to a JSON file and download
        let json_data = {
            title: JSON.parse(message).title,
            h1: JSON.parse(message).h1,
            url: url
        };

        let blob = new Blob([JSON.stringify(json_data)], {type: "application/json;charset=utf-8"});
        let objectURL = URL.createObjectURL(blob);
        chrome.downloads.download({ url: objectURL, filename: ('content/' + url_index + '/data.json'), conflictAction: 'overwrite' });
    });

    // execute content script
    chrome.tabs.executeScript({ file: 'script.js' }, function() {
        // resolve Promise after content script has executed
        resolve();
    });
}

