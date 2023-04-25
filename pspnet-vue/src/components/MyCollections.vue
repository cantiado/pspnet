<template>
  <div class="text-left flex flex-col gap-3 h-full">
    <h1 class="text-2xl font-bold border-b-2 pb-3">My Projects</h1>
    <div class="grid grid-cols-4 gap-4">
      <CollectionProject
        projectName="someProjectName1"
        @clicked="openProject"
      />
    </div>
    <h1 class="text-2xl font-bold border-b-2 pb-3">My Datasets</h1>
    <div class="grid grid-cols-4 gap-4">
      <CollectionDataset datasetName="myFirstDataset" @clicked="openDataset" />
    </div>
  </div>
</template>

<script setup>
import router from "@/router";
import CollectionDataset from "../components/CollectionDataset.vue";
import CollectionProject from "../components/CollectionProject.vue";

function openProject(projectName) {
  // console.log(projectName);
  router.push({ name: "singleProject", params: { projectName } });
}

function openDataset(datasetName) {
  router.push({ name: "singleDataset", params: { dsName: datasetName } });
}
</script>
