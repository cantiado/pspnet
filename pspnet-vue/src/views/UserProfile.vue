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
      <span class="">Verified Labeler: {{ verified ? "Yes" : "No" }} </span>
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
      <h2 v-if="!error && Object.keys(uploadData).length==0" class="text-xl font-bold">No Uploaded Images</h2>
      <div v-if="error">
        <div role="status" class="flex flex-row justify-center">
          <svg
            aria-hidden="true"
            class="w-8 h-8 mr-2 text-gray-200 animate-spin dark:text-gray-600 fill-blue-600"
            viewBox="0 0 100 101"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z"
              fill="currentColor"
            />
            <path
              d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z"
              fill="currentFill"
            />
          </svg>
          <span class="text-2xl font-bold">{{ error }}</span>
        </div>
      </div>
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
const uploadData = ref({});

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
    if (role.value == "Principal Investigator") {verified.value = true;}
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
    .catch((error.value = "Retrieving Data..."));
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
