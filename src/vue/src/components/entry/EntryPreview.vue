<!--
    Loads a preview of an Entry-Template and returns the filled in data to
    the parent once it's saved.
-->
<template>
    <div>
        <h2 class="mb-2">{{template.name}}</h2>
        <b-card class="no-hover">
            <div v-for="(field, i) in template.fields" :key="field.eID">
                <div v-if="field.title != ''">
                    <b>{{ field.title }}</b>
                </div>

                <div v-if="field.type=='t'">
                    <b-textarea class="theme-input" v-model="completeContent[i].data"></b-textarea><br>
                </div>
                <div v-else-if="field.type=='i'">
                    <b-form-file v-model="completeContent[i].data" :state="Boolean(completeContent[i].data)" placeholder="Choose a file..."></b-form-file><br><br>
                </div>
                <div v-else-if="field.type=='f'">
                    <b-form-file v-model="completeContent[i].data" :state="Boolean(completeContent[i].data)" placeholder="Choose a file..."></b-form-file><br><br>
                </div>
            </div>

            <b-alert :show="dismissCountDown" dismissible variant="secondary"
                @dismissed="dismissCountDown=0">
                Please fill in every field.
            </b-alert>
            <b-button class="add-button float-right" @click="save">
                <icon name="paper-plane"/>
                Post Entry
            </b-button>
        </b-card>
    </div>
</template>

<script>
import icon from 'vue-awesome/components/Icon'

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
    },
    components: {
        'icon': icon
    }
}
</script>
