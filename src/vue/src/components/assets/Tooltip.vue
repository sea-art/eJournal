<template>
    <!-- eslint-disable vue/attribute-hyphenation -->
    <icon
        v-b-tooltip:hover="title"
        name="info-circle"
        class="info-icon no-hover help-cursor shift-up-3"
    />
    <!-- eslint-enable vue/attribute-hyphenation -->
</template>
<script>

export default {
    props: ['tip'],
    computed: {
        title () {
            return this.tip.replace(/\s+/g, ' ')
        },
    },
}

</script>
