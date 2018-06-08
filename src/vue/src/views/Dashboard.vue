<template>
    <div class="dashboard">
        <h1>{{ msg }}</h1>

        <div v-for="names in courses">
            {{ names }}
        </div>

        <!-- <router-link tag="button" to="/Dashboard/PAV">PAV</router-link> -->
        <courseCard></courseCard>
    </div>
</template>

<script>
import courseCard from '@/components/courseCard'

export default {
    name: 'dashboard',
    data() {
        return {
            msg: "Dashboard",
            courses: {
                names: ["Webprogrammeren en databases project",
                        "Academische vaardigheden informatica 2",
                        "Academische vaardigheden informatica 1"],
                authors: ["Rob Belleman",
                          "Robert van Wijk",
                          "Robert van Wijk"],
                startdates: ["01-01-2017",
                             "01-01-2017",
                             "01-01-2017"]
            }
        }
    },
    components: {
        courseCard
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
