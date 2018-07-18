<template>
    <div class="todo-square">
        {{ num }}
    </div>
</template>

<script>
export default {
    props: ['num']
}
</script>

<style lang="sass">
@import '~sass/modules/colors.sass'
@import '~sass/partials/shadows.sass'

.todo-square
    @extend .shadow
    text-align: center
    color: white
    font-family: 'Roboto Condensed', sans-serif
    font-size: 18px
    background-color: $theme-blue
    &.unpublished-count
        background-color: $theme-change-selected
    width: 45px
    height: 30px
</style>
