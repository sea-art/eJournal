<template>
    <b-card class="bread-crumb-card">

        <b-breadcrumb v-if="$route.params.assign != undefined" class="bread-crumb" :items="items.concat(' ')"/>
        <b-breadcrumb v-else-if="$route.params.course != undefined" class="bread-crumb" :items="items.slice(0, 1).concat(' ')"/>

        <h1>{{ currentPage }}</h1>

    </b-card>
</template>

<script>
export default {
    // props: {
    //     currentPage: String,
    //     links: Array
    // },
    props: ['currentPage', 'links'],
    data () {
        return {
            items: ~[{
                text: 'Courses',
                to: '/Home'
            }, {
                text: this.links[0],
                to: '/Home/' + this.links[0]
            }]
        }
    }
}
</script>

<style>
.bread-crumb-card {
    text-align: left;
    font-size: small;
    background-color: var(--theme-light-grey);

    margin-top: 20px;
    margin-bottom: 20px;

    border-width: 0px;
    border-left-width: 20px;
    border-left-color: red;
    border-radius: 0px;
}

.bread-crumb {
    font-size: large;
    font-style: italic;
    padding-left: 0px;
}
</style>
