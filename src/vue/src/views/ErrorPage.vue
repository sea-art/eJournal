<template>
    <b-row class="error-content">
        <b-col cols="12">
            <h1 id="error-heading">
                Error {{ code }}: <span id="error-message">{{ message }}</span>
            </h1>
        </b-col>
        <b-col cols="12" v-if="description">
            {{ description }}
        </b-col>
        <b-col cols="12">
            <b-button :to="{name: 'Home'}">Home</b-button>
            <!-- TODO: Add mailto or similar. -->
            <b-button :to="{name: 'Home'}">Contact</b-button>
        </b-col>
    </b-row>
</template>

<script>
export default {
    name: 'Error',
    props: {
        code: {
            default: 404
        },
        message: {
            default: 'Not found'
        },
        description: {
            type: String
        }
    }
}
</script>

<style>
.error-content {
    padding: 40px;
}

#error-heading, #error-message {
    border: none;
    padding: 0px;
}

#error-heading {
    color: var(--theme-dark-grey);
    font-size: 80px;
}

#error-message {
    color: var(--theme-medium-grey);
    font-size: 60px;
}
</style>
