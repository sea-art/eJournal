<template>
    <b-card class="card" :class="$root.getBorderClass($route.params.cID)">
        <b-row align-h="between">
            <b-col cols="12" lg="6">
                <h2>{{ line1 }}</h2>
                {{ line2 }}
            </b-col>
            <b-col cols="12" lg="6">
                <slot></slot>
            </b-col>
        </b-row>
    </b-card>
</template>

<script>
export default {
    props: ['line1', 'line2']
}
</script>
