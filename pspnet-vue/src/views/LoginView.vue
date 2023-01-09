<template>
  <div class="w-full grid grid-cols-10">
    <div class="col-span-6 grid place-content-center">
      <h1 class="text-4xl">Login to Your Account</h1>
      <form @submit.prevent="handleLogin" class="mt-7 mb-7 mx-auto text-left p-10 max-w-md">
        <label class="label">Email:</label>
        <input v-model="email" class="input" type="email" required>

        <label class="label">Password:</label>
        <input v-model="pass" class="input" type="password" required>

        <div v-if="error" class="error"> {{error}}</div>

        <div class="flex justify-center">
          <button class="bg-soil text-white button">SIGN IN</button>
        </div>
      </form>
    </div>
    <div class="bg-soil col-span-4 grid place-content-center">
      <div class="max-w-md">
        <h2 class="text-4xl text-white my-6">New User?</h2>
        <p class="text-white my-6">Create an account to upload and contribute to the community!</p>
        <button class="bg-green-200 text-black button">CREATE ACCOUNT</button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import useLogin from '@/composables/userlog'

export default {
  name: 'LoginView',
  setup(){
    const pass = ref('')
    const email = ref('')

    const {error, login} = useLogin()

    const handleLogin = async () => {
      const res = await login(email.value, pass.value)
      console.log(res.data)
      if (!error.value){
        console.log('Sucessful Login')
      }
    }
    return {pass, email, handleLogin, error}
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
</style>
