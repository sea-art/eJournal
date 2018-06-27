<template>
    <div>
        <register-user/>

        <!-- <b-form @submit="onSubmit" @reset="onReset">
            <b-input class="mb-2 mr-sm-2 mb-sm-0 multi-form" v-model="form.username" placeholder="Username" required/>
            <b-input class="mb-2 mr-sm-2 mb-sm-0 multi-form" v-model="form.password" placeholder="Password" required/>
            <b-button class="float-right" type="reset">Reset</b-button>
            <b-button class="float-right" type="submit">Create</b-button>
        </b-form> -->
    </div>
</template>

<script>
import registerUser from '@/components/RegisterUser.vue'
import userApi from '@/api/user.js'

export default {
    name: 'CreateUser',
    props: ['lti'],
    components: {
        'register-user': registerUser
    },
    methods: {
        handleCreated () {

        }
    }
}
</script>
