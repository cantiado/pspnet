<template>
  <div class="text-left flex flex-col gap-3 h-full">
    <h1 class="text-2xl font-bold border-b-2 pb-3">My Projects</h1>
    <div class="grid grid-cols-4 gap-4">
      <div v-for="name in projectData">
        <CollectionProject
          :projectName=name
          @clicked="openProject"
        />

      </div>
    </div>
    <!-- <h1 class="text-2xl font-bold border-b-2 pb-3">My Datasets</h1>
    <div class="grid grid-cols-4 gap-4">
      <CollectionDataset datasetName="myFirstDataset" @clicked="openDataset" />
    </div> -->
  </div>
</template>

<script setup>
import router from "@/router";
import CollectionDataset from "../components/CollectionDataset.vue";
import CollectionProject from "../components/CollectionProject.vue";
import { ref, onMounted } from 'vue'
import axios from "axios";
import { authStore } from "@/store/authenticate";

const projectData = ref([]);
const error = ref("");

function openProject(projectName) {
  // console.log(projectName);
  router.push({ name: "singleProject", params: { projectName } });
}

function openDataset(datasetName) {
  router.push({ name: "singleDataset", params: { dsName: datasetName } });
}

onMounted(async () => {
  const data = await authStore().userData();
  if (data) {
    await axios.post("http://127.0.0.1:5000/collections/", {id:data.id})
      .then(
        (response) => (
          (projectData.value = response.data['projects']),
          // (datasetData.value = response.data['datasets']),
          console.log(projectData.value)
        )
      )
      .catch(error.value = "Error");
  }
});
</script>
