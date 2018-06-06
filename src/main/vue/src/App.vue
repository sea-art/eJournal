<template>
  <div id="app">
    <img src="./assets/logo.png">
    <div>
      <ul>
        <li><router-link to="/">Hello</router-link></li>
        <li><router-link to="/Courses/PAV">Courses</router-link></li>
        <li><router-link to="/Courses/PAV/Colloquium">Assignment</router-link></li>
        <li><router-link to="/Courses/PAV/Colloquium/Dennis">Journal</router-link></li>
      </ul>
    </div>
    <router-view/>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
