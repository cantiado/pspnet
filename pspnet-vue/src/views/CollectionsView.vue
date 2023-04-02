<template>
  <div class="w-full h-[79.5vh] flex flex-row">
    <div class="h-full basis-1/6 bg-slate-100 p-5 border-r-2 flex flex-col">
      <button class="mb-5 px-5 py-2 hover:bg-green-400 hover:border-green-300 focus:bg-green-400 bg-green-300 rounded-full border-2 border-green-200">
        <span class="text-lg font-bold">+ New</span>
      </button>
      <button class="px-3 py-1 rounded-full hover:bg-slate-300 focus:outline-none focus:bg-slate-300">
        <span class="">My Collections</span>
      </button>
      <button class="px-3 py-1 rounded-full hover:bg-slate-300 focus:outline-none focus:bg-slate-300">
        <span>Shared with me</span>
      </button>
    </div>
    <div class="basis-5/6 p-5 overflow-auto flex flex-col gap-3">
      <span class="text-left font-bold text-sm">Projects</span>
      <div class="grid grid-cols-4 gap-4">
        <CollectionProject projectName="someProjectName1"/>
        <CollectionProject projectName="someProjectName2"/>
        <CollectionProject projectName="someProjectName3"/>
        <CollectionProject projectName="someProjectName4"/>
        <CollectionProject projectName="someProjectName5"/>
        <CollectionProject projectName="someProjectName6"/>
        <CollectionProject projectName="someProjectName7"/>
      </div>
      <span class="text-left font-bold text-sm">Datasets</span>
      <div class="grid grid-cols-4 gap-4">
        <CollectionDataset datasetName="my-really-long-dataset-name-is-really-long" />
        <CollectionDataset datasetName="another dataset" />
        <CollectionDataset datasetName="myFirstDataset" />
        <CollectionDataset datasetName="03/29/23" />
        <CollectionDataset datasetName="???????????ranoutofnames" />
      </div>
    </div>
  </div>
</template>

<script setup>
import CollectionDataset from "../components/CollectionDataset.vue"
import CollectionProject from "../components/CollectionProject.vue"
</script>