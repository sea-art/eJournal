import axios from 'axios'
import store from '@/store'

const conn = axios.create()
const connRefresh = axios.create() // An instance without refresh interceptor
const connFile = axios.create({
    responseType: 'arraybuffer',
    headers: {
        'Content-Type': 'multipart/form-data',
    },
})
const connFileEmail = axios.create({
    headers: {
        'Content-Type': 'multipart/form-data',
    },
})

store.dispatch('connection/setupConnectionInterceptors', { connection: conn })
store.dispatch('connection/setupConnectionInterceptors', { connection: connRefresh, isRefresh: true })
store.dispatch('connection/setupConnectionInterceptors', { connection: connFile })
store.dispatch('connection/setupConnectionInterceptors', { connection: connFileEmail })

export default {
    conn,
    connRefresh,
    connFile,
    connFileEmail,
}
