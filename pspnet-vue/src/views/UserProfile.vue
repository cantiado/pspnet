<!-- Author: Antonio Lang -->

<template>
  <div class="col span-2 gap-5 p-10">
    <div>{{ error }}</div>
    <div class="user-info m-1">
      <div>
          <h1 class="text-4xl font-bold">{{ name }} </h1>
          <div class="inline-flex flex-row">
            <div class="p-2">Created account on {{ create_date }}</div>
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
        <!-- <div>{{img_data[0]}}</div> -->
        <li v-for="path in img_data">
          <!-- <div>{{value}}</div> -->
          <UserImg :src_path="path"/>
        </li>
      </div>
    </div>
  </div>
    <!-- Reference user's name, account creation data, verifier, bio from database -->
    <!-- count number of contributions from image database -->
    <!-- Display images from the image database with label -->
</template>

<script>
import UserImg from '../components/UserImg.vue'
import { ref } from '@vue/reactivity'
import { authStore } from '@/store/authenticate'
import { onMounted } from '@vue/runtime-core'
import axios from 'axios'


export default {
  name : 'ProfileView',
  data() {
    return {
      create_date: '01/01/1970',
      // user_bio: 'Hello! I like studying the effects of wildfire!',
      img_paths: ['../assets/sage.jpg'],
      verified: false,
    }
  },
  setup(){
    const store = authStore()
    const name = ref('John Doe')
    const email = ref('')
    const id = ref('')
    const error = ref('')
    const info = ref('')
    const num_images = ref(1)
    const img_data = ref('')

    onMounted(async () => {
      const data = await store.userData()
      name.value = data.name
      email.value = data.email
      id.value = data.id

      axios
        .post('http://127.0.0.1:5000/profile/', {id: data.id})
        // .then(console.log("Connected"))
        .then(response => (info.value = response.data,
                           num_images.value = response.data['img_count'],
                           img_data.value = response.data['img_data'],
                           console.log(response),
                           console.log(img_data.value)))
        .catch(console.log("Failed to Retrieve Data"))
    })
    return { name, email, error, info, num_images, img_data }
  },
    // need to check on if jwt contains user id -> could be used to cross-reference
    // data from the image database
    // i.e. get an image from each upload from the user
  components: {UserImg}
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