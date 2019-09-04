<template>
    <b-badge
        :class="{'info': num > 0}"
        class="todo-square"
    >
        {{ num ? Math.round(num * 100) / 100 : 0 }}
    </b-badge>
</template>

<script>
export default {
    props: ['num'],
}
</script>

<style lang="sass">
.todo-square
    font-family: 'Roboto Condensed', sans-serif
    font-size: 18px
    border-radius: 5px !important
</style>
