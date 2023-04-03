<!-- Author: Antonio Lang -->
<!-- Dropdown filter menu adapted from vue headless ui and tailwind-->

<template>
  <div class="w-full p-5 max-h-[79.5vh] overflow-auto flex flex-col justify-start items-center gap-5">
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
      <div v-if="error != null" class="text-2xl font-bold">{{ error }}</div>
      <router-link :to="{ name: 'singleDataset', params: {dsName: index}, props: true }" v-for="(value, index) in filteredData" :key="index">
      <!-- <div v-for="(value, index) in filteredData" :key="index" @click="openDataset(index)"> -->
        <div class="prevBox" >
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
  { filter: "reset", label: "Reset"},
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
};

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
    console.log("Reset")
    Object.fromEntries(
      Object.entries(filteredData.value).filter(([k, v]) => {
        v["show"] = true;
      })
    );
  }
};

function openDataset(ds_name) {
  console.log("Open view for: " + ds_name);
  show_modal.value = true;
  ds_modal.value = ds_name;
};

function closeDataset(close) {
  show_modal.value = false;
};

function getImgURL(imgBytes) {
  let tempArr = [];
  for (var i = 0; i < imgBytes.length; i++) {
    tempArr.push(URL.createObjectURL(b64toBlob(imgBytes[i])));
  }
  return tempArr;
};

function convertByDataset(images) {
  Object.keys(ds_info.value).forEach(function (key, index) {
    ds_info.value[key]["paths"] = getImgURL(images[index]);
  });
};

onMounted(async () => {
  await axios
    .get("http://127.0.0.1:5000/explore/")
    .then(
      (response) => (
        (ds_info.value = response.data["ds_info"]),
        (filteredData.value = response.data["ds_info"]),
        (images.value = response.data["images"]),
        convertByDataset(images.value),
        console.log(response.data),
        (error.value = null)
      )
    )
    .catch((error.value = "Retrieving data..."));
});
</script>

<!-- <script>
import DataSetPrev from "@/components/DataSetPrev.vue";
import DatasetView from "@/components/DatasetView.vue";
import axios from "axios";
import { onMounted } from "vue";
import { ref } from "@vue/reactivity";
import { Menu, MenuButton, MenuItems, MenuItem } from "@headlessui/vue";
import b64toBlob from "@/composables/byteToBlob";

export default {
  name: "ExploreDataView",
  setup() {
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
      // { filter: 'class eq 1', label: 'Single-Class Datasets'}
    ];

    const searchFilter = () => {
      Object.fromEntries(
        Object.entries(ds_info.value).filter(([k, v]) => {
          let condition = k.includes(searchInput.value);
          if (condition) v["show"] = true;
          else v["show"] = false;
        })
      );
      console.log(filteredData.value);
    };

    const applyFilter = (filter) => {
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
          Object.entries(ds_info.value).filter(([k, v]) => {
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
    };

    const openDataset = (ds_name) => {
      console.log("Open view for: " + ds_name);
      show_modal.value = true;
      ds_modal.value = ds_name;
    };
    const closeDataset = (close) => {
      show_modal.value = false;
    };

    const getImgURL = (imgBytes) => {
      let tempArr = [];
      for (var i = 0; i < imgBytes.length; i++) {
        tempArr.push(URL.createObjectURL(b64toBlob(imgBytes[i])));
      }
      return tempArr;
    };

    const convertByDataset = (images) => {
      Object.keys(ds_info.value).forEach(function (key, index) {
        ds_info.value[key]["paths"] = getImgURL(images[index]);
      });
    };

    onMounted(async () => {
      await axios
        .get("http://127.0.0.1:5000/explore/")
        .then(
          (response) => (
            (ds_info.value = response.data["ds_info"]),
            (filteredData.value = response.data["ds_info"]),
            (images.value = response.data["images"]),
            convertByDataset(images.value),
            console.log(response.data),
            (error.value = null)
          )
        )
        .catch((error.value = "Retrieving data..."));
    });
    return {
      ds_info,
      datasets,
      filteredData,
      error,
      active,
      links,
      searchInput,
      applyFilter,
      searchFilter,
      openDataset,
      show_modal,
      closeDataset,
      ds_modal,
      image_urls,
    };
  },
  components: {
    DataSetPrev,
    DatasetView,
    Menu,
    MenuButton,
    MenuItem,
    MenuItems,
  },
};
</script> -->

<style>
/* .datasetPrevContainer {
  border-width: 3px;
  border-radius: 10px;
  overflow-y: scroll;
}
.container {
  gap: 20px;
  display: grid;
  overflow-y: scroll;
  padding: 10px;
  height: 70vh;
  width: 85%;
}
.container li {
  list-style-type: none;
  width: 90%;
  height: 100%;
}
.dropdown {
  border-color: aquamarine;
}
.fade {
  transition: all 0.5s ease;
}
.viewWindow {
  margin: 25px;
  margin-top: 15px;
  height: 75vh;
  width: 65vw;
  display: grid;
  grid-gap: 10px;
} */
</style>
