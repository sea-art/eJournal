<!-- Example of a simple template. -->
<template>
    <b-card class="entry-template">
        <b-row>
            <b-col id="main-card-left-column" cols="12">

                <h3>Title: {{ textbox1 }}</h3><br>
                <p>{{ textbox2 }}</p><br>
            </b-col>
        </b-row>
    </b-card>
</template>

<script>
export default {
    /* Variables that are needed to fill in the template. */
    props: ['textbox1', 'textbox2', 'deadline']
}

</script>

<style>
.entry-template {
    margin-bottom: 8px;
    text-align: left;
    background-color: var(--theme-light-grey);
    border-width: 0px;
    border-left-width: 20px;
    border-left-color: red;
    border-radius: 0px;
}
</style>
