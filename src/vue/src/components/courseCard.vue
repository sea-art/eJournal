<template>
    <div>
        <h1>{{ msg }}</h1>
    </div>
</template>

<script>
export default {
    name: 'courseCard',
    data(vars) {
        return {
            msg: vars
        }
    }
}
</script>
