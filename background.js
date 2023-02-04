'use strict';

// activate extension when host is www.website.com
chrome.runtime.onInstalled.addListener(function() {
	chrome.declarativeContent.onPageChanged.removeRules(undefined, function() {
		chrome.declarativeContent.onPageChanged.addRules([{
				conditions: [new chrome.declarativeContent.PageStateMatcher({
					pageUrl: {hostEquals: 'https://www.cnn.com/2023/02/04/us/heidi-broussard-murder-fieramusca-guilty-plea/index.html'},
				})
			],
		    actions: [new chrome.declarativeContent.ShowPageAction()]
		}]);
	});
});