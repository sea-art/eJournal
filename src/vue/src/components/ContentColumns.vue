<template>
    <b-row no-gutters>
        <b-col lg="3" class="left-content d-none d-xl-block">
            <slot name="left-content-column"></slot>
        </b-col>
        <b-col lg="12" xl="6" class="main-content">
            <slot name="main-content-column"></slot>
        </b-col>
        <b-col lg="12" xl="3" class="right-content">
            <slot name="right-content-column"></slot>
        </b-col>
    </b-row>
</template>

<script>
export default {
    name: 'ContentColumns'
}
</script>

<style lang="sass">
@import '~sass/modules/colors.sass'
@import '~sass/modules/breakpoints.sass'

.left-content
    flex: 0 0 auto
    padding: 30px 30px 0 30px !important

.main-content
    background-color: $theme-medium-grey
    flex: 1 1 auto
    padding: 30px 0px !important
    @include sm
        padding: 30px !important
    @include xl
        padding-top: 40px !important

.right-content
    flex: 0 0 auto
    padding: 30px 0px !important
    @include sm
        padding: 30px !important
    @include xl
        padding: 30px 30px 0 30px !important
</style>
