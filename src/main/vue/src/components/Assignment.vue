<template>
    <div>
        <h1>{{ msg }}</h1>
        Hello {{ $route.params.assign }}

        <li><router-link tag="button" to="/Courses/PAV/Colloquium/Dennis">Dennis Journal</router-link></li>

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
                msg : 'Assignment',
            }
        }
    }
</script>
