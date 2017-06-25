var menuItem = {
    "id": "fakeNewsId",
    "title": "Fake Validation",
    "contexts": ["selection"]
};

function isInt(value) {
  return !isNaN(value) &&
         parseInt(Number(value)) == value &&
         !isNaN(parseInt(value, 10));
}

chrome.contextMenus.create(menuItem);

chrome.contextMenus.onClicked.addListener(function(clickData){
    if (clickData.menuItemId == "fakeNewsId" && clickData.selectionText){
        if (isInt(clickData.selectionText)){
            chrome.storage.sync.get(['fakeNews','percent'], function(budget){
                var newfakeNews = 0;
                if (budget.total){
                    newTotal += parseInt(fake.percent);
                }

                newTotal += parseInt(clickData.selectionText);
                chrome.storage.sync.set({'fakeNews': newfakeNews}, function(){

                    var notifOptions = {
											type: "basic",
											iconUrl: "icon.png",
											title: "Fake News!",
											message: "This is a fake news"
										};
                    chrome.notifications.create('id', notifOptions);


                });
            });
        }
    }
});
