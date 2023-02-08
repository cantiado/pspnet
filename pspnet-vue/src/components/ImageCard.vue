<!-- Author: Carl Antiado -->
<template>
  <div class="max-w-sm rounded overflow-hidden shadow-lg h-fit">
    <img class="w-full aspect-square" :src="filePath">
    <div class="px-3 py-2 flex justify-between items-center">
      <div class="font-bold text-sm">{{ fileName.length > MAX_STR_LEN ? fileName.slice(0, MAX_STR_LEN - 3) + "..." : fileName }}</div>
      <button v-if="!noDelete" @click="deleteImageCard" class="w-8"><XCircleIcon /></button>
    </div>
  </div>
</template>

<script>
import { XCircleIcon} from '@heroicons/vue/20/solid'

export default {
  emits: ["destroy"],
  props: {
    filePath: String,
    fileName: String,
    noDelete: Boolean
  },
  components: {
    XCircleIcon
  },
  data() {
    return {
      MAX_STR_LEN: 20
    }
  },
  methods: {
    deleteImageCard() {
      this.$emit("destroy");
    }
  }
}
</script>