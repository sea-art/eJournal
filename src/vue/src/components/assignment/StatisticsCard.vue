<template>
    <b-card class="no-hover" :class="$root.getBorderClass($route.params.cID)">
        <b>{{ subject }}</b><todo-square class="float-right" :num="num"/>
    </b-card>
</template>

<script>
import todoSquare from '@/components/assets/TodoSquare.vue'

export default {
    props: ['subject', 'num'],
    components: {
        'todo-square': todoSquare
    }
}
</script>
