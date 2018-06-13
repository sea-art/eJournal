<!-- Example of a simple template. -->
<template>
    <b-card class="entry-template">
        <b-row>
            <b-col id="main-card-left-column" cols="12">
                <h3>{{ textbox1 }}</h3>
                <p>{{ textbox2 }}</p><br>
            </b-col>
        </b-row>
    </b-card>
</template>

<script>
export default {
    /* Variables that are needed to fill in the template. */
    props: ['textbox1', 'textbox2', 'date']
}

</script>

<style>
.entry-template {
    background-color: var(--theme-light-grey);
}
</style>
