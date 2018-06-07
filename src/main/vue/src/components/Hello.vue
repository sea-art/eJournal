<template>
    <div class="hello">
        <h1>{{ msg }}</h1>

        <!-- Get these by ajax json -->
        <router-link tag="button" to="/Courses/PAV">PAV</router-link>

    </div>
</template>

<script>
export default {
    name : 'hello',
    data () {
        return {
            msg : 'Courses',
        }
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1, h2 {
  font-weight: normal;
}
ul {
    list-style-position: inside;
}
a {
  color: #42b983;
}
</style>
