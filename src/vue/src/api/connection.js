import axios from 'axios'

export default {
    conn: axios.create({
        baseURL: 'http://localhost:8000/api/',
        withCredentials: true,
        transformRequest: [(data) => {
            print(data.data)
            return JSON.stringify(data.data)
        }],
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
    })
}