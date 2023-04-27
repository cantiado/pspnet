<template>
  <div class="text-left flex flex-col gap-3 h-full">
    <h1 class="text-2xl font-bold border-b-2 pb-3">Shared Projects</h1>
    <div class="grid grid-cols-4 gap-4">
      <h1 v-if="projectData.length==0" 
          class="text-xl font-bold pb-3">
          No Shared Projects</h1>
      <div v-for="projectName in projectData">
        <CollectionProject
          :projectName=projectName
          @clicked="openProject"
        />
      </div>
    </div>
    <!-- <h1 class="text-2xl font-bold border-b-2 pb-3">Shared Datasets</h1>
    <div class="grid grid-cols-4 gap-4">
      <CollectionDataset datasetName="someSharedDataset" @clicked="openDataset" />
    </div> -->
  </div>
</template>

<script setup>
import router from "@/router";
import CollectionDataset from "../components/CollectionDataset.vue";
import CollectionProject from "../components/CollectionProject.vue";
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { authStore } from "@/store/authenticate";

const projectData = ref([]);
const datasetData = ref([]);

function openProject(projectName) {
  router.push({ name: "singleProject", params: { projectName } });
}

function openDataset(datasetName) {
  router.push({ name: "singleDataset", params: { dsName: datasetName } });
}

onMounted(async () => {
  const data = await authStore().userData();
  if (data) {
    await axios.post("http://127.0.0.1:5000/collections/shared/", {id:data.id})
    .then(
      (response) => (
        projectData.value = response.data['projects']
      )
    ).catch(console.log("Error"))
  }
});
</script>
