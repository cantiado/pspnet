<template>
<h1> Reset Password Link </h1>
  
</template>

<script>
import {useRoute} from 'vue-router'


export default {
  name: 'ResetView',
  setup() {
    const route = useRoute()
    const resetToken = route.params.resetToken
  }

}
</script>

<style>

</style>