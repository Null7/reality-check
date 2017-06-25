// Copyright (c) 2014 The Chromium Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

/**
 * Get the current URL.
 *
 * @param {function(string)} callback - called when the URL of the current tab
 *   is found.
 */
function getCurrentTabUrl(callback) {
  // Query filter to be passed to chrome.tabs.query - see
  // https://developer.chrome.com/extensions/tabs#method-query
  var queryInfo = {
    active: true,
    currentWindow: true
  };

  chrome.tabs.query(queryInfo, function(tabs) {
    // chrome.tabs.query invokes the callback with a list of tabs that match the
    // query. When the popup is opened, there is certainly a window and at least
    // one tab, so we can safely assume that |tabs| is a non-empty array.
    // A window can only have one active tab at a time, so the array consists of
    // exactly one tab.
    var tab = tabs[0];

    // A tab is a plain object that provides information about the tab.
    // See https://developer.chrome.com/extensions/tabs#type-Tab
    var url = tab.url;

    // tab.url is only available if the "activeTab" permission is declared.
    // If you want to see the URL of other tabs (e.g. after removing active:true
    // from |queryInfo|), then the "tabs" permission is required to see their
    // "url" properties.
    console.assert(typeof url == 'string', 'tab.url should be a string');

    callback(url);
  });

  // Most methods of the Chrome extension APIs are asynchronous. This means that
  // you CANNOT do something like this:
  //
  // var url;
  // chrome.tabs.query(queryInfo, function(tabs) {
  //   url = tabs[0].url;
  // });
  // alert(url); // Shows "undefined", because chrome.tabs.query is async.
}

/**
 * @param {string} newsUrl - url to parse.
 * @param {function(string)} callback - Called when an image has
 *   been found. The callback gets the URL, width and height of the image.
 * @param {function(string)} errorCallback - Called when the image is not found.
 *   The callback gets a string that describes the failure reason.
 */
function getMetaData(newsUrl, callback, errorCallback) {
  // Only works when you have the server running
  var url = `https://document-parser-api.lateral.io/?url=${newsUrl}`;
  // var url = "http://localhost:3000/api/parse/?url=" + newsUrl;
  var x = new XMLHttpRequest();
  if (!x) {
    alert('Giving up :( Cannot create an XMLHTTP instance');
    return false;
  }
  x.open('GET', url);
  x.setRequestHeader('content-type', 'application/json');
  x.setRequestHeader('subscription-key', '0b8b238af3bae8b43e6b8f27e0b76377')
  x.responseType = "json";
  x.onload = function() {
    // Parse and process the response from the server
    var response = x.response;
    console.log(response);
    // if (!response || !response.responseData || !response.responseData.results ||
    //     response.responseData.results.length === 0) {
    //   errorCallback('No response from the parser!');
    //   return;
    // }

    callback(response);
  };
  x.onerror = function(erro) {
    errorCallback('Network error.');
  };
  x.send();
}

function renderStatus(statusText) {
  document.getElementById('status').textContent = statusText;
}

document.addEventListener('DOMContentLoaded', function() {
  getCurrentTabUrl(function(url) {
    // Put the image URL in Google search.
    renderStatus('Parsing url: ' + url);

    getMetaData(url, (result) => {
      renderStatus(JSON.stringify(result, null, 4));
    }, function(errorMessage) {
      renderStatus('Cannot parse article ' + errorMessage);
    });
  });
});
