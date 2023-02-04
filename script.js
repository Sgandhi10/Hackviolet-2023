let page_title = document.title,
	page_h1_tag = '';

if(document.querySelector("h1") !== null)
	page_h1_tag = document.querySelector("h1").textContent;

// prepare JSON data with page title & first h1 tag
let data = JSON.stringify({ title: page_title, h1: page_h1_tag });

// send message back to popup script
chrome.runtime.sendMessage(null, data);