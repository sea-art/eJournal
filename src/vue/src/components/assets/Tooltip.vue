<template>
    <sup>
        <icon
            v-b-tooltip.hover
            :title="tip"
            name="info"
            class="info-icon no-hover help-cursor"
        />
    </sup>
</template>
<script>

export default {
    props: ['tip'],
}

</script>
