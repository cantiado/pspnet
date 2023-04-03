<template>
    <div class="w-full h-[79vh] flex flex-row">
        <div class="basis-1/3 p-5">
            <router-link to="/explore">
                <div class="rounded p-4 bg-[#b9e0a5] text-white">
                    Back to Explore
                </div>
            </router-link>
            <div>
                <ul>
                    <li><text class="font-bold">{{ dsName }}</text></li>
                    <li>No. of Images: {{ numImages }}</li>
                    <li>No. of Uploads: {{ numUploads }}</li>
                    <!-- <li># Contributors: {{ numContributers }}</li> -->
                    <!-- <li># Modifications: </li> -->
                    <li>Size of Dataset: {{ dsSize }} MB</li>

                </ul>
            </div>
        </div>
        <div class="basis-2/3 p-6 max-h-[79.5vh] overflow-auto">
            <div class="imgContainer inline-grid grid-cols-1 gap-3">
              <div v-for="(value, index) in imgData">
                <div>
                  <div class="text-xl font-bold">Upload: {{ index+1 }}</div>
                  <div>Number of Images: {{ value['count'] }}</div>
                  <div>Submitted By: {{ value['user'] }}</div>
                  <div class="inline-grid grid-cols-3 gap-3" v-for="(img_value, img_index) in value['images']">
                    <div>
                      <img
                            class="object-cover h-48 w-48 p-1 bg-white border rounded max-w-sm"
                            :src="img_value"
                        />
                        <span>{{ value['labels'][img_index] }}</span>
                    </div>
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
    numImages: Number
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
      var returnURLs = []
      for (var i = 0; i < imgBytes.length; i++) {
        returnURLs.push(URL.createObjectURL(b64toBlob(imgBytes[i])));
      }
      return returnURLs
    };

    const convertByUpload = (imageData) => {
        for (var i = 0; i < imageData.length; i++) {
          imgData.value[i]["images"] = getURLs(imageData[i]["images"]);
        };
      };

    onMounted(async () => {
      if (dsName.value) {
        await axios
          .get("http://127.0.0.1:5000/datasetview/" + dsName.value + "/")
          .then(
            (response) => (
                (responseData.value = response.data),
                imgData.value = response.data["upload_data"],
                convertByUpload(response.data["upload_data"]),
                numUploads.value = response.data["upload_data"].length,
                numImages.value = response.data["num_images"],
                dsSize.value = response.data["ds_size"],
                console.log(responseData.value),
                console.log(imgData.value)
            )
          )
          .catch((error.value = "Failed to retreive data"));
      }
    });

    return { imgData, numImages, numUploads, numContributers, dsSize };
  },
  components: { UserImg },
};
</script>