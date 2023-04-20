<template>
  <div
    class="w-full grid place-content-center bg-[url('../assets/registeration_image.jpg')] bg-no-repeat bg-cover bg-top"
  >
    <div class="bg-gray-50 rounded-md max-w-md">
      <h1 class="text-4xl mt-10 text-center">Create an Account</h1>
      <h2 class="text-1xl text-center">
        Already have an account?
        <router-link class="underline text-blue-500" :to="{ name: 'login' }"
          >Login here</router-link
        >
      </h2>
      <form class="form" @submit.prevent="handleCreateAccount">
        <input
          v-model="firstname"
          type="text"
          placeholder="First Name"
          class="input"
          required
        />
        <input
          v-model="lastname"
          type="text"
          placeholder="Last Name"
          class="input"
          required
        />
        <input
          v-model="email"
          type="email"
          placeholder="Email Address"
          class="input"
          required
        />
        <input
          v-model="pass"
          type="password"
          placeholder="Password"
          class="input"
          required
        />
        <div v-if="error_msg" class="error">{{ error_msg }}</div>
        <div class="flex justify-center">
          <button
            v-if="!store.loading_data"
            class="button bg-soil text-white hover:bg-pecan"
          >
            Create Account
          </button>
          <button
            v-else
            class="button bg-soil text-white hover:bg-pecan disabled:opacity-50 disabled"
          >
            Creating...
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { authStore } from "@/store/authenticate";

const email = ref("");
const pass = ref("");
const firstname = ref("");
const lastname = ref("");

const error_msg = ref("");
const router = useRouter();

const store = authStore();

async function handleCreateAccount() {
  error_msg.value = await store.createUser({
    email: email.value,
    password: pass.value,
    firstname: firstname.value,
    lastname: lastname.value,
  });
  console.log(error_msg.value);
  if (!error_msg.value) {
    router.push({ name: "login" });
  }
}
</script>

<!-- <script>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { authStore } from '@/store/authenticate'


export default {
  name: 'RegisterView',
  setup(){
    const email = ref('')
    const pass = ref('')
    const firstname = ref('')
    const lastname = ref('')

    const error_msg = ref('')
    const router = useRouter()

    const store = authStore()


    const handleCreateAccount = async () => {
      error_msg.value = await store.createUser({
        'email' : email.value,
        'password' : pass.value,
        'firstname' : firstname.value,
        'lastname' : lastname.value
      })
      console.log(error_msg.value)
      if(!error_msg.value){
        router.push({name : 'login'})
      }
    }

    return {email, pass, firstname, lastname, handleCreateAccount, store, error_msg}
  }
}
</script> -->

<style lang="postcss" scoped>
.input {
  @apply rounded-md my-2;
}
</style>
