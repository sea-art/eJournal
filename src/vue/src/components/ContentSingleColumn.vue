<template>
    <b-row no-gutters>
        <b-col cols="12" lg="6" offset-lg="3" :class="'main-content ' + extraClasses">
            <slot/>
        </b-col>
    </b-row>
</template>

<script>
export default {
    name: 'ContentColumns',
    props: {
        extraClasses: {
            default: ''
        }
    }
}
</script>

<style lang="sass">
@import '~sass/modules/colors.sass'
@import '~sass/modules/breakpoints.sass'

.main-content
    background-color: $theme-medium-grey
    flex: 1 1 auto

// @media(max-width:992px)
//     .main-content
//         padding: 30px !important
//
// @media (max-width: 576px)
//     .main-content
//         padding: 30px 0px !important
</style>
