<!-- Author: Antonio Lang -->

<template>
  <div class="col span-2 gap-5 p-10">
    <div class="user-info m-1">
      <div>
          <h1 class="text-4xl font-bold">{{ first_name }} {{ last_name }}</h1>
          <div class="inline-flex flex-row">
            <div class="p-2">Created account on {{ create_date }}</div>
            <div class="p-2">Verified Labeler: <span v-if="verified">Yes</span> <span v-else>No</span> </div>
            <div class="p-2">No. of Contributions: {{ num_images }}</div>
          </div>
      </div>
      <div class="user-bio">
          <p>{{ user_bio }}</p>
      </div>
    </div>
    <div class="user-image-gallery m-2">
      <h2 class="text-lg font-bold">Images Contributed</h2>
          <ul class="mdc-image-list my-image-list">
            <li class="mdc-image-list__item">
              <UserImg src_path="user_images/sage.jpg"/>
            </li>
          </ul>
    </div>
  </div>
    <!-- Reference user's name, account creation data, verifier, bio from database -->
    <!-- count number of contributions from image database -->
    <!-- Display images from the image database with label -->
</template>

<script>
import UserImg from '../components/UserImg.vue'

export default {
  data() {
    return {
      first_name: "John",
      last_name: "Doe",
      create_date: '01/01/1970',
      user_bio: 'Hello! I like studying the effects of wildfire!',
      num_images: 1,
      img_paths: ['../assets/sage.jpg'],
      verified: false
    }
  },
  components: {UserImg},
  setup() {

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
</style>