<!--
    Loads a preview of an Entry-Template and returns the filled in data to
    the parent once it's saved.
-->
<template>
    <div>
        <b-card
            :class="$root.getBorderClass($route.params.cID)"
            class="no-hover"
        >
            <h2 class="mb-2">
                {{ template.name }}
            </h2>
            <p v-if="description">
                {{ description }}
            </p>

            <entry-fields
                :template="template"
                :completeContent="completeContent"
                :displayMode="false"
                :nodeID="nodeID"
            />

            <b-alert
                :show="dismissCountDown"
                dismissible
                variant="secondary"
                @dismissed="dismissCountDown=0"
            >
                Some fields are empty or incorrectly formatted.
            </b-alert>
            <b-button
                class="add-button float-right"
                @click="save"
            >
                <icon name="paper-plane"/>
                Post Entry
            </b-button>
        </b-card>
    </div>
</template>

<script>
import entryFields from '@/components/entry/EntryFields.vue'

export default {
    components: {
        entryFields,
    },
    props: ['template', 'nodeID', 'description'],
    data () {
        return {
            completeContent: [],
            dismissSecs: 3,
            dismissCountDown: 0,
            showDismissibleAlert: false,
        }
    },
    watch: {
        template () {
            this.completeContent = []
            this.setContent()
        },
    },
    created () {
        this.setContent()
    },
    methods: {
        setContent () {
            this.template.field_set.forEach((field) => {
                this.completeContent.push({
                    data: null,
                    id: field.id,
                })
            })
        },
        checkFilled () {
            for (let i = 0; i < this.completeContent.length; i++) {
                const content = this.completeContent[i]
                const field = this.template.field_set[i]
                if (field.required && !content.data) {
                    return false
                }
            }

            return true
        },
        checkChanges () {
            for (let i = 0; i < this.completeContent.length; i++) {
                if (this.completeContent[i].data !== null && this.completeContent[i].data !== '') {
                    return true
                }
            }
            return false
        },
        save () {
            if (this.checkFilled()) {
                this.$emit('content-template', this.completeContent)
            } else {
                this.dismissCountDown = this.dismissSecs
            }
        },
    },
}
</script>
