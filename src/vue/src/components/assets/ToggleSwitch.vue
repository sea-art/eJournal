<template>
    <div class="round-border">
        <label class="switch">
            <input
                v-model="active"
                type="checkbox"
            />
            <span class="slider"/>
        </label>
    </div>
</template>

<script>
export default {
    props: ['isActive'],
    computed: {
        active: {
            get () {
                return this.isActive
            },
            set (value) {
                this.$emit('parentActive', value)
            },
        },
    },
}
</script>

<style lang="sass">
@import "~sass/modules/colors.sass"

.switch
    position: relative
    display: inline-block
    width: 48px
    height: 26px
    input
        display: none
    .slider
        position: absolute
        cursor: pointer
        top: 0
        left: 0
        right: 0
        bottom: 0
        background-color: #ccc
        -webkit-transition: .4s
        transition: .4s
        border-radius: 1em !important
        &:before
            position: absolute
            content: ""
            height: 18px
            width: 18px
            left: 4px
            bottom: 4px
            background-color: white
            -webkit-transition: .4s
            transition: .4s
            border-radius: 1em !important

input:checked + .slider
    background-color: $theme-green

input:focus + .slider
    box-shadow: 0 0 1px #2196F3

input:checked + .slider:before
    -webkit-transform: translateX(21px)
    -ms-transform: translateX(21px)
    transform: translateX(21px)
</style>
