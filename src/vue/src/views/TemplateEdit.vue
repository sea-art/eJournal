<template>
    <content-single-column>
        <h1 slot="main-content-column">{{pageName}}</h1>
        <b-card slot="main-content-column" class="card no-hover">
            <b-form @submit="onSubmit">
                <b-input class="mb-2 mr-sm-2 mb-sm-0 multi-form" v-model="name" :placeholder="field.name" required/>
                <b-button type="submit">Update Settings</b-button>
                <b-button :to="{name: 'Course', params: {cID: 1}}">Back</b-button>
                <br/>
            </b-form>
        </b-card>
    </content-single-column>
</template>

<script>
import contentSingleColumn from '@/components/ContentSingleColumn.vue'
import courseApi from '@/api/course.js'

export default {
    name: 'TemplateEdit',
    props: {
        cID: {
            required: true
        },
        aID: {
            required: true
        },
        tID: {
            required: true
        }
    },
    data () {
        return {
            name: '',
            fields: [{
                'tag': 0,
                'type': 't',
                'title': 'Evenementnaam',
                'location': 0
            }, {
                'tag': 1,
                'type': 't',
                'title': 'Naam spreker',
                'location': 1
            }, {
                'tag': 2,
                'type': 't',
                'title': 'Aantal punten',
                'location': 2
            }]
        }
    },
    components: {
        'content-single-column': contentSingleColumn
    },
    methods: {
    }
}
</script>
