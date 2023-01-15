<template>
  <div class="w-full grid grid-cols-10">
    <div class="col-span-6 grid place-content-center bg-gray-50">
      <h1 class="text-4xl">Login to Your Account</h1>
      <form @submit.prevent="handleLogin" class="form">
        <label class="label">Email:</label>
        <input v-model="email" class="input" type="email" required>

        <label class="label">Password:</label>
        <input v-model="pass" class="input" type="password" required>

        <div v-if="error" class="error"> {{error}}</div>

        <div class="flex justify-center">
          <button v-if="!isPending" class="bg-soil text-white hover:bg-pecan button">SIGN IN</button>
          <button v-else class="bg-soil text-white button disabled:opacity-50 disabled ">Loading...</button>
        </div>
      </form>
    </div>
    <div class="bg-soil col-span-4 grid place-content-center">
      <div class="max-w-md">
        <h2 class="text-4xl text-white my-6">New User?</h2>
        <p class="text-white my-6">Create an account to upload and contribute to the community!</p>
        <button @click="handleCreate" class="bg-green-200 text-black button hover:bg-green-300">CREATE ACCOUNT</button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import useLogin from '@/composables/userlog'
import { useRouter } from 'vue-router'

export default {
  name: 'LoginView',
  setup(){
    const pass = ref('')
    const email = ref('')
    const router = useRouter()

    const {error, login, isPending} = useLogin()

    const handleLogin = async () => {
      const res = await login(email.value, pass.value)
      console.log(res.data)
      if (!error.value){
        router.push({name: 'home'})
      }
    }

    const handleCreate = () => {
      router.push({name: 'register'})
    }


    return {pass, email, handleLogin, error, isPending, handleCreate}
  }
}
</script>

<style lang="postcss">
.label{
  @apply mb-6 mt-6 font-bold uppercase text-inputColor inline;
}

.input{
  @apply py-2.5 px-1.5 w-full border rounded-full;
}

.button{
  @apply border-0 rounded-3xl mt-5 py-2.5 px-5 hover:shadow-lg shadow-inner
}

.error{
  @apply bg-red-100 rounded-lg py-4 text-base text-red-700 m-3 text-center
}

.form{
  @apply mt-7 mb-7 mx-auto text-left p-10 max-w-md
}
</style>
