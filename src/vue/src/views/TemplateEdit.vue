<template>
    <content-single-column>
        <b-card slot="main-content-column" class="no-hover">
            <b-input class="mb-2 mr-sm-2 mb-sm-0 multi-form" id="templateName" v-model="name" placeholder="name" required/>
            <draggable v-model="fields" @start="drag=true" @end="drag=false" @update="onUpdate" :options="{ handle:'.handle' }">
                <div v-for="field in fields" :key="field.tag">
                    <b-card class="field-card">
                        <b-row align-h="between">
                            <b-col cols="12" md="11">
                                <b-input class="mb-2 mr-sm-2 mb-sm-0 multi-form" v-model="field.title" placeholder="title" required/>
                                <b-select :options="fieldTypes"></b-select>
                            </b-col>
                            <b-col cols="12" md="1" class="handle">
                                <icon class="move-icon" name="arrows" scale="1.75"></icon>
                            </b-col>
                        </b-row>
                    </b-card>
                </div>
            </draggable>
            <b-card class="hover" @click="addField">+ Add field</b-card>
            <b-button @click="onSubmit" :to="{name: 'Course', params: {cID: 1}}">Save</b-button>
            <!-- {{ fields }} -->
        </b-card>

    </content-single-column>
</template>

<script>
import contentSingleColumn from '@/components/ContentSingleColumn.vue'
import icon from 'vue-awesome/components/Icon'
import courseApi from '@/api/course.js'
import draggable from 'vuedraggable'

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
            name: 'Template title',
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
            }],
            fieldTypes: {
                'i': 'Image',
                't': 'Text',
                'f': 'File'
            }
        }
    },
    components: {
        'content-single-column': contentSingleColumn,
        'icon': icon,
        'draggable': draggable
    },
    methods: {
        onSubmit () {
            console.log('submit')
        },
        addField () {
            console.log('addField')
            var tag = this.fields[this.fields.length - 1].tag + 1
            var type = 't'
            var title = 'Field title'
            var location = this.fields.length

            var newField = {
                'tag': tag,
                'type': type,
                'title': title,
                'location': location
            }

            this.fields.push(newField)
        },
        onUpdate () {
            console.log('hihih')
        }
    }
}
</script>

<style>
#templateName {
    font-weight: bold;
    font-size: 35px;
    font-family: 'Roboto', sans-serif;
    color: var(--theme-dark-blue);
}

.field-card {
    background-color: var(--theme-medium-grey);
}

.sortable-chosen .card {
    background-color: var(--theme-dark-grey)
}

.sortable-ghost {
    visibility: hidden;
}

.sortable-drag .card {
    visibility: visible;
}

.handle {
    cursor: grab;
    text-align: center;
    padding: 20px 0px 0px 0px;
}

.move-icon {
    fill: var(--theme-dark-grey)
}

.field-card:hover .move-icon {
    fill: var(--theme-dark-blue);
}
</style>
