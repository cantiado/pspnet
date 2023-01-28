<template>
  <div class="flex flex-col  h-screen">
    <nav class="flex justify-start bg-plant">
      <router-link class = "mx-2 item-left" :to="{name: 'home'}">PSPNet</router-link> 
      <router-link v-if="currentRoute != 'login' && currentRoute != 'register'" class = "mx-2" :to="{name: 'about'}">About</router-link> 
      <div v-if="!((currentRoute === 'login') || (currentRoute === 'register'))" class="grow flex justify-end">
        <button v-if="!store.isAuthenticated()" @click="toLogin" class="btn bg-gray-50 rounded-md">Login</button>
        <ProfileIcon v-else/>
      </div>
    </nav>
    <div class="flex flex-grow">
      <router-view/>
    </div>
  </div>
</template>

<script>
import { computed } from '@vue/runtime-core'
import { useRouter } from 'vue-router'
import { authStore } from './store/authenticate'
import ProfileIcon from '@/components/ProfileIcon.vue'

export default {
  components: {ProfileIcon},
  setup(){
    const store = authStore()
    const router = useRouter()
    const toLogin = () => {
      if (store.isAuthenticated()){
      }
      else{
        router.push({name : 'login'})
      }
    }
    const currentRoute = computed(() => {
      return router.currentRoute.value.name
    })

    return { currentRoute, toLogin, store }
  }
}
</script>


<style lang="postcss" scoped>


/*.btn {
  @apply font-bold px-4 py-0.5
}*/

nav {
  padding: 30px;
}

nav a {
  font-weight: bold;
  color: #2c3e50;
}

nav a.router-link-exact-active {
  color: #42b983;
}
</style>
