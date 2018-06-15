<template>
    <div class="todo-circle">
        {{ num }}
    </div>
</template>

<script>
export default {
    props: ['num']
}
</script>

<style>
.todo-circle {
    float: right;
    text-align: center;
    color: white;
    font-family: 'Roboto Condensed', sans-serif;
    font-size: 18px;
    background-color: var(--theme-blue);
    display:inline-block;
    padding: 3px;
}
</style>
