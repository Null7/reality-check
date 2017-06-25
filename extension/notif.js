  var notifOptions = {
											type: "basic",
			                iconUrl: "fake-news.jpg",
			                title: "Warning!!! Fake News!",
			                message: "This is a fake! Do not trust!"

													};
                chrome.notifications.create(notifOptions, callback);

            function callback(){
								console.log('fake news!');
						}
