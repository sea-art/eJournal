<template>
    <b-row>
        <b-col cols="3" class="left-content"></b-col>
        <b-col cols="6" class="main-content">
            <bread-crumb :links="['test', 'test2']" :currentPage="'Courses'"></bread-crumb>

            <div v-for="c in courses" :key="c.cID">
                <b-link tag="b-button" :to="{ name: 'Course', params: {course: c.cID} }">
                    <main-card :line1="c.name" :line2="c.date"> <!-- Enter obj3 --> </main-card>
                </b-link>
            </div>
        </b-col>
        <b-col cols="3" class="right-content"></b-col>
    </b-row>
</template>

<script>
import breadCrumb from '@/components/BreadCrumb.vue'
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
        'bread-crumb': breadCrumb,
        'main-card': mainCard
    }
}
</script>
