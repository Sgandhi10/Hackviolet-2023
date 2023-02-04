'use strict'




chrome.runtime.onMessage.addListener(function (msg, sender, sendResponse) {

    if(msg.text == "report back"){

        sendResponse(document[0].outerHTML);
    }
})

