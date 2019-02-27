<template>
    <b-badge
        class="todo-square"
        :class="{'info': num > 0}">
        {{ num ? Math.round(num * 100) / 100 : 0 }}
    </b-badge>
</template>

<script>
export default {
    props: ['num']
}
</script>

<style lang="sass">
.todo-square
    font-family: 'Roboto Condensed', sans-serif
    font-size: 18px
</style>
