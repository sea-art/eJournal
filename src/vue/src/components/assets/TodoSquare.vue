<template>
    <div class="todo-square" :class="num ? 'num-nonzero' : 'num-zero'">
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
    text-align: center
    color: white
    font-family: 'Roboto Condensed', sans-serif
    font-size: 18px
    width: 45px
    height: 30px
    &.num-nonzero
        background-color: $theme-blue
        @extend .shadow
    &.unpublished-count
        background-color: $theme-orange
    &.num-zero
        background-color: $theme-dark-grey
</style>
