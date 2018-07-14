<template>
    <div class="editor-container">
        <tiny-mce v-model="content" ref="mce" :init="tinyMCEInit"/>
    </div>
</template>

<script>
export default {
    name: 'TextEditor',
    data () {
        return {
            tinyMCEInit: {
                menubar: false,
                statusbar: false
            },
            content: ''
        }
    },
    methods: {
    }
}
</script>

<style lang="sass">
    .editor-container
        padding: 2px
</style>
