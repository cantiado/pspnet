<template>
  <button
    class="flex flex-col p-3 gap-2 bg-slate-100 hover:bg-slate-300 focus:bg-slate-300 rounded-lg"
    @click="emit('clicked', datasetName)"
  >
    <div class="h-fit w-full flex flex-row items-center gap-2">
      <PhotoIcon class="w-6 h-6" />
      <span class="text-left truncate">{{ datasetName }}</span>
    </div>
    <img v-if="imageSrc" :src="imageSrc" class="aspect-square min-w-24" />
    <div
      v-else
      class="text-lg w-full flex flex-row justify-center items-center border-2 border-dashed border-slate-500 min-w-24 aspect-square"
    >
      No image
    </div>
  </button>
</template>

<script setup>
import { PhotoIcon } from "@heroicons/vue/20/solid";

const props = defineProps({
  datasetName: String,
  imageSrc: String,
});

const emit = defineEmits(["clicked"])
</script>

<!-- <script>
export default {
  props: {
    datasetName: String,
    imageSrc: String,
  },
};
</script> -->
