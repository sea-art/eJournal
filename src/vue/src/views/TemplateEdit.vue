<template>
    <div>
        <b-card class="no-hover">
            <b-input class="mb-2 mr-sm-2 mb-sm-0 multi-form" id="templateName" v-model="name" placeholder="Template name" required/>
            <draggable v-model="this.template.fields" @start="drag=true" @end="drag=false" @update="onUpdate" :options="{ handle:'.handle' }">
                <div v-for="field in this.template.fields" :key="field.location">
                    <b-card class="field-card">
                        <b-row align-h="between" no-gutters>
                            <b-col cols="12" md="11">
                                <b-input class="mb-2 mr-sm-2 mb-sm-0 multi-form" v-model="field.title" placeholder="Field title" required/>
                                <b-select :options="fieldTypes" v-model="field.type"></b-select>
                            </b-col>
                            <b-col cols="12" md="1">
                                <div class="icon-box">
                                    <div class="handle">
                                        <icon class="move-icon" name="arrows" scale="1.75"></icon>
                                    </div>
                                    <div class="trash-box" @click="removeField(field.location)">
                                        <icon class="trash-icon" name="trash" scale="1.75"></icon>
                                    </div>
                                </div>
                            </b-col>
                        </b-row>
                    </b-card>
                </div>
                <div style="visibility: hidden;"></div>
            </draggable>
            <b-card class="hover" @click="addField">+ Add field</b-card>
            <b-button @click="onSubmit" :to="{name: 'Course', params: {cID: 1}}">Save</b-button>
        </b-card>
    </div>
</template>

<script>
import ContentSingleColumn from '@/components/ContentSingleColumn.vue'
import icon from 'vue-awesome/components/Icon'
import courseApi from '@/api/course.js'
import draggable from 'vuedraggable'

export default {
    name: 'TemplateEdit',
    props: {
        template: {
            required: true
        }
    },
    data () {
        return {
            fieldTypes: {
                'i': 'Image',
                't': 'Text',
                'f': 'File'
            }
        }
    },
    components: {
        'content-single-column': ContentSingleColumn,
        'icon': icon,
        'draggable': draggable
    },
    methods: {
        onSubmit () {
            // #TODO Handle saving the template.
        },
        addField () {
            var newField = {
                'type': 't',
                'title': '',
                'location': this.template.fields.length
            }

            this.template.fields.push(newField)
        },
        removeField (location) {
            if (confirm('Are you sure you want to remove \'' + this.template.fields[location].title + '\'?')) {
                this.template.fields.splice(location, 1)
            }
        },
        onUpdate () {
            for (var i = 0; i < this.template.fields.length; i++) {
                this.template.fields[i].location = i
            }
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

.icon-box {
    text-align: center;
}

.handle, .trash-box {
    text-align: center;
    padding: 10px 0px 10px 10px;
}

.handle {
    cursor: grab;
}

.trash-box {
    cursor: pointer;
}

.move-icon, .trash-icon {
    fill: var(--theme-dark-grey)
}

.field-card:hover .move-icon, .field-card:hover .trash-icon {
    fill: var(--theme-dark-blue);
}

.trash-box:hover .trash-icon {
    fill: var(--theme-red);
}

.handle:hover .move-icon {
    fill: var(--theme-blue);
}

@media(max-width:768px){
    .icon-box {
        margin-top: 10px;
    }

    .handle, .trash-box {
        display: inline;
    }
}
</style>
