<template>
    <div>
        <p>
            {{ cName }}<br>
            {{ cAuth }}<br>
            {{ cDate }}
        </p>
    </div>
</template>

<script>
export default {
    name: 'courseCard',
    props: ["cName", "cAuth", "cDate"]
}
</script>
