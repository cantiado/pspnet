<!-- Author: Antonio Lang -->

<template>
  <div class="col span-2 gap-4 p-2">
    <div>
        <h1>{{ first_name }} {{ last_name }}</h1>
        <p>Created account on {{ create_date }}</p>
        <p>Verified Labeler: {{ verified }}</p>
        <p>No. of Contributions: {{ num_images }}</p>
    </div>
    <div class="user-bio">
        <p>{{ user_bio }}</p>
    </div>
    <div class="user-image-gallery">
      <h2>Images Contributed</h2>
          <ul class="mdc-image-list my-image-list">
            <li class="mdc-image-list__item">
              <UserImg src_path="sage.jpg"/>
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

</style>