<!-- Author: Antonio Lang -->

<template>
  <div class="page">
      <div class="user-info m-1">
        <div>
            <h1 class="text-4xl font-bold">{{ name }} </h1>
            <div class="inline-flex flex-row">
              <div class="p-2">Role: {{ role }}</div>
              <!-- <div class="p-2">Created account on {{ create_date }}</div> -->
              <div class="p-2">Verified Labeler: <span v-if="verified">Yes</span> <span v-else>No</span> </div>
              <div class="p-2">No. of Contributions: {{ numImages }}</div>
            </div>
        </div>
        <!-- Not used in current implementation -->
        <!-- <div class="user-bio">
            <p>{{ user_bio }}</p>
        </div> --> 
      </div>
      <div class="userImageGallery m-2">
        <h2 class="text-lg font-bold">Image Uploads</h2>
        <div class="container rounded-b">
          <div v-if="error" class="text-2xl font-bold">{{ error }}</div>
          <li v-for="(value, index) in uploadData">
            <UserImg :imgURLs="value['paths']" :numUploaded="value['count']" :uploadID="index"/>
          </li>
        </div>
      </div>
  </div>
</template>

<script>
import UserImg from '../components/UserImg.vue'
import { ref } from '@vue/reactivity'
import { authStore } from '@/store/authenticate'
import { onMounted } from '@vue/runtime-core'
import axios from 'axios'
import { useRouter } from 'vue-router'
import b64toBlob from '@/composables/byteToBlob'

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

    const name = ref('Anonymous User')
    const id = ref('')
    const error = ref('Failed to Retrieve Data')
    const responseData = ref('')
    const numImages = ref(0)
    const img_data = ref('')
    const role = ref('Not Logged In')
    const uploadData = ref()

    onMounted(async () => {
      const data = await store.userData()
      if (data) {
        name.value = data.name
        id.value = data.id
        role.value = data.role
      }

      const getImgURL = (imgBytes) => {
            let tempArr = []
            for (var i = 0; i < imgBytes.length; i++) {
                tempArr.push(URL.createObjectURL(b64toBlob(imgBytes[i])))
            }
            return tempArr
        }

        const convertByUpload = (imageData) => {
            Object.keys(uploadData.value).forEach(function(key, index) {
                numImages.value += uploadData.value[key]['count']
                uploadData.value[key]['paths'] = getImgURL(imageData[key]['paths'])
            });
        }

      await axios
        .post('http://127.0.0.1:5000/profile/', {id: data.id})
        .then(response => (responseData.value = response.data,
                           uploadData.value = responseData.value,
                           console.log(responseData),
                           convertByUpload(response.data),
                           error.value = null))
        .catch(error.value = "Failed to Retrieve Data")
    })
    return { name, numImages, error, uploadData, role }
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
.flex {
  justify-content: center;
}
.container {
  height: 60%;
  width: 100%;
}
.container li {
    list-style-type: none;
}
.page {
  margin: 25px;
  margin-top: 15px;
  height: 75vh;
}
.userImageGallery {
  overflow-y: scroll;
  border-width: 5px;
  border-radius: 15px;
  border-color: #663300;
  margin-bottom: 10px;
}
</style>