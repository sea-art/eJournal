<template>
    <b-card class="card" :class="color">
        <b-row align-h="between">
            <b-col cols="6" lg-cols="6">
                <h2>{{ line1 }}</h2>
                {{ line2 }}
            </b-col>
            <b-col cols="2" lg-cols="2">
                <slot></slot>
            </b-col>
        </b-row>
    </b-card>
</template>

<script>
export default {
    props: ['line1', 'line2', 'color']
}
</script>
