  var notifOptions = {
											type: "basic",
			                iconUrl: "fake-news.jpg",
			                title: "Fake News!",
			                message: "This is a fake news"

													};
                chrome.notifications.create(notifOptions, callback);

            function callback(){
								console.log('fake news!');
						}
