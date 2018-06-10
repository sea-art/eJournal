<template>
    <div>
        <h1> {{ $route.params.course }} </h1>
    </div>
</template>

<script>

export default {
    props: ['subject'],
    data() {
        return {
            msg: ""
        }
    }
}
</script>
