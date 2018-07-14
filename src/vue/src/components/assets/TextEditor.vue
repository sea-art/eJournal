<template>
    <tiny-mce :init="tinyMCEInit"/>
</template>

<script>
export default {
    name: 'TextEditor',
    data () {
        return {
            tinyMCEInit: {
                menubar: false,
                statusbar: false,
                autosave_ask_before_unload: false
            },
            checked: ''
        }
    },
    methods: {
    }
}
</script>
