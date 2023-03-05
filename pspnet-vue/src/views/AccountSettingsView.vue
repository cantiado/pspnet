<template>
  <div class="w-full bg-gray-50">
    <h1 class="text-left ml-10 font-bold text-lg my-5">Account Settings</h1>
    <div class="divide-y-2 mr-52 ml-10 max-w-7xl">

      <div class="flex justify-between grow card border-t-2">
        <div class="setting">Name</div>
        <div v-if="!toggleName">{{name}}</div>
        <input v-else ref="nameInput" v-model="name" @blur="commitChange" @keyup.enter="commitChange" type="text" />
        <div class="update" @click="toggleNewName" >Update</div>
      </div>

      <div class="flex justify-between grow card">
        <div class="setting">Email</div>
        <div v-if="!toggleEmail">{{email}}</div>
        <input ref="emailInput" v-model="email" @blur="commitChange" @keyup.enter="commitChange" v-else type="text" />
        <div @click="toggleNewEmail" class="update">Update</div>
      </div>

      <div class="flex justify-between grow card">
        <div class="setting">Role</div>
        <div>{{role}}</div>
        <div class="update">Update</div>
      </div>

    </div>

    <div v-if="error_msg" class="error">
      {{ error_msg }}
    </div>
  </div>
</template>

<script>
import { ref} from '@vue/reactivity'
import { authStore } from '@/store/authenticate'
import { onMounted } from '@vue/runtime-core'
import { nextTick } from 'vue'
import { update_user_settings } from '@/helpers'
import { useRouter } from 'vue-router'

export default {
  name : 'AccountSettingsView',
  setup(){
    const store = authStore()
    const name = ref('')
    const email = ref('')
    const role = ref('')

    const error_msg = ref('')
    //refs to DOM elements to focus inputs
    const nameInput = ref(null)
    const emailInput = ref(null)

    
    const toggleEmail = ref(false)
    const toggleName = ref(false)


    onMounted(async () => {
      const data = await store.userData()
      name.value = data.name
      email.value = data.email
      role.value = data.role
    })
    const commitChange = async () => {
      toggleEmail.value = false
      toggleName.value = false
      if(name.value.split(' ').length != 2){
        error_msg = "Please add first and last name"
      }
      else {
        await update_user_settings({
          'email' : email.value,
          'firstname' : name.value.split(' ')[0],
          'lastname' : name.value.split(' ')[1]
        })
      }
    }

    const toggleNewEmail= () => {
      toggleEmail.value = true
      nextTick(() => {
        emailInput.value.focus()
      })
    }
    const toggleNewName = () => {
      toggleName.value = true
      nextTick(() => {
        nameInput.value.focus()
      })
    }

    return { name, email, role, toggleNewEmail, toggleNewName, toggleName, toggleEmail, commitChange, nameInput, emailInput, error_msg}
  },
  beforeMount() {
    const store = authStore();
    if (!store.isAuthenticated()) {
      const router = useRouter();
      router.push({name: 'login'})
    }
  }
}
</script>

<style lang="postcss" scoped>
input {
  @apply text-center
}

.card {
  @apply h-20 items-center
}

.update {
  @apply text-blue-400 hover:cursor-pointer
}

.setting {
  @apply text-gray-500
}
</style>