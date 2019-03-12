<template>
    <sup>
        <icon
            v-b-tooltip.hover
            :title="tip"
            name="info"
            class="info-icon no-hover help-cursor"/>
    </sup>
</template>
<script>

import icon from 'vue-awesome/components/Icon'

export default {
    props: ['tip'],
    components: {
        icon
    }
}

</script>
