<template>
  <button
    class="px-3 py-2 bg-slate-100 hover:bg-slate-300 focus:bg-slate-300 rounded-lg flex flex-row"
    @click="emit('clicked', projectName)"
  >
    <span class="text-left truncate">{{ projectName }}</span>
  </button>
</template>

<script setup>
const props = defineProps({
  projectName: String,
});

const emit = defineEmits(["clicked"]);
</script>
