<template>
  <div class="flex flex-col p-3 gap-2 bg-slate-100 rounded-lg">
    <div class="h-fit flex flex-row items-center gap-2">
      <span class="text-left truncate">{{ datasetName }}</span>
    </div>
    <img v-if="imageSrc" :src="imageSrc" class="aspect-square min-w-24" />
    <div
      v-else
      class="text-lg flex flex-row justify-center items-center border-2 border-dashed border-slate-300 min-w-24 aspect-square"
    >
      No image
    </div>
  </div>
</template>

<script setup>
import { PhotoIcon } from "@heroicons/vue/20/solid";

const props = defineProps({
  datasetName: String,
  imageSrc: String,
});
</script>

<!-- <script>
export default {
  props: {
    datasetName: String,
    imageSrc: String,
  },
};
</script> -->
