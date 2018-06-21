<!-- Loads a preview of a template. -->
<template>
    <b-card class="card main-card noHoverCard" :class="'dark-border'">
        <b-row>
            <b-col id="main-card-left-column" cols="9" lg-cols="12">
                <h2>{{template.name}}</h2>
            </b-col>
            <b-col id="main-card-right-column" cols="3" lg-cols="12" class="right-content">
            </b-col>
        </b-row>
        <b-row>
            <b-col id="main-card-left-column" cols="12" lg-cols="12">
                <div v-for="(field, i) in entryNode.entry.template.fields" :key="field.eID">
                    <div v-if="field.title != ''">
                        <h4>{{ field.title }}</h4>
                    </div>
                    <div v-if="field.type=='t'">
                        {{ completeContent[i].data }}<br><br>
                    </div>
                    <div v-else-if="field.type=='i'">
                    </div>
                    <div v-else-if="field.type=='f'">
                    </div>
                </div>

                <b-button @click="save">Post Entry</b-button>
            </b-col>
        </b-row>
    </b-card>
</template>

<script>
export default {
    props: ['entryNode'],
    data () {
        return {
            tempNode: this.entryNode,
            completeContent: []
        }
    },
    watch: {
        entryNode: function () {
            this.completeContent = []
            this.setContent()
        }
    },
    created () {
        this.setContent()
    },
    methods: {
        setContent: function () {
            var checkFound = false
            for (var templateField of this.entryNode.entry.template.fields) {
                checkFound = false

                for (var content of this.entryNode.entry.content) {
                    if (content.tag === templateField.tag) {
                        this.completeContent.push({
                            data: content.data,
                            tag: content.tag
                        })

                        checkFound = true
                        break
                    }
                }

                if (!checkFound) {
                    this.completeContent.push({
                        data: null,
                        tag: templateField.tag
                    })
                }
            }
        }
    }
}
</script>
