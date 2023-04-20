<template>
  <span class="text-left font-bold text-sm">Projects</span>
  <div class="grid grid-cols-4 gap-4">
    <CollectionProject projectName="someProjectName1" />
    <CollectionProject projectName="someProjectName2" />
    <CollectionProject projectName="someProjectName3" />
    <CollectionProject projectName="someProjectName4" />
    <CollectionProject projectName="someProjectName5" />
    <CollectionProject projectName="someProjectName6" />
    <CollectionProject projectName="someProjectName7" />
  </div>
  <span class="text-left font-bold text-sm">Datasets</span>
  <div class="grid grid-cols-4 gap-4">
    <CollectionDataset
      datasetName="my-really-long-dataset-name-is-really-long"
    />
    <CollectionDataset datasetName="another dataset" />
    <CollectionDataset datasetName="myFirstDataset" />
    <CollectionDataset datasetName="03/29/23" />
    <CollectionDataset datasetName="???????????ranoutofnames" />
  </div>
</template>

<script setup>
import CollectionDataset from "../components/CollectionDataset.vue";
import CollectionProject from "../components/CollectionProject.vue";
</script>
