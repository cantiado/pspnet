<!-- Author: Antonio Lang -->

<template>
  <div
    class="w-full max-h-[79.5vh] flex flex-col justify-start items-center gap-3 p-5 overflow-auto"
  >
    <h1 class="text-4xl font-bold">{{ name }}</h1>
    <div
      class="flex flex-row gap-5 bg-slate-100 p-5 border border-slate-200 rounded-lg"
    >
      <span class="">Role: {{ role }}</span>
      <!-- <div class="p-2">Created account on {{ create_date }}</div> -->
      <span class=""> Verified Labeler: {{ verified ? "Yes" : "No" }} </span>
      <span class="">No. of Contributions: {{ numImages }}</span>
    </div>

    <!-- Not used in current implementation -->
    <!-- <div class="user-bio">
            <p>{{ user_bio }}</p>
        </div> -->
    <h2 class="text-xl font-bold">Image Uploads</h2>
    <div
      class="w-full flex flex-col gap-3 border-4 border-[#663300] rounded-md p-3"
    >
      <div v-if="error" class="text-2xl font-bold">{{ error }}</div>
      <div v-for="(value, index) in uploadData">
        <UserImg
          :imgURLs="value['paths']"
          :numUploaded="value['count']"
          :uploadID="index"
          :labels="value['labels']"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import UserImg from "../components/UserImg.vue";
import { ref, onMounted, onBeforeMount } from "vue";
import { authStore } from "@/store/authenticate";
import axios from "axios";
import { useRouter } from "vue-router";
import b64toBlob from "@/composables/byteToBlob";

const img_paths = ref(["../assets/sage.jpg"]);
const verified = ref(false);

const store = authStore();

const name = ref("Anonymous User");
const id = ref("");
const error = ref("Loading...");
const responseData = ref("");
const numImages = ref(0);
const img_data = ref("");
const role = ref("Not Logged In");
const uploadData = ref();

onBeforeMount(() => {
  if (!store.isAuthenticated()) {
    const router = useRouter();
    router.push({ name: "login" });
  }
});

onMounted(async () => {
  const data = await store.userData();
  if (data) {
    name.value = data.name;
    id.value = data.id;
    role.value = data.role;
  }

  const getImgURL = (imgBytes) => {
    let tempArr = [];
    for (var i = 0; i < imgBytes.length; i++) {
      tempArr.push(URL.createObjectURL(b64toBlob(imgBytes[i])));
    }
    return tempArr;
  };

  const convertByUpload = (imageData) => {
    Object.keys(uploadData.value).forEach(function (key, index) {
      numImages.value += uploadData.value[key]["count"];
      uploadData.value[key]["paths"] = getImgURL(imageData[key]["paths"]);
    });
  };

  await axios
    .post("http://127.0.0.1:5000/profile/", { id: data.id })
    .then(
      (response) => (
        (responseData.value = response.data),
        (uploadData.value = responseData.value),
        console.log(responseData),
        convertByUpload(response.data),
        (error.value = null)
      )
    )
    .catch((error.value = "Failed to Retrieve Data"));
});
</script>

<!-- <script>
import UserImg from "../components/UserImg.vue";
import { ref, onMounted, onBeforeMount } from "vue";
import { authStore } from "@/store/authenticate";
import axios from "axios";
import { useRouter } from "vue-router";
import b64toBlob from "@/composables/byteToBlob";

export default {
  name: "ProfileView",
  data() {
    return {
      img_paths: ["../assets/sage.jpg"],
      verified: false,
    };
  },
  setup() {
    const store = authStore();

    const name = ref("Anonymous User");
    const id = ref("");
    const error = ref("Loading...");
    const responseData = ref("");
    const numImages = ref(0);
    const img_data = ref("");
    const role = ref("Not Logged In");
    const uploadData = ref();

    onMounted(async () => {
      const data = await store.userData();
      if (data) {
        name.value = data.name;
        id.value = data.id;
        role.value = data.role;
      }

      const getImgURL = (imgBytes) => {
        let tempArr = [];
        for (var i = 0; i < imgBytes.length; i++) {
          tempArr.push(URL.createObjectURL(b64toBlob(imgBytes[i])));
        }
        return tempArr;
      };

      const convertByUpload = (imageData) => {
        Object.keys(uploadData.value).forEach(function (key, index) {
          numImages.value += uploadData.value[key]["count"];
          uploadData.value[key]["paths"] = getImgURL(imageData[key]["paths"]);
        });
      };

      await axios
        .post("http://127.0.0.1:5000/profile/", { id: data.id })
        .then(
          (response) => (
            (responseData.value = response.data),
            (uploadData.value = responseData.value),
            console.log(responseData),
            convertByUpload(response.data),
            (error.value = null)
          )
        )
        .catch((error.value = "Failed to Retrieve Data"));
    });
    return { name, numImages, error, uploadData, role };
  },
  components: { UserImg },
  beforeMount() {
    const store = authStore();
    if (!store.isAuthenticated()) {
      const router = useRouter();
      router.push({ name: "login" });
    }
  },
};
</script> -->

<style>
/* .flex {
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
} */
</style>
