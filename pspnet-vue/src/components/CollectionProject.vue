<template>
  <div class="px-3 py-2 bg-slate-100 rounded-lg flex flex-row">
    <span class="text-left truncate">{{ projectName }}</span>
  </div>
</template>

<script setup>
const props = defineProps({
  projectName: String
})
</script>