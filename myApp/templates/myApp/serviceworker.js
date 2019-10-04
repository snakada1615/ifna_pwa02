/*
 Copyright 2016 Google Inc. All Rights Reserved.
 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at
     http://www.apache.org/licenses/LICENSE-2.0
 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
*/

// Names of the two caches used in this version of the service worker.
// Change to v2, etc. when you update any of the local resources, which will
// in turn trigger the install event again.
//const PRECACHE = 'precache-v1';
var PRECACHE = "django-pwa-v" + new Date().getTime();

const RUNTIME = 'runtime';

// A list of local resources we always want to be cached.
const PRECACHE_URLS = [
//  '/css/django-pwa-app.css',
  'test/',
  'usage/',
  'who/',
  'offline/',
  '/static/css/bootstrap.min.css',
  '/static/js/bootstrap.bundle.min.js',
  '/static/js/jquery-3.4.1.min.js',
  '/static/js/vue.js',
  '/static/img/icons/chef72.png',
  '/static/img/icons/chef96.png',
  '/static/img/icons/chef128.png',
  '/static/img/icons/chef144.png',
  '/static/img/icons/chef152.png',
  '/static/img/icons/chef192.png',
  '/static/img/icons/chef384.png',
  '/static/img/icons/chef512.png',
  '/static/img/mother and child 640.png'
];

/**
 * Returns a promise that resolves with an ID token if available.
 * @return {!Promise<?string>} The promise that resolves with an ID token if
 *     available. Otherwise, the promise resolves with null.
 */
const getIdToken = () => {
  return new Promise((resolve, reject) => {
    const unsubscribe = firebase.auth().onAuthStateChanged((user) => {
      unsubscribe();
      if (user) {
        user.getIdToken().then((idToken) => {
          resolve(idToken);
        }, (error) => {
          resolve(null);
        });
      } else {
        resolve(null);
      }
    });
  });
};

const getOriginFromUrl = (url) => {
  // https://stackoverflow.com/questions/1420881/how-to-extract-base-url-from-a-string-in-javascript
  const pathArray = url.split('/');
  const protocol = pathArray[0];
  const host = pathArray[2];
  return protocol + '//' + host;
};

/**
 * Returns a promise that resolves with an ID token if available.
 * @return {!Promise<?string>} The promise that resolves with an ID token if
 *     available. Otherwise, the promise resolves with null.
 */


// The install handler takes care of precaching the resources we always need.
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(PRECACHE)
      .then(cache => cache.addAll(PRECACHE_URLS))
      .then(self.skipWaiting())
  );
});

// The activate handler takes care of cleaning up old caches.
self.addEventListener('activate', event => {
  const currentCaches = [PRECACHE, RUNTIME];
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return cacheNames.filter(cacheName => !currentCaches.includes(cacheName));
    }).then(cachesToDelete => {
      return Promise.all(cachesToDelete.map(cacheToDelete => {
        return caches.delete(cacheToDelete);
      }));
    }).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', function(event) {
  // every request from our site, passes through the fetch handler
  // I have proof
  console.log('I am a request with url: ',
   event.request.clone().url)

  if (event.request.clone().method === 'GET') {
    event.respondWith(
      // check all the caches in the browser and find
      // out whether our request is in any of them
      caches.match(event.request.clone())
        .then(function(response) {
          if (response) {
            // if we are here, that means there's a match
            //return the response stored in browser
            return response;
          }
          // no match in cache, use the network instead
          return fetch(event.request.clone());
        }
      )
    );
  } else if (event.request.clone().method === 'POST') {
    // attempt to send request normally

     //*
     //*
     //*
     const requestProcessor = (idToken) => {
       let req = event.request;
       // For same origin https requests, append idToken to header.
       if (self.location.origin == getOriginFromUrl(event.request.url) &&
           (self.location.protocol == 'https:' ||
            self.location.hostname == 'localhost') &&
           idToken) {
         // Clone headers as request headers are immutable.
         const headers = new Headers();
         for (let entry of req.headers.entries()) {
           headers.append(entry[0], entry[1]);
         }
         // Add ID token to header.
         headers.append('Authorization', 'Bearer ' + idToken);
         try {
           req = new Request(req.url, {
             method: req.method,
             headers: headers,
             mode: 'same-origin',
             credentials: req.credentials,
             cache: req.cache,
             redirect: req.redirect,
             referrer: req.referrer,
             body: req.body,
             bodyUsed: req.bodyUsed,
             context: req.context
           });
         } catch (e) {
           // This will fail for CORS requests. We just continue with the
           // fetch caching logic below and do not pass the ID token.
         }
       }
     };

    //*
    //*
    //*

    event.respondWith(fetch(req).catch(function
    (error) {
      // only save post requests in browser, if an error occurs
      //savePostRequests(event.request.clone().url, form_data)
      console.log('local save function not available')
    }))
  };
});

/*
https://stackoverflow.com/questions/38986351/serviceworker-cache-all-failed-post-requests-when-offline-and-resubmit-when-on
// Cache signature post request
    //This retrieves all the information about the POST request including the formdata body, where the URL contains updateSignature.
// Resubmit offline signature requests
    //This resubmits all cached POST results and then empties the array.

self.addEventListener('fetch', function(event) {
    // Intercept all fetch requests from the parent page
    event.respondWith(
        caches.match(event.request)
        .then(function(response) {
            // Cache signature post request
            if (event.request.url.includes('updateSignature') && !navigator.onLine) {
                var request = event.request;
                var headers = {};
                for (var entry of request.headers.entries()) {
                    headers[entry[0]] = entry[1];
                }
                var serialized = {
                    url: request.url,
                    headers: headers,
                    method: request.method,
                    mode: request.mode,
                    credentials: request.credentials,
                    cache: request.cache,
                    redirect: request.redirect,
                    referrer: request.referrer
                };
                request.clone().text().then(function(body) {
                    serialized.body = body;
                    callsToCache.push(serialized);
                    console.log(callsToCache);
                });
            }
            // Immediately respond if request exists in the cache and user is offline
            if (response && !navigator.onLine) {
                return response;
            }
            // Resubmit offline signature requests
            if(navigator.onLine && callsToCache.length > 0) {
                callsToCache.forEach(function(signatureRequest) {
                    fetch(signatureRequest.url, {
                        method: signatureRequest.method,
                        body: signatureRequest.body
                    })
                });
                callsToCache = [];
            }


            // IMPORTANT: Clone the request. A request is a stream and
            // can only be consumed once. Since we are consuming this
            // once by cache and once by the browser for fetch, we need
            // to clone the response
            var fetchRequest = event.request.clone();

            // Make the external resource request
            return fetch(fetchRequest).then(
                function(response) {
                // If we do not have a valid response, immediately return the error response
                // so that we do not put the bad response into cache
                if (!response || response.status !== 200 || response.type !== 'basic') {
                    return response;
                }

                // IMPORTANT: Clone the response. A response is a stream
                // and because we want the browser to consume the response
                // as well as the cache consuming the response, we need
                // to clone it so we have 2 stream.
                var responseToCache = response.clone();

                // Place the request response within the cache
                caches.open(CACHE_NAME)
                .then(function(cache) {
                    if(event.request.method !== "POST")
                    {
                        cache.put(event.request, responseToCache);
                    }
                });

                return response;
            }
            );
        })
    );
});
*/
