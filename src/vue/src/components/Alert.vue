<template>
    <b-alert show :variant="type">{{ description }}</b-alert>
</template>
<style>
.alert-success {
    background: var(--theme-add-unselected);
    color: black;
    border: none;
}
.alert-danger {
    background: var(--theme-red);
    color: white;
    border: none;
}
</style>
<script>
export default {
    props: ['type', 'description']
}
</script>
