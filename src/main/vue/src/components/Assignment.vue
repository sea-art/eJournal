<template>
    <div>
        <h1>{{ msg }}</h1>
        Hello {{ $route.params.assign }} </br>
        <router-link tag="button" to="/Courses/PAV/Colloquium/Dennis">Dennis Journal</router-link>

        <!-- <courses v-if="seen"></courses> -->
    </div>
</template>

<script>
    // import courses from '@/components/Courses'
    export default {
        name : 'assignment',
        // components: {
		//           courses
        //       },
        data () {
            return {
                msg : 'Docent student overview',
            }
        }
    }
</script>
