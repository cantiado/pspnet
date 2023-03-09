<template>
  <div  
    class="mb-4 rounded-lg bg-green-200 py-5 px-6 text-base text-green-700"
    > {{ message }} 
  </div>
</template>

<script>

export default {
  name: 'EmailSuccess',
  props: ['message'],

}

</script>

<style lang="postcss" scoped>

</style>
