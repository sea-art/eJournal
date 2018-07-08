<template>
    <b-alert show :variant="type">{{ description }}</b-alert>
</template>

<script>
export default {
    props: ['type', 'description']
}
</script>

<style lang="sass">
@import '~sass/modules/colors.sass'

.alert-success
    background: $theme-positive-selected
    color: black
    border: none

.alert-danger
    background: $theme-negative-selected
    color: white
    border: none
</style>
