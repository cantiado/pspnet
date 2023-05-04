<!-- Author: Antonio Lang -->
<!-- Dropdown filter menu adapted from vue headless ui and tailwind-->

<template>
  <div
    class="w-full p-5 max-h-[79.5vh] overflow-auto flex flex-col justify-start items-center gap-5"
  >
    <div
      class="w-full flex flex-row justify-center items-center bg-slate-50 p-5 border-2"
    >
      <div class="w-full flex flex-col justify-start gap-2">
        <!-- following div component from tailwind elements -->
        <div class="">
          <input
            v-model="searchInput"
            type="search"
            class="form-control block w-full px-3 py-1.5 text-base font-normal text-gray-700 bg-white bg-clip-padding border border-solid border-gray-300 rounded transition ease-in-out m-0 focus:text-gray-700 focus:bg-white focus:border-blue-600 focus:outline-none"
            id="searchBar"
            placeholder="Dataset name"
            @change="searchFilter"
          />
        </div>
        <!-- following div component from tailwind elements -->
        <Menu as="div" class="flex flex-row gap-3 justify-start">
          <MenuButton
            as="div"
            class="dropdown-toggle px-6 py-2.5 bg-[#b9e0a5] text-black font-medium text-sm uppercase rounded shadow-md hover:bg-green-800 hover:shadow-lg focus:bg-green-800 focus:shadow-lg focus:outline-none focus:ring-0 text-white active:bg-[#b9e0a5] active:shadow-lg active:text-black transition duration-150 ease-in-out flex items-center whitespace-nowrap"
            >Filters</MenuButton
          >
          <transition
            enter-active-class="transition duration-100 ease-out"
            enter-from-class="transform scale-95 opacity-0"
            enter-to-class="transform scale-100 opacity-100"
            leave-active-class="transition duration-75 ease-in"
            leave-from-class="transform scale-100 opacity-100"
            leave-to-class="transform scale-95 opacity-0"
          >
            <MenuItems class="w-fill flex flex-row">
              <!-- Use the `active` state to conditionally style the active item. -->
              <MenuItem
                v-for="link in links"
                :key="link.href"
                as="div"
                v-slot="active"
                class="group flex w-full items-center justify-center px-2 py-2 text-sm border bg-white hover:bg-gray-200"
                @click="applyFilter(link.filter)"
              >
                {{ link.label }}
              </MenuItem>
            </MenuItems>
          </transition>
        </Menu>
      </div>
    </div>
    <div class="w-full flex flex-col gap-3">
      <div v-if="error != null">
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
      <router-link
        :to="{ name: 'singleDataset', params: { dsName: index }, props: true }"
        v-for="(value, index) in filteredData"
        :key="index"
      >
        <!-- <div v-for="(value, index) in filteredData" :key="index" @click="openDataset(index)"> -->
        <div class="prevBox">
          <div v-if="value['show']">
            <DataSetPrev
              :ds_name="index"
              :ds_count="value['count']"
              :img_paths="value['paths']"
              :location="value['location']"
              :description="value['description']"
            />
          </div>
        </div>
      </router-link>
    </div>
  </div>
</template>

<script setup>
import DataSetPrev from "@/components/DataSetPrev.vue";
import DatasetView from "@/components/DatasetView.vue";
import axios from "axios";
import { ref, onMounted } from "vue";
import { Menu, MenuButton, MenuItems, MenuItem } from "@headlessui/vue";
import b64toBlob from "@/composables/byteToBlob";

const error = ref("Retrieving data...");
const active = ref(true);
const searchInput = ref("");
const filteredData = ref("");
const ds_info = ref("");
const ds_modal = ref("");
const show_modal = ref(false);
const datasets = ref([]);
const images = ref([]);
const image_urls = ref([]);

const links = [
  { filter: "img l 5", label: "< 5 images" },
  { filter: "img g 5", label: "> 5 images" },
  { filter: "reset", label: "Reset" },
  // { filter: 'class eq 1', label: 'Single-Class Datasets'}
];

function searchFilter() {
  Object.fromEntries(
    Object.entries(ds_info.value).filter(([k, v]) => {
      let condition = k.includes(searchInput.value);
      if (condition) v["show"] = true;
      else v["show"] = false;
    })
  );
  console.log(filteredData.value);
}

function applyFilter(filter) {
  if (filter == "img l 5") {
    console.log("Filter datasets with fewer than 5 images");
    // Adapted from: https://9to5answer.com/how-to-filter-a-dictionary-by-value-in-javascript
    // filteredData.value = Object.fromEntries(Object.entries(ds_info.value).filter(([k,v]) => v['count']<5));
    Object.entries(filteredData.value).filter(([k, v]) => {
      let condition = v["count"] < 5;
      if (condition) v["show"] = true;
      else v["show"] = false;
    });
  }
  if (filter == "img g 5") {
    console.log("Filter datasets with greater than 5 images");
    // Adapted from: https://9to5answer.com/how-to-filter-a-dictionary-by-value-in-javascript
    Object.fromEntries(
      Object.entries(filteredData.value).filter(([k, v]) => {
        let condition = v["count"] > 5;
        if (condition) v["show"] = true;
        else v["show"] = false;
      })
    );
  }
  if (filter == "class eq 1") {
    console.log("Filter datasets with one class");
    console.log(filteredData.value);
  }
  if (filter == "reset") {
    console.log("Reset");
    Object.fromEntries(
      Object.entries(filteredData.value).filter(([k, v]) => {
        v["show"] = true;
      })
    );
  }
}

function openDataset(ds_name) {
  console.log("Open view for: " + ds_name);
  show_modal.value = true;
  ds_modal.value = ds_name;
}

function closeDataset(close) {
  show_modal.value = false;
}

function getImgURL(imgBytes) {
  let tempArr = [];
  for (var i = 0; i < imgBytes.length; i++) {
    tempArr.push(URL.createObjectURL(b64toBlob(imgBytes[i])));
  }
  return tempArr;
}

function convertByDataset() {
  Object.keys(ds_info.value).forEach(function (key, index) {
    ds_info.value[key]["paths"] = getImgURL(ds_info.value[key]["paths"]);
  });
}

onMounted(async () => {
  await axios
    .get("http://127.0.0.1:5000/explore/")
    .then(
      (response) => (
        (ds_info.value = response.data["ds_info"]),
        (filteredData.value = response.data["ds_info"]),
        convertByDataset(),
        console.log(filteredData.value),
        (error.value = null)
      )
    )
    .catch((error.value = "Retrieving data..."));
});
</script>

<style></style>
