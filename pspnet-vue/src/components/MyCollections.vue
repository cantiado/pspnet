<template>
  <div class="text-left flex flex-col gap-3 h-full">
    <h1 class="text-2xl font-bold border-b-2 pb-3">My Projects</h1>
    <div class="grid grid-cols-4 gap-4">
      <div v-for="name in projectData">
        <CollectionProject
          :projectName=name
          @clicked="openProject"
        />

      </div>
    </div>
    <div class="flex flex-row items-center gap-3 border-b-2 pb-3">
      <h1 class="text-2xl font-bold">My Datasets</h1>
      <button
        @click="openModal"
        class="text-sm border-2 border-green-100 bg-green-200 hover:bg-green-300 px-2 py-1 rounded-lg"
      >
        + Add Dataset to Project
      </button>
    </div>
    <div class="grid grid-cols-4 gap-4">
      <CollectionDataset
        v-for="dataset in datasets"
        :datasetName="dataset"
        @clicked="openDataset"
      />
    </div>
  </div>
  <TransitionRoot appear :show="viewModal" as="template">
    <Dialog as="div" @close="closeModal" class="relative z-10">
      <TransitionChild
        as="template"
        enter="duration-300 ease-out"
        enter-from="opacity-0"
        enter-to="opacity-100"
        leave="duration-200 ease-in"
        leave-from="opacity-100"
        leave-to="opacity-0"
      >
        <div class="fixed inset-0 bg-black bg-opacity-25" />
      </TransitionChild>

      <div class="fixed inset-0 overflow-y-auto">
        <div
          class="flex min-h-full items-center justify-center p-4 text-center"
        >
          <TransitionChild
            as="template"
            enter="duration-300 ease-out"
            enter-from="opacity-0 scale-95"
            enter-to="opacity-100 scale-100"
            leave="duration-200 ease-in"
            leave-from="opacity-100 scale-100"
            leave-to="opacity-0 scale-95"
          >
            <DialogPanel
              class="w-full max-w-md transform overflow-hidden rounded-2xl bg-white p-6 text-left align-middle shadow-xl transition-all"
            >
              <DialogTitle
                as="h3"
                class="text-lg font-medium leading-6 text-gray-900"
              >
                Select target dataset(s) and destination project:
              </DialogTitle>
              <div class="mt-2">
                <div class="grid grid-cols-2 gap-3">
                  <h4 class="">Datasets</h4>
                  <h4 class="">Projects</h4>
                  <ul
                    class="border-2 flex flex-col w-full max-h-[50vh] overflow-y-auto overflow-x-hidden"
                  >
                    <li
                      v-for="(dataset, index) in datasets"
                      class="border w-full px-2 py-1"
                      :class="{
                        'bg-blue-100': selectedDatasetIndices.has(index),
                      }"
                      @click="toggleDataset(index)"
                    >
                      {{ dataset }}
                    </li>
                  </ul>
                  <ul
                    class="border-2 flex flex-col w-full max-h-[50vh] overflow-y-auto overflow-x-hidden"
                  >
                    <li
                      v-for="(project, index) in projects"
                      class="border w-full px-2 py-1"
                      :class="{ 'bg-blue-100': selectedProjectIndex == index }"
                      @click="selectProjectIndex(index)"
                    >
                      {{ project }}
                    </li>
                  </ul>
                </div>
              </div>

              <div class="mt-4 flex flex-row gap-2 justify-start">
                <button
                  v-if="
                    selectedDatasetIndices.size != 0 &&
                    selectedProjectIndex != -1
                  "
                  type="button"
                  class="inline-flex justify-center rounded-md border border-transparent bg-blue-100 px-4 py-2 text-sm font-medium text-blue-900 hover:bg-blue-200 focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2"
                  @click="addDatasetsToProject"
                >
                  Confirm
                </button>
                <button
                  v-else
                  type="button"
                  class="inline-flex justify-center rounded-md border border-transparent bg-gray-300 px-4 py-2 text-sm font-medium text-black"
                  disabled
                >
                  Confirm
                </button>
                <button
                  type="button"
                  class="text-xs font-normal px-4 py-2 rounded-md hover:bg-slate-200 focus:outline-none focus-visible:ring-2 focus-visible:ring-slate-500 focus-visible:ring-offset-2"
                  @click="closeModal"
                >
                  Cancel
                </button>
              </div>
            </DialogPanel>
          </TransitionChild>
        </div>
      </div>
    </Dialog>
  </TransitionRoot>
</template>

<script setup>
import router from "@/router";
import CollectionDataset from "../components/CollectionDataset.vue";
import CollectionProject from "../components/CollectionProject.vue";
import { ref, onMounted } from 'vue'
import axios from "axios";
import { authStore } from "@/store/authenticate";

const projectData = ref([]);
const error = ref("");
import { ref } from "vue";
import {
  TransitionRoot,
  TransitionChild,
  Dialog,
  DialogPanel,
  DialogTitle,
} from "@headlessui/vue";

// seeded datasets
const datasets = [
  "dataset1",
  "dataset2",
  "dataset3",
  "dataset4",
  "dataset5",
  "dataset6",
  "dataset7",
  "dataset8",
];

// seeded projects
const projects = ["project1", "project2", "project3"];

const selectedDatasetIndices = ref(new Set());
function toggleDataset(index) {
  if (selectedDatasetIndices.value.has(index)) {
    selectedDatasetIndices.value.delete(index);
  } else {
    selectedDatasetIndices.value.add(index);
  }
}
const selectedProjectIndex = ref(-1);
function selectProjectIndex(index) {
  selectedProjectIndex.value = index;
}

function openProject(projectName) {
  // console.log(projectName);
  router.push({ name: "singleProject", params: { projectName } });
}

function openDataset(datasetName) {
  router.push({ name: "singleDataset", params: { dsName: datasetName } });
}

onMounted(async () => {
  const data = await authStore().userData();
  if (data) {
    await axios.post("http://127.0.0.1:5000/collections/", {id:data.id})
      .then(
        (response) => (
          (projectData.value = response.data['projects']),
          // (datasetData.value = response.data['datasets']),
          console.log(projectData.value)
        )
      )
      .catch(error.value = "Error");
  }
});

const viewModal = ref(false);
function openModal() {
  viewModal.value = true;
}
function closeModal() {
  viewModal.value = false;
  selectedDatasetIndices.value = new Set();
  selectedProjectIndex.value = -1;
}

function addDatasetsToProject() {
  console.log("click");
  const selectedDatasetNames = datasets.filter((name, index) => {
    if (selectedDatasetIndices.value.has(index)) {
      return name;
    }
  });
  const selectedProjectName = projects[selectedProjectIndex.value];
  console.log(selectedDatasetNames, selectedProjectName);
  // do something with the dataset names and project name
  closeModal();
}
</script>
