var url = "http://quincyhuynh.pythonanywhere.com/predict";

window.onload=function(){
    chrome.tabs.query({currentWindow: true, active: true}, function(tabs){
    	makeRequest(tabs[0].url);
	});
}

function makeRequest(tab_url) {
	// how to fetch tab url using activeInfo.tabid
    console.log(tab_url);
	var xhr = new XMLHttpRequest();
	xhr.open("GET", url + "?" + "url=" + tab_url, true);
	xhr.onreadystatechange = function() {
  		if (xhr.readyState == 4) {
			resp = xhr.responseText;
			chrome.runtime.sendMessage({updatePopup: true, data: resp});
			console.log(resp);
			document.getElementById("resp").innerHTML = resp;
			//swal("Hello world!"); 
	
  		}
  	}
 	xhr.send();
}