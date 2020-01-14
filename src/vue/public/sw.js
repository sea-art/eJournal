self.addEventListener('install', event => {
    console.log('V1 installing…');

    // cache a cat SVG
    event.waitUntil(
        caches.open('static-v1').then(cache => cache.add('/cat.svg'))
    );
});

self.addEventListener('activate', event => {
    clients.claim(); // If a page loads without a SW neither will its subresources so we claim the client.

    console.log('V1 now ready to handle fetches!');
});

// TODO FILE: Avoid CSRF pitfalls, only set header to our file API on get requests
// const toApi = new RegExp(`^${CustomEnv.API_URL}`)
self.addEventListener('fetch', event => {
    const url = new URL(event.request.url)
    // console.log(url)
    // console.log(event.request)

    // event.request.headers['Authorization'] = 'test'


    // if (toApi.test(url)) {
    // console.log(event)

    // serve the cat SVG from the cache if the request is
    // same-origin and the path is '/dog.svg'
    if (url.origin == location.origin && url.pathname == '/dog.svg') {
        event.respondWith(caches.match('/cat.svg'));
    }
    // }

    // event.respondWith(getResponse(event.request))
});

const getResponse = async request => {
    // there is no easy way to add
    // a new field to a request, so we
    // need to create a copy of a request with
    // a new field already set
    const headers = {};
    for (let entry of request.headers) {
        headers[entry[0]] = headers[entry[1]];
    }

    const { apiUrl, jwtAccess } = await getAuthInfo()

    // when we can't get auth token, we can try our best
    // and ask our user to log in
    // that situation may occur due to a lack of a page in scope,
    // auth token has expired or a user had a link from
    // some other external source
    if (jwtAccess === null) {
        // if a request was executed by clicking on a link
        // or changing window.location
        // we can redirect a user to ui login page
        if (request.mode === 'navigate') {
            return new Response(null, {
                status: 302,
                statusText: 'Found',
                headers: new Headers({
                    'location': '/login',
                })
            })
        }

        // if a request was executed using Ajax,
        // we can just return auth error
        return new Response(null, {
            status: 401,
            statusText: 'Unauthorized'
        });
    }

    headers['Authorization'] = `Bearer ${jwtAccess}`
    const body = await ['HEAD', 'GET'].includes(request.method) ? Promise.resolve() : request.text();
    const bodyObj = body ? { body, } : {};

    // we proceed with a request using Fetch API
    return fetch(new Request(request.url, {
        method: request.method,
        headers,
        cache: request.cache,
        mode: 'cors', // we cannot use mode 'navigate', but can fall back to cors, which is good enough
        credentials: request.credentials,
        redirect: 'manual', // browser will handle redirect on its own
        ...bodyObj,
    }));
};


const getAuthInfo = async () => {
    // we can't get a client that sent the current request, therefore we need
    // to ask any controlled page for auth token
    const allClients = await self.clients.matchAll();
    const client = allClients.filter(client => client.type === 'window')[0];

    // if there is no page in scope, we can't get any token
    // and we indicate it with null value
    if (!client) {
        console.log('No client found')
        return null;
    }

    // to communicate with a page we will use MessageChannels
    // they expose pipe-like interface, where a receiver of
    // a message uses one end of a port for messaging and
    // we use the other end for listening
    const channel = new MessageChannel();

    console.log('Requesting init from app');
    client.postMessage(
        { 'action': 'getAuthInfo' },
        [channel.port1]
    );

    // ports support only onmessage callback which
    // is cumbersome to use, so we wrap it with Promise
    return new Promise((resolve, reject) => {
        channel.port2.onmessage = event => {
            if (event.data.error) {
                console.log('Port error', event.error);
                reject(event.data.error);
            }

            console.log('Resolving auth')
            resolve(event.data);
        }
    });
};
