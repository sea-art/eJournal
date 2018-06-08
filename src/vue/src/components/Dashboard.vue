<template>
    <div class="dashboard">
        <h1>{{ msg }}</h1>

        <!-- Get these by ajax json -->
        <router-link tag="button" to="/Dashboard/PAV">PAV</router-link>
        <Deadline></Deadline>
    </div>
</template>

<script>
import Deadline from '@/components/Deadline'

export default {
    name: 'dashboard',
    data () {
        return {
            msg: 'Dashboard'
        }
    },
    components: {
        Deadline
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
