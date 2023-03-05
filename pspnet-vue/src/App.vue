<template>
  <div class="flex flex-col  h-screen">
    <nav class="flex justify-start bg-plant h-24 items-center">
      <router-link class = "mx-2" :to="{name: 'home'}">PSPNet</router-link> 
      <router-link v-if="currentRoute != 'login' && currentRoute != 'register'" class = "mx-2" :to="{name: 'about'}">About</router-link> 
      <router-link v-if="currentRoute != 'login' && currentRoute != 'register'" class = "mx-2" :to="{name: 'explore'}">Explore</router-link> 
      <router-link v-if="currentRoute != 'login' && currentRoute != 'register'" class = "mx-2" :to="{name: 'identify'}">Identify</router-link>
      <div v-if="!((currentRoute === 'login') || (currentRoute === 'register'))" class="grow flex justify-end">
        <button v-if="!store.isAuthenticated()" @click="toLogin" type="button" class="btn bg-gray-50 rounded-md">Login</button>
        <ProfileIcon v-else/>
      </div>
    </nav>
    <div class="flex flex-grow">
      <router-view/>
    </div>
    <Footer/>
  </div>
</template>

<script>
import { computed } from '@vue/runtime-core'
import { useRouter } from 'vue-router'
import { authStore } from './store/authenticate'
import Footer from './components/Footer.vue'
import ProfileIcon from '@/components/ProfileIcon.vue'

export default {
  components: {ProfileIcon, Footer},
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
/* Some button styles are from https://tailwind-elements.com/docs/standard/components/login-form/ */


#app .btn {
  @apply inline-block px-7 py-3 bg-gray-50 text-black font-medium text-sm leading-snug uppercase rounded shadow-md hover:bg-gray-100 hover:shadow-lg focus:bg-gray-100 focus:shadow-lg focus:outline-none focus:ring-0 active:bg-gray-200 active:shadow-lg transition duration-150 ease-in-out
}

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
