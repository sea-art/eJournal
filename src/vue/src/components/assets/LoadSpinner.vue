<template>
    <b-card
        class="large-load-spinner no-hover"
    >
        <icon
            name="circle-o-notch"
            spin
            scale="4"
        />
    </b-card>
</template>

<style lang="sass">
@import '~sass/modules/colors.sass'
@import '~sass/partials/shadows.sass'

.card.large-load-spinner
    position: absolute
    left: 50%
    top: 50%
    transform: translate(-50%, -50%)
    border-left-width: 1px
    .card-body
        border: 0px
    svg
        fill: $theme-dark-grey
</style>
