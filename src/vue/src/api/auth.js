import connection from '@/api/connection'

export default {
    login(username, password) {
      connection.conn.post('/token/', {data: {username: 'rick', password: 'admin123'}}, {headers: {'Content-Type': 'application/json' }})
          .then(response => {
          console.log(response)
          })
          .catch(error => {
            console.error(error)
          })
      },
    logout() {
        localStorage.removeItem('jwt')
    },
}
