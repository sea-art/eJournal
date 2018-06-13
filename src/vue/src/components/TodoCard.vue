<template>
    <b-card id="card" class="card" :class="color" @mouseover="hover">
        <h6>{{ line0 }}</h6>
        <h5>{{ line1 }}</h5>
        {{ line2 }}
    </b-card>
</template>

<script>
export default {
    props: ['line0', 'line1', 'line2', 'color']
}
</script>
