<template>
    <div>
        <div v-if="!createNew">
            Pls maak een page voor het maken van assignments
        </div>
        <newTemplate v-if="createNew"></newTemplate>
        <button v-on:click="newTemplateToggle">{{ButtonCreateNew}}</button>
    </div>
</template>

<script>
import newTemplate from '@/components/newTemplate'
export default {
    name: 'newAssign',
    components: {
        newTemplate
    },
    data () {
        return {
            createNew: false,
            ButtonCreateNew: 'new template'
        }
    },
    methods: {
        newTemplateToggle () {
            this.createNew = !this.createNew
            if (this.createNew) {
                this.ButtonCreateNew = 'Cancel'
            } else {
                this.ButtonCreateNew = 'new template'
            }
        }
    }
}
</script>
