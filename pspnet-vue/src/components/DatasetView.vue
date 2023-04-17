<!-- Author: Antonio Lang, styled by Carl Antiado -->

<template>
  <div class="w-full h-[79vh] flex flex-row">
    <div class="basis-1/4 p-5 bg-slate-50">
      <div class="flex flex-row items-center">
        <router-link to="/explore" class="basis-1/3">
          <div class="rounded px-3 py-2 bg-[#b9e0a5] text-white">
            Back to Explore
          </div>
        </router-link>
        <h1 class="basis-2/3 font-bold text-xl">{{ dsName }}</h1>
      </div>
      <div class="mt-5 border-t-2 pt-5 text-left">
        <h2 class="font-bold text-lg">Information</h2>
        <ul>
          <li>No. of Images: {{ numImages }}</li>
          <li>No. of Uploads: {{ numUploads }}</li>
          <!-- <li># Contributors: {{ numContributers }}</li> -->
          <!-- <li># Modifications: </li> -->
          <li>Size of Dataset: {{ dsSize }} MB</li>
        </ul>
      </div>
    </div>
    <div class="basis-3/4 p-5 max-h-[79.5vh] overflow-auto">
      <div class="grid grid-cols-1 gap-3">
        <div v-for="(value, index) in imgData" class="p-5 flex flex-col gap-5 border-2 rounded-lg">
          <div class="flex flex-row items-center gap-5">
            <h2 class="text-xl font-bold">Upload: {{ index + 1 }}</h2>
            <span>Number of Images: {{ value["count"] }}</span>
            <span>Submitted By: {{ value["user"] }}</span>
            <span v-if="value['notes']">Notes: {{ value["notes"] }}</span>
            <div 
              v-if="value['verified']" 
              class="italic border rounded p-1 border-[#b9e0a5]">
              Labels Verified</div>
              <button 
              v-else="!value['verified']" 
              @click="value['verified'] = updateLabels(imgData, dsName,value['id'])"
              class="border rounded p-1 border-black">
              Verify Labels
            </button>
            <!-- check user role to display verified button -->
          </div>
          <div class="flex flex-row flex-wrap gap-5">
            <div v-for="(img_value, img_index) in value['images']">
              <img
                class="object-cover h-48 w-48 p-1 bg-white border rounded max-w-sm"
                :src="img_value"
              />
              <span>{{ value["labels"][img_index] }}</span>
            </div>
          </div>
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
    numImages: Number,
  },

  setup(props) {
    const responseData = ref();
    const imgData = ref([]);
    const dsName = ref(props.dsName);
    const error = ref("");
    const numImages = ref(0);
    const numUploads = ref(0);
    const numContributers = ref(0);
    const dsSize = ref(0);

    const getURLs = (imgBytes) => {
      var returnURLs = [];
      for (var i = 0; i < imgBytes.length; i++) {
        returnURLs.push(URL.createObjectURL(b64toBlob(imgBytes[i])));
      }
      return returnURLs;
    };

    const updateLabels = (imgData, dsName, uploadID) => {
      var URL = "http://127.0.0.1:5000/datasetview/".concat(dsName).concat("/").concat(uploadID)
      axios.get(URL)
      return true
    };

    const convertByUpload = (imageData) => {
      for (var i = 0; i < imageData.length; i++) {
        imgData.value[i]["images"] = getURLs(imageData[i]["images"]);
      }
    };

    onMounted(async () => {
      if (dsName.value) {
        await axios
          .get("http://127.0.0.1:5000/datasetview/" + dsName.value + "/")
          .then(
            (response) => (
              (responseData.value = response.data),
              (imgData.value = response.data["upload_data"]),
              convertByUpload(response.data["upload_data"]),
              (numUploads.value = response.data["upload_data"].length),
              (numImages.value = response.data["num_images"]),
              (dsSize.value = response.data["ds_size"]),
              console.log(responseData.value),
              console.log(imgData.value)
            )
          )
          .catch((error.value = "Failed to retreive data"));
      }
    });

    return { imgData, numImages, numUploads, numContributers, dsSize, updateLabels };
  },
  components: { UserImg },
};
</script>
