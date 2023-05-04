<!-- Author: Antonio Lang, styled by Carl Antiado -->

<template>
  <div v-if="showUploadModal">
    <UploadPopup
      :dsName="dsName"
      :uploadID="modalUploadID"
      @closeModal="closeModal"
    />
  </div>
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
          <li>
            <button
              class="rounded px-3 py-2 bg-[#b9e0a5] text-white m-1"
              :href="url"
              @click.prevent="downloadDataset(dsName)"
            >
              Download
            </button>
          </li>
          <li>
            <button
              v-if="userID > 0"
              class="rounded px-3 py-2 bg-[#b9e0a5] text-white m-1"
              @click.prevent="saveDataset()"
            >
              Save Dataset
            </button>
          </li>
        </ul>
      </div>
    </div>
    <div class="basis-3/4 p-5 max-h-[79.5vh] overflow-auto">
      <div v-if="imgData.length == 0 && !responseData" class="w-full h-full flex flex-row items-center justify-center" role="status">
        <svg
          aria-hidden="true"
          class="w-16 h-16 mr-2 text-gray-200 animate-spin dark:text-gray-600 fill-blue-600"
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
      <div v-else class="grid grid-cols-1 gap-3">
        <div
          v-for="(value, index) in imgData.slice().reverse()"
          class="p-5 flex flex-col gap-5 border-2 rounded-lg"
        >
          <div class="flex flex-row items-center gap-5">
            <button
              class="text-xl font-bold border border-1 rounded p-1"
              @click="openModal(value['id'])"
            >
              Upload ID: {{ value["id"] }}
            </button>
            <span>Number of Images: {{ value["count"] }}</span>
            <span>Submitted By: {{ value["user"] }}</span>
            <span>Date: {{ value["timestamp"] }}</span>
            <span v-if="value['notes']">Notes: {{ value["notes"] }}</span>

            <button
              v-if="role === 'Principal Investigator' && !value['verified']"
              @click="
                value['verified'] = updateLabels(
                  value['verified'],
                  value['id'],
                  index
                )
              "
              class="border rounded p-1 border-black"
            >
              Verify Labels
            </button>
            <button
              v-else-if="role === 'Principal Investigator' && value['verified']"
              @click="
                value['verified'] = updateLabels(
                  value['verified'],
                  value['id'],
                  index
                )
              "
              class="italic border rounded p-1 border-[#b9e0a5]"
            >
              Labels Verified
            </button>
            <div
              v-else-if="value['verified']"
              class="italic border rounded p-1 border-[#b9e0a5]"
            >
              Labels Verified
            </div>
            <!-- check conditions for the button vs not -->
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
import UploadPopup from "./UploadPopup.vue";
import { onMounted } from "vue";
import b64toBlob from "@/composables/byteToBlob";
import { authStore } from "@/store/authenticate";

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
    const store = authStore();
    const role = ref(0);
    const userID = ref(0);
    const baseDownloadURL = ref("http://127.0.0.1:5000/datasetview/");
    const saveURL = ref(
      "http://127.0.0.1:5000/explore/" + dsName.value + "/save/"
    );
    const showUploadModal = ref(false);
    const modalUploadID = ref();

    const downloadDataset = (dsName) => {
      var downloadURL = baseDownloadURL.value
        .concat(dsName)
        .concat("/download/");
      axios
        .get(downloadURL, { responseType: "blob" })
        .then((response) => {
          const blob = new Blob([response.data], { type: "zip" });
          const link = document.createElement("a");
          link.href = URL.createObjectURL(blob);
          link.download = dsName + ".zip";
          link.click();
          URL.revokeObjectURL(link.href);
        })
        .catch(console.error);
    };

    const saveDataset = () => {
      var success = false;
      axios
        .post(saveURL.value, { id: userID.value })
        .then((response) => {
          console.log(response.data);
          success = response.data["success"];
        })
        .catch(console.log(""));
      return success;
    };

    function openModal(uploadID) {
      modalUploadID.value = uploadID;
      showUploadModal.value = true;
    }

    function closeModal(close) {
      showUploadModal.value = false;
    }

    const getURLs = (imgBytes) => {
      var returnURLs = [];
      for (var i = 0; i < imgBytes.length; i++) {
        returnURLs.push(URL.createObjectURL(b64toBlob(imgBytes[i])));
      }
      return returnURLs;
    };

    const checkRole = () => {
      console.log(store);
    };

    const updateLabels = async (verified, uploadID, index) => {
      var baseURL = "http://127.0.0.1:5000/datasetview/";
      var extension = dsName.value
        .concat("/")
        .concat(uploadID)
        .concat("/")
        .concat("updateLabel")
        .concat("/");
      var URL = baseURL.concat(extension);
      var newLabel;
      await axios.get(URL).then(
        (response) => (
          (newLabel = response.data["verified"]),
          (imgData.value[imgData.value.length - 1 - index]["verified"] =
            newLabel)
          // verified.value = newLabel)
          // imgData.value[dsName][index]['verified'] = newLabel)
        )
      );
      console.log(imgData.value);
      return newLabel;
    };

    const convertByUpload = (imageData) => {
      for (var i = 0; i < imageData.length; i++) {
        imgData.value[i]["images"] = getURLs(imageData[i]["images"]);
      }
    };

    const convertToDate = (upload) => {
      const monthNames = [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
      ];
      for (var i = 0; i < upload.length; i++) {
        var timestamp = new Date(Number(upload[i]["timestamp"]));
        upload[i]["timestamp"] =
          String(timestamp.getFullYear()) +
          " " +
          monthNames[timestamp.getMonth()] +
          " " +
          String(timestamp.getDate());
      }
    };

    onMounted(async () => {
      const data = await store.userData();
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
              convertToDate(response.data["upload_data"])
            )
          )
          .catch((error.value = "Failed to retreive data"));
      }
      if (data) {
        role.value = data.role;
        userID.value = data.id;
      }
    });

    return {
      imgData,
      numImages,
      numUploads,
      numContributers,
      dsSize,
      updateLabels,
      role,
      url: baseDownloadURL,
      downloadDataset,
      saveDataset,
      userID,
      openModal,
      closeModal,
      showUploadModal,
      modalUploadID,
    };
  },
  components: { UserImg, UploadPopup },
};
</script>
