/* SW starting point */
self.addEventListener('install', (event) => {
    self.channel = new MessageChannel();
    // TODO FILE: Check if we can block initialize and retrieve all data in SW on install, so we dont miss any fetches
    postTwoWayMsg('getJwtAccess').then((jwtAccess) => { console.log('intstall jwt', jwtAccess) })
    event.waitUntil(self.skipWaiting());
});

self.addEventListener('activate', (event) => {
    event.waitUntil(self.clients.claim());
    console.log('Activated');
});

/* Generic SW message listener, used for one way communication from page to SW */
self.addEventListener('message', (event) => {
    const { action } = event.data

    console.log('SW received message', event)

    if (action === 'init') {
        console.log('Init from page to sw receved', event)
        self.apiUrl = event.data.apiUrl
        self.toApi = new RegExp(`^${event.data.apiUrl}`);
        self.jwtAccess = event.data.jwtAccess
    } else if (action === 'jwtUpdate') {
        self.jwtAccess = event.data.jwtAccess
    } else {
        postOneWayMsg('error', { error: 'Unregistered SW message action received.'})
    }
});

// TODO FILE: Are there CSRF pitfalls? Only set header to our file API on get requests
self.addEventListener('fetch', event => {
    const url = new URL(event.request.url)
    console.log(self.jwtAccess, event)

    const toApi = new RegExp(`^http://localhost:8000/files`);
    if (toApi.test(url)) {
        console.log(event)
        let reqClone = event.request.clone();
        reqClone.headers['Authorization'] = `Bearer ${self.jwtAccess}`
        // event.respondWith(getResponse(event.request))
        // https://developer.mozilla.org/en-US/docs/Web/API/FetchEvent/respondWith
        console.log(reqClone)
        event.respondWith(fetch(reqClone))
    }

    if (url.origin == location.origin && url.pathname == '/dog.svg') {
    }
});

const getResponse = async request => {
    /* There is no simple way of adding a new a field to a request.
     * Therefore a copy of the request is created with the new fields already set */
    const headers = {};
    for (let entry of request.headers) {
        headers[entry[0]] = headers[entry[1]];
    }

    headers['Authorization'] = `Bearer ${self.jwtAccess}`
    const body = await ['HEAD', 'GET'].includes(request.method) ? Promise.resolve() : request.text();
    const bodyObj = body ? { body, } : {};

    return fetch(new Request(request.url, {
        method: request.method,
        headers,
        cache: request.cache,
        mode: 'cors', /* Navigate is not available, but can fall back to cors, which is good enough */
        credentials: request.credentials,
        redirect: 'manual', /* Allow the browser to handle redirect on its own */
        ...bodyObj,
    }));
};

/* Post a message without expecting a response in turn */
const postOneWayMsg = async (action, msgObj) => {
    const allClients = await self.clients.matchAll();
    const client = allClients.filter(client => client.type === 'window')[0];

    return new Promise((resolve, reject) => {
        if (!client) {
            reject(new Error(`SW could not find client for action: ${action} sending message: ${msgObj}`))
        }

        client.postMessage(
            { action, ...msgObj },
            [self.channel.port1]
        );

        resolve()
    });
}

/* Post a message, then wait for a response in turn */
const postTwoWayMsg = async (action, msgObj) => {
    return new Promise((resolve, reject) => {
        postOneWayMsg(action, msgObj)
            .then(() => {
                self.channel.port2.onmessage = (event) => {
                    if (event.data.error) {
                        console.log('Port error', event.error);
                        /* The actual error logging should be handled by the client */
                        reject(event.data.error);
                    }

                    console.log('Two way message success', event.data)
                    resolve(event.data);
                }
            })
            // TODO FILE: Send errors occuring in the SW only to Sentry as well
            .catch((error) => { reject(error) })
    });
}
