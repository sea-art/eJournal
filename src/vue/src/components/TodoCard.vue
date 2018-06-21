<template>
    <b-card class="card" :class="color">
        <b-row>
            <b-col cols="7">
                <h6>{{ line0 }}</h6>
            </b-col>
            <b-col cols="5">
                <p>{{ $root.timeLeft(this.line0) }}</p>
            </b-col>
        </b-row>
            <h5>{{ line1 }}</h5>
            {{ line2 }}
    </b-card>
</template>

<script>
export default {
    props: ['line0', 'line1', 'line2', 'timeLeft', 'color']
}
</script>

<style scoped>
h6 {
    display: inline;
}

p {
    text-align: right;
    font-size: 20px;
    color: var(--theme-blue);
    margin-bottom: 0px;
}
</style>
