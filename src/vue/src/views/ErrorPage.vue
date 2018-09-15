<template>
    <b-row class="error-content">
        <b-col cols="12">
            <h1 id="error-heading">
                Error {{ code }}: <span id="error-message">{{ reasonPhrase }}</span>
            </h1>
        </b-col>
        <b-col cols="12" >
            <div class="description-container">
                {{ description }}
            </div>
        </b-col>
        <b-col cols="12">
            <b-button :to="{name: 'Home'}">
                <icon name="home"/>
                Home
            </b-button>
        </b-col>
    </b-row>
</template>

<script>
import icon from 'vue-awesome/components/Icon'

export default {
    name: 'Error',
    props: {
        code: {
            default: '520'
        },
        reasonPhrase: {
            default: 'Unknown Error'
        },
        description: {
            default: 'We are sorry, but an unkown error has brought you here. ' +
                     'Please use the feedback button at the bottom of the page ' +
                     'to get in touch with us.'
        }
    },
    components: {
        icon
    }
}
</script>

<style lang="sass">
@import '~sass/modules/colors.sass'

.error-content
    padding: 40px

.description-container
    padding: 20px 0px

#error-heading, #error-message
    border: none
    padding: 0px

#error-heading
    color: $theme-dark-grey
    font-size: 80px

#error-message
    color: $theme-medium-grey
    font-size: 60px
</style>
