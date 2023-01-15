<template>
  <div class="w-full grid place-content-center bg-[url('../assets/registeration_image.jpg')] bg-no-repeat bg-cover bg-top">
    <div class=" bg-gray-50 rounded-md max-w-md">
      <h1 class="text-4xl mt-10">Create an Account</h1>
      <h2 class="text-1xl">Already have an account?
        <router-link class="underline text-blue-500" :to="{name: 'login'}">Login here</router-link>
      </h2>
      <form class="form" @submit.prevent="handleCreateAccount">
        <input v-model="firstname" type="text" placeholder="First Name" class="input" required> 
        <input v-model="lastname" type="text" placeholder="Last Name" class="input" required> 
        <input v-model="email" type="email" placeholder="Email Address" class="input" required> 
        <input v-model="pass" type="password" placeholder="Password" class="input" required> 
        <div v-if="response_data" class="error"> {{response_data}}</div>
        <div class="flex justify-center">
          <button v-if="!isPending" class="button bg-soil text-white hover:bg-pecan">Create Account</button>
          <button v-else class="button bg-soil text-white hover:bg-pecan disabled:opacity-50 disabled">Creating...</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import useCreate from '@/composables/CreateAccount'
import { useRouter } from 'vue-router'


export default {
  name: 'RegisterView',
  setup(){
    const email = ref(null)
    const pass = ref(null)
    const firstname = ref(null)
    const lastname = ref(null)
    const router = useRouter()
    const response_data =ref(null)

    const {error, isPending, createAccount} = useCreate()

    const handleCreateAccount = async () => {
      const res = await createAccount(firstname.value, lastname.value, email.value, pass.value)
      response_data.value = res.data.status
      if (!res.data.status){
        router.push({name: 'home'})
      }
    }

    return {email, pass, firstname, lastname, handleCreateAccount, isPending, error, response_data}
  }
}
</script>

<style lang="postcss" scoped>

.input{
  @apply rounded-none my-2
}


</style>