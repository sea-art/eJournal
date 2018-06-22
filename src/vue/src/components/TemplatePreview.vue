<!-- Loads a preview of a template. -->
<template>
    <b-card class="card main-card no-hover" :class="'dark-border'">
        <b-row>
            <b-col id="main-card-left-column" cols="9" lg-cols="12">
                <h2>{{template.name}}</h2>
            </b-col>
            <b-col id="main-card-right-column" cols="3" lg-cols="12" class="right-content">
            </b-col>
        </b-row>
        <b-row>
            <b-col id="main-card-left-column" cols="12" lg-cols="12">
                <div v-for="field in template.fields" :key="field.eID">
                    <div v-if="field.title != ''">
                        <b>{{ field.title }}</b>
                        <br>
                    </div>
                </div>
            </b-col>
        </b-row>
    </b-card>
</template>

<script>
export default {
    props: ['template']
}
</script>
