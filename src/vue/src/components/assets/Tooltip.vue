<template>
    <icon
        v-b-tooltip.hover
        :title="tip"
        name="info"
        class="info-icon no-hover help-cursor shift-up-3"
    />
</template>
<script>

export default {
    props: ['tip'],
}

</script>
