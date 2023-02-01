<template>
  <div class="w-full bg-gray-50">
    <h1 class="text-left ml-10 font-bold text-lg my-5">Profile</h1>
    <div class="divide-y-2 mr-52 ml-10 max-w-7xl">
      <div class="flex justify-between grow card border-t-2">
        <div class="setting">Name</div>
        <div>{{name}}</div>
        <div class="update">Update</div>
      </div>

      <div class="flex justify-between grow card">
        <div class="setting">Email</div>
        <div>{{email}}</div>
        <div class="update">Update</div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from '@vue/reactivity'
import { authStore } from '@/store/authenticate'
import { onMounted } from '@vue/runtime-core'

export default {
  name : 'AccountSettingsView',
  setup(){
    const store = authStore()
    const name = ref('')
    const email = ref('')


    onMounted(async () => {
      const data = await store.userData()
      name.value = data.name
      email.value = data.email
    })

    return { name, email }
  }
}
</script>

<style lang="postcss" scoped>
.card {
  @apply h-20 items-center
}

.update {
  @apply text-blue-400
}

.setting {
  @apply text-gray-500
}
</style>