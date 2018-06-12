<template>
    <b-row>
        <b-col cols="3" class="left-content"></b-col>
        <b-col cols="6" class="main-content">
            <h1>Home Page</h1>
            <div v-for="c in courses" :key="c.cID">
                <b-link tag="b-button" :to="{name: 'Course', params: {course: c.cID}}">
                    <main-card :line1="c.name" :line2="c.date" :color="set_color()">hoi</main-card>
                </b-link>
            </div>
        </b-col>
        <b-col cols="3" class="right-content">

        </b-col>
    </b-row>
</template>

<script>
import mainCard from '@/components/MainCard.vue'

export default {
    name: 'Home',
    data () {
        return {
            /* Define the banner colors and set the index to -1 for first setup. */
            colors: ["pink-border", "peach-border", "blue-border"],
            color_idx: -1,
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
            }],
            deadlines: [{
                name: 'Individueel logboek',
                vak: 'WEDA',
                datetime: '8-6-2018 13:00'
            }, {
                name: 'Logboek academia',
                vak: 'AVI2',
                datetime: '8-6-2018 13:00'
            }, {
                name: 'Individueel logboek',
                vak: 'AVI1, AVI2',
                datetime: '8-6-2018 13:00'
            }]
        }
    },
    methods: {
        set_color() {
            this.color_idx + 1 == this.colors.length ? this.color_idx = 0 : this.color_idx++
            return this.colors[this.color_idx];
        }
    },
    components: {
        'main-card': mainCard
    }
}
</script>
