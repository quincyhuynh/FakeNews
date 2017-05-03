var url = "http://quincyhuynh.pythonanywhere.com/predict";

// chrome.browserAction.onClicked.addListener(function(tab){
//   console.log("hii");
//   chrome.tabs.query({active: true, currentWindow: true}, function(tabs){
//     chrome.tabs.sendMessage(tabs[0].id, {action: "SendIt"}, function(response) {});  
//   });
// });

// chrome.browserAction.onClicked.addListener(function (tab){
// 	var xhr = new XMLHttpRequest();
// 	xhr.open("GET", url + "?" + "url=" + tab.url, true);
// 	xhr.onreadystatechange = function() {
//   		if (xhr.readyState == 4) {
// 			var resp = xhr.responseText;
// 			//chrome.runtime.sendMessage({updatePopup: true, data: resp});
// 			console.log(resp);
// 			sweetAlert("Hello world!");
	
//   		}
//   	}
//  	xhr.send();
// });



// chrome.tabs.onUpdated.addListener(function(tabId, activeInfo) {
// 	if (activeInfo.status == "complete") {
// 		chrome.tabs.get(tabId, function(tab){
//   			makeRequest(tab.url);
//   		});  
// 	}
// });

// chrome.tabs.onUpdated.addListener(function(tabId, activeInfo)) {
// 	if (activeInfo.status == "complete") {
// 		console.log("hii");
//   		chrome.tabs.query({active: true, currentWindow: true}, function(tabs){
//     		chrome.tabs.sendMessage(tabs[0].id, {action: "SendIt"}, function(response) {});  
//   		});
// 	}
// }


// chrome.tabs.onActivated.addListener(function(activeInfo) {
// 	chrome.tabs.get(activeInfo.tabId, function(tab){
//   		makeRequest(tab.url);
//   	});  
  
// }); 

var resp; 

function makeRequest(tab_url) {
	// how to fetch tab url using activeInfo.tabid
  
	var xhr = new XMLHttpRequest();
	xhr.open("GET", url + "?" + "url=" + tab_url, true);
	xhr.onreadystatechange = function() {
  		if (xhr.readyState == 4) {
			resp = xhr.responseText;
			chrome.runtime.sendMessage({updatePopup: true, data: resp});
			console.log(resp);
	
  		}
  	}
 	xhr.send();
}


