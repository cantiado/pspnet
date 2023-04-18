<template>
  <div class="w-full h-[79.5vh] flex flex-row">
    <div class="h-full basis-1/6 bg-slate-100 p-5 border-r-2 flex flex-col">
      <button
        class="mb-5 px-5 py-2 hover:bg-green-400 hover:border-green-300 focus:bg-green-400 bg-green-300 rounded-full border-2 border-green-200"
      >
        <span class="text-lg font-bold">+ New</span>
      </button>
      <router-link
        :to="{ name: 'collections' }"
        class="px-3 py-1 rounded-full hover:bg-slate-300"
        :class="{ 'bg-blue-300': viewOption == 0 }"
        @click="selectMyCollections"
      >
        <span>My Collections</span>
      </router-link>
      <router-link
        :to="{ name: 'shared' }"
        class="px-3 py-1 rounded-full hover:bg-slate-300"
        :class="{ 'bg-blue-300': viewOption == 1 }"
        @click="selectSharedCollections"
      >
        <span>Shared with me</span>
      </router-link>
      <router-link
        :to="{ name: 'affiliates' }"
        class="px-3 py-1 rounded-full hover:bg-slate-300"
        :class="{ 'bg-blue-300': viewOption == 2 }"
        @click="selectAffiliates"
      >
        <span>Affiliated Researchers</span>
      </router-link>
    </div>
    <div class="basis-5/6 p-5 overflow-auto">
      <router-view />
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";

const viewOption = ref(0);

function selectMyCollections() {
  viewOption.value = 0;
}

function selectSharedCollections() {
  viewOption.value = 1;
}

function selectAffiliates() {
  viewOption.value = 2;
}
</script>
