<template>
  <div class="home">
    <button class="button" @click="isValid"> Click to authenticate </button>
  </div>
</template>

<script>
import { authStore } from '@/store/authenticate'
// @ is an alias to /src

export default {
  name: 'HomeView',
  components: {
  },
  setup(){
    const store = authStore()

    const isValid = () => {
      console.log(store.isAuthenticated())
    }
    return {store, isValid}
  }
}
</script>
