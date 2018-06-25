<template>
    <b-row class="error-content">
        <b-col cols="12">
            <h1 id="error-heading">Error {{ errorCode }}:</h1><h1 id="error-message"> {{ errorMessage }}</h1><br/>
        </b-col>
        <b-col cols="12">
            Unfortunately the page you are looking for is not here.<br/>
            You might want to try going back to the homepage or report a problem.
        </b-col>
        <b-col cols="12">
            <b-button :to='"/Home"'>Home</b-button>
            <b-button :to='"/Home"'>Contact</b-button>
        </b-col>
    </b-row>
</template>

<script>
export default {
    name: 'Error',
    props: {
        errorCode: {
            required: true
        },
        errorMessage: {
            required: true
        }
    }
}
</script>

<style>
.error-content {
    padding: 40px;
}

#error-heading, #error-message {
    font-size: 100px;
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
