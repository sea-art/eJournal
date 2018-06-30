<template>
    <div>
        <b-card class="no-hover">
            <b-input class="mb-2 mr-sm-2 mb-sm-0 multi-form" id="templateName" v-model="template.name" placeholder="Template name" required/>
            <draggable v-model="template.fields" @start="drag=true" @end="drag=false" @update="onUpdate" :options="{ handle:'.handle' }">
                <div v-for="field in template.fields" :key="field.location">
                    <b-card class="field-card">
                        <b-row align-h="between" no-gutters>
                            <b-col cols="12" sm="10" lg="11">
                                <b-input class="mb-2 mr-sm-2 mb-sm-0 multi-form" v-model="field.title" placeholder="Field title" required/>
                                <b-select :options="fieldTypes" v-model="field.type"></b-select>
                            </b-col>
                            <b-col cols="12" sm="2" lg="1" class="icon-box">
                                <div class="handle d-inline d-sm-block">
                                    <icon class="move-icon" name="arrows" scale="1.75"></icon>
                                </div>
                                <icon class="trash-icon" @click.native="removeField(field.location)" name="trash" scale="1.75"/>
                            </b-col>
                        </b-row>
                    </b-card>
                </div>
                <div style="visibility: hidden;"></div>
            </draggable>
            <b-card class="hover add-button" @click="addField">+ Add field</b-card>
        </b-card>
    </div>
</template>

<script>
import ContentSingleColumn from '@/components/ContentSingleColumn.vue'
import icon from 'vue-awesome/components/Icon'
import draggable from 'vuedraggable'

export default {
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
        updateLocations () {
            for (var i = 0; i < this.template.fields.length; i++) {
                this.template.fields[i].location = i
            }
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

            this.updateLocations()
        },
        onUpdate () {
            this.updateLocations()
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

.handle {
    text-align: center;
}

.move-icon {
    fill: var(--theme-dark-grey)
}

.field-card:hover .move-icon, .field-card:hover .trash-icon {
    fill: var(--theme-dark-blue) !important;
}

.handle:hover .move-icon {
    cursor: grab;
    fill: var(--theme-blue) !important;
}

.field-card:hover .trash-icon:hover {
    fill: var(--theme-negative-selected) !important;
}

@media(max-width:768px){
    .icon-box {
        margin-top: 10px;
    }
}
</style>
