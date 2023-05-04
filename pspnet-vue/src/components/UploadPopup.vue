<template>
  <div class="background" @click="closeView">
    <div class="window">
      <div class="dsName text-2xl font-bold">
        {{ dsName }} - Upload ID: {{ uploadID }}
      </div>
      <div v-if="imgURLs.length == 0 && !responseData" class="flex flex-row justify-center" role="status">
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
        <span class="sr-only">Loading...</span>
      </div>
      <div class="imgContainer inline-grid grid-cols-3 gap-3">
        <div
          v-if="imgURLs"
          v-for="(path, index) in imgURLs"
          class="individualImg"
        >
          <img
            class="object-cover h-48 w-48 p-1 bg-white border rounded max-w-sm"
            :src="path"
          />
          <span>{{ imgLabels[index] }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { ref } from "vue";
import UserImg from "./UserImg.vue";
import { onMounted } from "vue";
import b64toBlob from "@/composables/byteToBlob";

export default {
  props: {
    dsName: String,
    uploadID: Number,
  },
  setup(props, { emit }) {
    const responseData = ref();
    const imgURLs = ref([]);
    const imgLabels = ref([]);
    const dsName = ref(props.dsName);
    const error = ref("");

    const getURLs = (imgBytes) => {
      for (var i = 0; i < imgBytes.length; i++) {
        imgURLs.value.push(URL.createObjectURL(b64toBlob(imgBytes[i])));
      }
    };

    onMounted(async () => {
      var baseURL = "http://127.0.0.1:5000/datasetview/";
      var extension = props.dsName
        .concat("/")
        .concat(props.uploadID)
        .concat("/");
      var URL = baseURL.concat(extension);
      if (dsName.value) {
        await axios
          .get(URL)
          .then(
            (response) => (
              (responseData.value = response.data),
              getURLs(response.data["images"]),
              (imgLabels.value = responseData.value["labels"]),
              console.log(responseData.value)
            )
          )
          .catch((error.value = "Failed to retreive data"));
      }
    });

    const closeView = () => {
      emit("closeModal", true);
    };

    return { imgURLs, imgLabels, closeView, emit };
  },
  components: { UserImg },
};
</script>

<style>
.background {
  background: rgba(0, 0, 0, 0.25);
  top: 0;
  left: 0;
  position: fixed;
  width: 100%;
  height: 100%;
}
.window {
  background: white;
  position: relative;
  margin: 125px auto;
  border-width: 5px;
  border-radius: 5px;
  width: 60%;
  height: 60%;
  overflow-y: auto;
  padding: 15px;
}
.imgContainer {
  display: grid;
}
.individualImg {
  width: auto;
  position: relative;
}
.dsName {
  margin-bottom: 15px;
}
</style>
