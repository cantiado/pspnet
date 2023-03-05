<!-- Author: Antonio Lang -->

<template>
  <div class="col span-2 gap-5 p-10">
    <div class="user-info m-1">
      <div>
          <h1 class="text-4xl font-bold">{{ name }} </h1>
          <div class="inline-flex flex-row">
            <div class="p-2">Role: {{ role }}</div>
            <!-- <div class="p-2">Created account on {{ create_date }}</div> -->
            <div class="p-2">Verified Labeler: <span v-if="verified">Yes</span> <span v-else>No</span> </div>
            <div class="p-2">No. of Contributions: {{ num_images }}</div>
          </div>
      </div>
      <!-- Not used in current implementation -->
      <!-- <div class="user-bio">
          <p>{{ user_bio }}</p>
      </div> --> 
    </div>
    <div class="user-image-gallery m-2">
      <h2 class="text-lg font-bold">Image Uploads</h2>
      <div class="container rounded-b">
        <div v-if="error" class="text-2xl font-bold">{{ error }}</div>
        <li v-for="path in img_data">
          <UserImg :src_path="path"/>
        </li>
      </div>
    </div>
  </div>
    <!-- count number of contributions from image database -->
    <!-- Display images from the image database with label -->
</template>

<script>
import UserImg from '../components/UserImg.vue'
import { ref } from '@vue/reactivity'
import { authStore } from '@/store/authenticate'
import { onMounted } from '@vue/runtime-core'
import axios from 'axios'
import { useRouter } from 'vue-router'

export default {
  name : 'ProfileView',
  data() {
    return {
      img_paths: ['../assets/sage.jpg'],
      verified: false,
    }
  },
  setup(){
    const store = authStore()
    const create_date = ref('01/01/1970')
    const name = ref('Anonymous User')
    const id = ref('')
    const error = ref('Failed to Retrieve Data')
    const info = ref('')
    const num_images = ref(0)
    const img_data = ref('')
    const role = ref('Not Logged In')

    onMounted(async () => {
      const data = await store.userData()
      if (data) {
        name.value = data.name
        id.value = data.id
        role.value = data.role
      }

      axios
        .post('http://127.0.0.1:5000/profile/', {id: data.id})
        .then(response => (info.value = response.data,
                           num_images.value = response.data['img_count'],
                           img_data.value = response.data['img_data'],
                           console.log(response),
                           console.log(img_data.value),
                           error.value = null))
        .catch(error.value = "Failed to Retrieve Data")
    })
    return { name, error, info, num_images, img_data, create_date, role }
  },
  components: {UserImg},
  beforeMount() {
    const store = authStore()
    if (!store.isAuthenticated()) {
      const router = useRouter()
      router.push({name: 'login'})
    }
  }
}
</script>

<style>
.user-info {
  justify-items: left;
}
.flex {
  justify-content: center;
}
.container {
  height: 80%;
  width: 100%;
}
.container li {
    list-style-type: none;
}
</style>