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
                    <li># Images: </li>
                    <li># Uploads: </li>
                    <li>Contributors: </li>
                    <li>Changes:</li>

                </ul>
            </div>
        </div>
        <div class="basis-2/3 p-5">
            <div class="imgContainer inline-grid grid-cols-3 gap-3">
                <div v-if="imgURLs" v-for="path in imgURLs" class="individualImg">
                <img
                    class="object-cover h-48 w-48 p-1 bg-white border rounded max-w-sm"
                    :src="path"
                />
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
  },

  setup(props) {
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
      if (dsName.value) {
        await axios
          .get("http://127.0.0.1:5000/datasetview/" + dsName.value + "/")
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

    return { imgURLs };
  },
  components: { UserImg },
};
</script>