<template>
   <div>
     <h1>{{ msg }}</h1>
       Hello {{ $route.params.name }}
   </div>
</template>

<script>
  export default {
    name: 'assignment',
    data () {
      return {
      msg: 'Assignment'
    }
  }
}
</script>
