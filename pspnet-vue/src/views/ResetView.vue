<template>
   <div class="w-full grid place-content-center ">
    <div v-if="!good_msg" class="max-w-xs">
      
      <h1 class="text-4xl text-center"> Reset Password</h1>

      <form class="form" @submit.prevent="handleSubmit">

       <input v-model="password" type="password" placeholder="New Password" class="input" required>
       <input v-model="confirmPassword" type="password" placeholder="Confirm New Password" class="input" required>
       <button class="button bg-plant hover:bg-green-400 font-bold w-full">Submit</button>

       <div class="error" v-if="error_msg"> {{ error_msg }}</div>

      </form>
    </div>

    <div v-if="good_msg" class="max-w-md">

      <EmailSuccess message="Password successfuly reset"></EmailSuccess>

    </div>
   </div>
 
  
</template>

<script>
import { ref } from 'vue'
import {useRoute} from 'vue-router'
import { resetPass } from '@/api/'
import EmailSuccess from '@/components/EmailSuccess.vue'

export default {
  name: 'ResetView',
  components : { EmailSuccess },
  setup() {
    const password = ref('')
    const confirmPassword = ref('')

    const route = useRoute()
    const resetToken = route.params.resetToken

    const error_msg = ref('')
    const good_msg = ref('')

    const handleSubmit = async () => {
      if (password.value == confirmPassword.value){
        try{
          const res = await resetPass({ 'new_password' : password.value}, resetToken)
          good_msg.value = res.data.message
        }
        catch(err){
          error_msg.value = err.response.data.message
        }
      } else {
        error_msg.value = 'Passwords do not match'
        password.value = ''
        confirmPassword.value = ''
      }
    }
  
    return {error_msg, good_msg, password, confirmPassword, handleSubmit, resetToken}
  }

}
</script>

<style lang="postcss" scoped>
.form{
  @apply mt-7 mb-7  text-left p-0 max-w-xs
}

.input {
  @apply rounded-xl my-2 bg-gray-100
}

.button {
  @apply rounded-xl my-1
}
</style>