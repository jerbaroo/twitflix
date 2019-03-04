let changeColor = document.getElementById('changeColor');

// Set button to colour from storage.
chrome.storage.sync.get('color', function(data) {
  changeColor.style.backgroundColor = data.color;
  changeColor.setAttribute('value', data.color);
});

// Change current page to button colour on button click.
changeColor.onclick = function(element) {
  let color = element.target.value;
  chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
    chrome.tabs.executeScript(
      tabs[0].id,
      {code: 'document.body.style.backgroundColor = "' + color + '";'});
  });
};
