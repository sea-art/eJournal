<template>
    <b-card id="card" class="card todo-card" :class="color" @mouseover="hover">
        <b-row>
            <b-col id="main-card-left-column" cols="6">
                <h>{{ line0 }}</h><br/>
                <h>{{ line1 }}</h><br/>
                <h>{{ line2 }}</h>
            </b-col>
            <b-col id="main-card-right-column" cols="6">
                <slot></slot>
            </b-col>
        </b-row>
    </b-card>
</template>

<script>
export default {
    props: ['line0', 'line1', 'line2', 'color']
}
</script>

<style>
.todo-card {
    margin-bottom: 8px;
    /* margin-left: 30px; */
    /* margin-right: 30px; */
    text-align: left;
    background-color: var(--theme-light-grey);
    border-width: 0px;
    border-left-width: 20px;
    border-radius: 0px;
}
</style>
