<template>
    <div>
        <h4>
            <b-breadcrumb v-if="$route.params.student != undefined" class="bread-crumb" :items="items.concat(' ')"/>
            <b-breadcrumb v-else-if="$route.params.assign != undefined" class="bread-crumb" :items="items.slice(0, 2).concat(' ')"/>
            <b-breadcrumb v-else-if="$route.params.course != undefined" class="bread-crumb" :items="items.slice(0, 1).concat(' ')"/>
        </h4>
        <h1>
            {{ currentPage }}
        </h1>
    </div>
</template>

<script>
export default {
    props: ['currentPage'],
    data () {
        return {
            items: [{
                text: 'Courses',
                to: '/Home'
            }, {
                text: this.$route.params.course,
                to: '/Home/' + this.$route.params.course
            }, {
                text: this.$route.params.assign,
                to: '/Home/' + this.$route.params.course + '/' + this.$route.params.assign
            }]
        }
    }
}
</script>

<style>
.bread-crumb {
    padding: 0px;
    background-color: var(--theme-medium-grey);
    margin-bottom: 0px;
}
</style>
