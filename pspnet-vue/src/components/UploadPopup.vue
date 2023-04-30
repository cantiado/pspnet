<template>
  <div class="background" @click="closeView">
    <div class="window">
      <div class="dsName text-2xl font-bold">{{ dsName }} - Upload ID: {{ uploadID }}</div>
      <div class="imgContainer inline-grid grid-cols-3 gap-3">
        <div v-if="imgURLs" v-for="(path, index) in imgURLs" class="individualImg">
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
      var baseURL = "http://127.0.0.1:5000/datasetview/"
      var extension = props.dsName.concat('/').concat(props.uploadID).concat('/')
      var URL = baseURL.concat(extension)
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
