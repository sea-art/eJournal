<template>
    <b-row no-gutters>
        <b-col lg="3" order="3" order-lg="1" class="left-content d-none d-lg-block"></b-col>
        <b-col md="12" lg="6" order="2" class="main-content">
            <h1>Home Page</h1>
            <div v-for="c in courses" :key="c.cID">
                <b-link tag="b-button" :to="{ name: 'Course', params: {course: c.cID} }">
                    <main-card :line1="c.name" :line2="c.date"> <!-- TODO Enter obj3 --> </main-card>
                </b-link>
            </div>
        </b-col>
        <b-col md="12" lg="3" order="1" order-lg="3" class="right-content"></b-col>
    </b-row>
</template>

<script>
import mainCard from '@/components/MainCard.vue'

export default {
    name: 'Home',
    data () {
        return {
            courses: [{
                name: 'Webprogrammeren en databases project',
                auth: 'Rob Belleman',
                date: '01-01-2017',
                abbr: 'WDB7',
                cID: '2017WDB'
            }, {
                name: 'Academische vaardigheden informatica 2',
                auth: 'Robert van Wijk',
                date: '01-01-2017',
                abbr: 'AVI2',
                cID: '2017AVI2'
            }, {
                name: 'Academische vaardigheden informatica 1',
                auth: 'Robert van Wijk',
                date: '01-01-2017',
                abbr: 'AVI1',
                cID: '2017AVI1'
            }]
        }
    },
    components: {
        'main-card': mainCard
    }
}
</script>
