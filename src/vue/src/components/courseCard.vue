<template>
    <div>
        <p>
            {{ course.name }}<br>
            {{ course.auth }}<br>
            {{ course.date }}
        </p>
    </div>
</template>

<script>
export default {
    name: 'courseCard',
    props: ["course"]
}
</script>
