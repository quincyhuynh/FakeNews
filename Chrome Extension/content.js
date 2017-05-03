chrome.runtime.onMessage.addListener(
  function(request, sender, sendResponse){
    alert(request);
    var xhr = new XMLHttpRequest();
    xhr.open("GET", url + "?" + "url=" + request, true);
    xhr.onreadystatechange = function() {
        if (xhr.readyState == 4) {
        var resp = xhr.responseText;
        //chrome.runtime.sendMessage({updatePopup: true, data: resp});
        console.log("hi");
        sweetAlert("Hello world!");
    
        }
     }
     xhr.send();
);