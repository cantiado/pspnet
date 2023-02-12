<template>
  <ul class="w-full h-1/2 overflow-auto text-sm font-medium bg-white border border-gray-200 rounded-lg">
    <li v-for="item in items" :key="item.id" class="flex justify-between items-center px-4 py-2 border-b border-gray-200 rounded-t-lg">
      <span>{{ item.name.length > MAX_STR_LEN ? item.name.slice(0, MAX_STR_LEN - 3) + "..." : item.name }}</span>
      <button v-if="!noDelete" @click="deleteItem(item)" class="w-8"><XCircleIcon /></button>
    </li>
  </ul>
</template>

<script>
import { XCircleIcon} from '@heroicons/vue/20/solid'

export default {
  emits: ["destroy"],
  props: {
    items: Object,
    noDelete: Boolean
  },
  components: {
    XCircleIcon
  },
  data() {
    return {
      MAX_STR_LEN: 50
    }
  },
  methods: {
    deleteItem(item) {
      this.$emit("destroy", item);
    }
  }
}
</script>