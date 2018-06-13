<template>
    <b-row>
        <b-col cols="3" class="left-content"></b-col>
        <b-col cols="6" class="main-content">
            <bread-crumb :links="[$route.params.course]" :currentPage="'Colloqiumlogboek'"></bread-crumb>

        </b-col>
        <b-col cols="3" class="right-content"></b-col>
    </b-row>
</template>

<script>
import breadCrumb from '@/components/BreadCrumb.vue'

export default {
    name: 'Assignment',
    data () {
        return {
            assignments: [{
                name: 'Colloqiumlogboek',
                auth: 'Robert van Wijk',
                progress: '4/10'
            }]
        }
    },
    components: {
        'bread-crumb': breadCrumb
    }
}
</script>
