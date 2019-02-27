<template>
    <sup>
        <icon
            v-b-tooltip.hover
            :title="tip"
            name="question"
            class="question-icon no-hover help-cursor"/>
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
