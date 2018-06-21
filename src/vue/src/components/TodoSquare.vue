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

<style>
.point-square {
    text-align: center;
    color: white;
    font-family: 'Roboto Condensed', sans-serif;
    font-size: 18px;
    background-color: var(--theme-blue);
    width: 45px;
    height: 30px;
}
</style>
