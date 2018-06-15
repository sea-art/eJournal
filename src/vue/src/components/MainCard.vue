<template>
    <b-card class="card" :class="color">
        <b-row align-h="between">
            <b-col lg="6" sm="12">
                <h2>{{ line1 }}</h2>
                {{ line2 }}
            </b-col>
            <b-col lg="6" sm="12">
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
