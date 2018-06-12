<template>
    <b-form inline>
          <label class="sr-only" for="inlineFormInputName2">Username</label>
          <b-input class="mb-2 mr-sm-2 mb-sm-0" id="inlineFormInputName2" placeholder="Username" />
          <label class="sr-only" for="inlineFormInputGroupUsername2">Password</label>
          <b-input-group left="@" class="mb-2 mr-sm-2 mb-sm-0">
              <b-input id="inlineFormInputGroupUsername2" placeholder="Password" />
          </b-input-group>
         <b-button class="mb-2 mr-sm-2 mb-sm-0" @click="handleLogin()">Login</b-button>
         <b-button class="mb-2 mr-sm-2 mb-sm-0" @click="handleRegister()">Register</b-button>
    </b-form>
</template>

<script>
export default {
    methods: {
        handleLogin () {
            this.$router.push('/Home')
        },
        handleRegister () {
            alert('TODO Handle register')
        }
    }
}
</script>
