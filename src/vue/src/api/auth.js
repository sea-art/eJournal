import axios from 'axios'

export default {
  login(username, password) {
    response = axios.post('/api/token/', { 'username': username, 'password': password })
    response.json()
  },
  logout() {
    // Remove token
  },
};
