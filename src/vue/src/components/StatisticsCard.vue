<template>
    <b-card class="card" style="">
        <b>{{ subject }}</b><div class="point-square">{{ num }}</div>
    </b-card>
</template>

<script>
export default {
    props: ['subject', 'num']
}
</script>

<style>
.point-square {
    float: right;
    text-align: center;
    color: white;
    font-family: 'Roboto Condensed', sans-serif;
    font-size: 18px;
    background-color: var(--theme-blue);
    width: 45px;
    height: 30px;
}
</style>
