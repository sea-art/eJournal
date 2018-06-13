<template>
    <b-card id="card" class="todo-card" :class="color" @mouseover="hover">
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
    props: ['line1', 'line2', 'color']
}
</script>

<style>
.todo-card {
    margin-bottom: 8px;
    margin-left: 15px;
    margin-right: 30px;
    text-align: left;
    background-color: var(--theme-light-grey);
    border-width: 0px;
    border-left-width: 20px;
    border-radius: 0px;
}

.todo-card.pink-border {
    border-left-color: var(--theme-pink);
}

.todo-card.peach-border {
    border-left-color: var(--theme-peach);
}

.todo-card.blue-border {
    border-left-color: var(--theme-blue);
}

.todo-card:hover {
    background-color: var(--theme-dark-grey);
}
</style>
