import axios from 'axios'

export default {
    conn: axios.create({
        baseURL: 'http://localhost:8000/',
        transformRequest: [(data) => JSON.stringify(data)],
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
    })
}
