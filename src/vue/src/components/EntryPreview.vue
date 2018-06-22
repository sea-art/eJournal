<!-- Loads a preview of a template. -->
<template>
    <b-card class="card main-card no-hover" :class="'dark-border'">
        <b-row>
            <b-col id="main-card-left-column" cols="9" lg-cols="12">
                <h2>{{template.name}}</h2>
            </b-col>
            <b-col id="main-card-right-column" cols="3" lg-cols="12" class="right-content">
            </b-col>
        </b-row>
        <b-row>
            <b-col id="main-card-left-column" cols="12" lg-cols="12">
                <div v-for="(field, i) in template.fields" :key="field.eID">
                    <div v-if="field.title != ''">
                        <b>{{ field.title }}</b>
                    </div>

                    <div v-if="field.type=='t'">
                        <b-textarea v-model="completeContent[i].data"></b-textarea><br><br>
                    </div>
                    <div v-else-if="field.type=='i'">
                        Insert input for image
                    </div>
                    <div v-else-if="field.type=='f'">
                        Insert input for file
                    </div>
                </div>

                <b-button @click="save">Post Entry</b-button>
            </b-col>
        </b-row>
    </b-card>
</template>

<script>
export default {
    props: ['template'],
    data () {
        return {
            completeContent: []
        }
    },
    watch: {
        template: function () {
            this.completeContent = []
            this.setContent()
        }
    },
    created () {
        this.setContent()
    },
    methods: {
        setContent: function () {
            for (var field of this.template.fields) {
                this.completeContent.push({
                    data: null,
                    tag: field.tag
                })
            }
        },
        save: function () {
            this.$emit('content-template', this.completeContent)
        }
    }
}
</script>
