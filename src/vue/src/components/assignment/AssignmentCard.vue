<template>
    <b-card :class="$root.getBorderClass($route.params.cID)">
        <b-row align-h="between">
            <b-col cols="12" lg="6">
                <b-badge
                    v-if="lti"
                    class="ml-2 mt-2 info"
                    v-b-tooltip.hover
                    title="Linked via LTI">
                    LTI
                </b-badge>
                <h2 class="float-left">{{ line1 }}</h2>
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
    props: ['line1', 'line2', 'lti']
}
</script>
