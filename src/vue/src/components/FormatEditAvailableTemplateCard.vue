<template>
    <b-card class="card no-hover" :class="this.color" style="">
        <b>{{ template.t.name }}</b>
        <toggle-switch @click.native.stop class="template-todo-card-switch" :isActive="isActive" @parentActive="template.available = $event"/>
    </b-card>
</template>

<script>
import Switch from '@/components/SwitchComponent.vue'

export default {
    props: ['template', 'color'],
    data () {
        return {
            isActive: this.template.available
        }
    },
    components: {
        'toggle-switch': Switch
    }
}
</script>

<style>
.template-todo-card-switch {
    float: right;
    text-align: center;
}

.no-hover:hover {
    background-color: var(--theme-light-grey) !important;
}
</style>
