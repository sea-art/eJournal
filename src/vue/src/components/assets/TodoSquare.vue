<template>
    <div class="point-square">
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

.point-square
    text-align: center
    color: white
    font-family: 'Roboto Condensed', sans-serif
    font-size: 18px
    background-color: $theme-blue
    width: 45px
    height: 30px
</style>
