<template>
    <b-card class="card student-card">
        <b-row>
            <b-col id="student-card-portrait-column" order="1" cols="6" md="2">
                <div class="portrait-container">
                    <img src="../assets/logo.png">
                </div>
            </b-col>
            <b-col id="student-card-main-content-column" order="3" order-md="2" cols="12" md="8">
                <h>{{ student }}</h><br/>
                <h>{{ studentNumber }}</h><br/>
                <h>{{ studentPortraitPath }}</h><br/>
                <h>{{ progress }}</h><br/>
                <h>{{ entriesStats }}</h>
            </b-col>
            <b-col id="main-card-right-column" order="2" order-md="3" cols="6" md="2">GRADED<br/>1MSG</b-col>
        </b-row>
    </b-card>
</template>

<script>
export default {
    props: ['student', 'studentNumber', 'studentPortraitPath', 'progress', 'entriesStats']
}
</script>

<style>
.student-card {
    margin-bottom: 8px;
    text-align: left;
    background-color: var(--theme-light-grey);
    border-width: 0px;
    border-left-width: 20px;
    border-left-color: red;
    border-radius: 0px;
}
</style>
