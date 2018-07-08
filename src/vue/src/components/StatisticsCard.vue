<template>
    <b-card class="card no-hover" :class="color" style="">
        <b>{{ subject }}</b><div class="point-square">{{ num }}</div>
    </b-card>
</template>

<script>
export default {
    props: ['subject', 'num', 'color']
}
</script>

<style lang="sass">
@import '~sass/modules/colors.sass'
.point-square
    float: right
    text-align: center
    color: white
    font-family: 'Roboto Condensed', sans-serif
    font-size: 18px
    background-color: $theme-blue
    width: 45px
    height: 30px
</style>
