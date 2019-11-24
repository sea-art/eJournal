<template>
    <b-card
        :class="$root.getBorderClass()"
        class="no-hover"
    >
        <div>
            <div class="d-flex multi-form">
                <div class="portrait-wrapper">
                    <img
                        class="no-hover"
                        :src="user.profile_picture"
                    />
                </div>
                <div class="student-details">
                    <slot/>
                    <b>{{ user.full_name }}</b>
                    <p>({{ user.username }})</p>
                </div>
            </div>
        </div>
    </b-card>
</template>

<script>
export default {
    props: {
        user: {
            required: true,
        },
    },
}
</script>

<style lang="sass">
@import '~sass/partials/shadows.sass'
@import '~sass/modules/breakpoints.sass'

.portrait-wrapper
    position: relative
    min-width: 80px
    height: 70px
    img
        @extend .shadow
        width: 70px
        height: 70px
        border-radius: 50% !important
    .number-badge
        position: absolute
        right: 0px
        top: 0px

.student-details
    position: relative
    width: calc(100% - 80px)
    min-height: 70px
    flex-direction: column
    padding: 10px
    .username-wrapper
        display: block
        width: 100%
        text-overflow: ellipsis
        white-space: nowrap
        overflow: hidden
    &.list-view
        padding-left: 40px
    @include sm-max
        align-items: flex-end

</style>
