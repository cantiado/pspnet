<template>
  <div class="w-full h-full flex flex-row justify-start items-stretch">
    <nav class="h-full text-left flex flex-col justify-start bg-slate-100">
      <router-link
        v-for="(section, index) in sections"
        :to="{ name: section }"
        :key="index"
        class="py-3 px-5 hover:bg-slate-200 focus:bg-slate-200 cursor-pointer"
        :class="{
          'bg-slate-200': currentSection == index && section == currentPathName,
        }"
        @click="selectSection(index)"
      >
        {{ section[0].toUpperCase() + section.slice(1) }}
      </router-link>
    </nav>
    <div class="w-full text-justify p-5 max-w-[75%]">
      <router-view />
    </div>
  </div>
</template>

<script>
import { useRouter } from "vue-router";

export default {
  data() {
    return {
      currentSection: -1,
      sections: [
        "abstract",
        "background",
        "goals",
        "dataset",
        "research",
        "resources",
      ],
    };
  },
  computed: {
    currentPathName() {
      const router = useRouter();
      return router.currentRoute.value.name;
    },
  },
  methods: {
    selectSection(i) {
      this.currentSection = i;
    },
  },
};
</script>
