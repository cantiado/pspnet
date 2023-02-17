<template>
  <div
    class="w-full border-2 border-gray-300 min-h-[100px] flex flex-col items-center"
  >
    <div class="relative w-full">
      <label
        for="search"
        class="mb-2 text-sm font-medium text-gray-900 sr-only dark:text-white"
        >Search</label
      >
      <div
        class="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none"
      >
        <svg
          aria-hidden="true"
          class="w-5 h-5 text-gray-500 dark:text-gray-400"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
          xmlns="http://www.w3.org/2000/svg"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
          ></path>
        </svg>
      </div>
      <input
        v-model="searchQuery"
        type="search"
        id="search"
        class="block w-full p-2 pl-10 text-sm text-gray-900 border border-gray-300 bg-gray-50 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
        placeholder="Search"
        :disabled="!Object.keys(files).length"
      />
    </div>
    <ul
      v-if="Object.keys(files).length"
      class="w-full overflow-auto text-sm font-medium bg-white border border-gray-200 rounded-lg"
    >
      <li
        v-for="(file, id) in files"
        :key="id"
        :class="{ hidden: searchQuery && !file.name.startsWith(searchQuery) }"
        class="flex justify-between items-center px-4 py-2 border border-gray-200"
      >
        <span class="block text-left">{{
          file.name.length > MAX_STR_LEN
            ? file.name.slice(0, MAX_STR_LEN - 3) + "..."
            : file.name
        }}</span>
        <button v-if="!noDelete" @click="deleteItem(id)" class="w-8">
          <XCircleIcon />
        </button>
      </li>
    </ul>
    <div v-else class="h-full flex flex-col justify-center">No images uploaded</div>
  </div>
</template>

<script>
import { XCircleIcon } from "@heroicons/vue/20/solid";

export default {
  emits: ["destroy"],
  props: {
    files: Object,
    noDelete: Boolean,
  },
  components: {
    XCircleIcon,
  },
  data() {
    return {
      MAX_STR_LEN: 50,
      searchQuery: "",
    };
  },
  methods: {
    deleteItem(key) {
      this.$emit("destroy", key);
    },
  },
};
</script>
