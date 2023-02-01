<template>
  <div class="w-full grid grid-cols-10">
    <div class="col-span-6 grid place-content-center bg-gray-50">
      <h1 class="text-4xl text-center">Login to Your Account</h1>
      <form @submit.prevent="handleLogin" class="form">
        <label class="label">Email:</label>
        <input v-model="email" class="input" type="email" required>

        <label class="label">Password:</label>
        <input v-model="pass" class="input" type="password" required>

        <div v-if="error_msg" class="error"> {{error_msg}}</div>

        <div class="flex justify-center">
          <button v-if="!store.loading_data" class="bg-soil text-white hover:bg-pecan button">Sign In</button>
          <button v-else class="bg-soil text-white button disabled:opacity-50 disabled ">Loading...</button>
        </div>
      </form>
    </div>
    <div class="bg-soil col-span-4 grid place-content-center">
      <div class="max-w-md">
        <h2 class="text-4xl text-white my-6 text-center">New User?</h2>
        <p class="text-white my-6 text-center">Create an account to upload and contribute to the community!</p>
        <div class="flex justify-center">
          <button @click="handleCreate" class="bg-plant  text-black button hover:bg-green-400">Create Account</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { authStore } from '@/store/authenticate'

export default {
  name: 'LoginView',
  setup(){
    const pass = ref('')
    const email = ref('')
    const router = useRouter()

    const store = authStore()
    const error_msg = ref('')

    const handleLogin = async () => {
      error_msg.value = await store.loginUser({'email' : email.value, 'password' : pass.value})
      if (!error_msg.value){
        router.push({name : 'home'})
      }
    }

    const handleCreate = () => {
      router.push({name: 'register'})
    }


    return {pass, email, handleLogin, handleCreate, error_msg, store}
  }
}
</script>

<style lang="postcss">
</style>
