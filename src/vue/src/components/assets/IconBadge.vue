<template>
    <b-badge
        class="badge-part"
        :class="custonClass"
    >
        <!-- {{ leftNum ? Math.round(leftNum * 100) / 100 : 0 }} -->
        <icon :name="icon"/>
    </b-badge>
</template>

<script>
export default {
    props: {
        custonClass: {
            required: false,
            default: '',
            String,
        },
        icon: {
            required: true,
            String,
        },
    },
}
</script>

<style lang="sass">
@import '~sass/modules/colors.sass'
.badge-part
    font-family: 'Roboto Condensed', sans-serif
    font-size: 1em
    border-radius: 5px !important
    border: 1px solid #CCCCCC
</style>
