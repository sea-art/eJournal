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
                        <br>
                        <b-form-file v-model="completeContent[i].data" :state="Boolean(file)" placeholder="Choose a file..."></b-form-file><br><br>
                    </div>
                    <div v-else-if="field.type=='f'">
                        <b-form-file v-model="completeContent[i].data" :state="Boolean(file)" placeholder="Choose a file..."></b-form-file><br><br>
                    </div>
                </div>

                <b-alert :show="dismissCountDown" dismissible variant="secondary"
                    @dismissed="dismissCountDown=0">
                    Please fill in every field.
                </b-alert>
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
            completeContent: [],
            dismissSecs: 3,
            dismissCountDown: 0,
            showDismissibleAlert: false
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
        checkFilled: function () {
            for (var content of this.completeContent) {
                if (content.data === null) {
                    return false
                }
            }

            return true
        },
        save: function () {
            if (this.checkFilled()) {
                this.$emit('content-template', this.completeContent)
            } else {
                this.dismissCountDown = this.dismissSecs
            }
        }
    }
}
</script>
