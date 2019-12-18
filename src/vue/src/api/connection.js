import axios from 'axios'
import store from '@/store'

axios.defaults.baseURL = CustomEnv.API_URL

const conn = axios.create({
    transformRequest: [(data, headers) => {
        if (store.getters['user/jwtAccess']) { headers.Authorization = `Bearer ${store.getters['user/jwtAccess']}` }
        return data
    }, ...axios.defaults.transformRequest],
})

// An instance without refresh interceptor
const connRefresh = axios.create({
    transformRequest: [(data, headers) => {
        if (store.getters['user/jwtAccess']) { headers.Authorization = `Bearer ${store.getters['user/jwtAccess']}` }
        return data
    }, ...axios.defaults.transformRequest],
})

const connFile = axios.create({
    transformRequest: [(data, headers) => {
        if (store.getters['user/jwtAccess']) { headers.Authorization = `Bearer ${store.getters['user/jwtAccess']}` }
        return data
    }, ...axios.defaults.transformRequest],
    responseType: 'arraybuffer', // TODO FILE: We no longer use base64 images -> this can be merged and removed
    headers: {
        'Content-Type': 'multipart/form-data',
    },
})

// TODO FILE: Merge or delete with above
const connFileEmail = axios.create({
    transformRequest: [(data, headers) => {
        if (store.getters['user/jwtAccess']) { headers.Authorization = `Bearer ${store.getters['user/jwtAccess']}` }
        return data
    }, ...axios.defaults.transformRequest],
    headers: {
        'Content-Type': 'multipart/form-data',
    },
})

const connSentry = axios.create({
    /* /api/0/projects/{organization_slug}/{project_slug}/ */
    baseURL: `https://sentry.io/api/0/projects/${CustomEnv.SENTRY_ORGANIZATION_SLUG}/${CustomEnv.SENTRY_PROJECT_SLUG}/`,
    headers: {
        Authorization: `DSN ${CustomEnv.SENTRY_DSN}`,
    },
})

export default {
    conn,
    connRefresh,
    connFile,
    connFileEmail,
    connSentry,
}
