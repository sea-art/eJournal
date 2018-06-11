<template>
    <div>
        <h1>Journal Page</h1>
        Hello {{ $route.params.student }}
        Hello {{ $route.params.assign }}
        Hello {{ $route.params.course }}
    </div>
</template>

<script>
export default {
    name: 'Journal'
}
</script>
