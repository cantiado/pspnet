<template>
  <div class="w-full h-[79.5vh] flex flex-row">
    <div class="h-full min-w-max bg-slate-100 p-5 border-r-2 flex flex-col">
      <button
        class="mb-5 px-5 py-2 hover:bg-green-400 hover:border-green-300 focus:bg-green-400 bg-green-300 rounded-full border-2 border-green-200"
        @click="newProjectButton"
      >
        <span class="text-lg font-bold">+ New Project</span>
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
    <div class="w-full p-5 overflow-auto">
      <router-view />
    </div>
  </div>
  <TransitionRoot appear :show="viewModal" as="template">
    <Dialog as="div" @close="" class="relative z-10">
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
                Create New Project
              </DialogTitle>
              <div class="mt-2">
                <div class="flex flex-col items-start gap-3">
                  <label for="project-name-input">Project name</label>
                  <input
                    v-model="newProjectName"
                    class="w-full px-2 py-1 text-sm border border-black bg-slate-50"
                    id="project-name-input"
                    name="project-name-input"
                  />
                  <span v-if="errorMsg" class="text-red-500">{{ errorMsg }}</span>
                </div>
              </div>

              <div class="mt-4 flex flex-row gap-2 justify-start">
                <button
                  v-if="newProjectName"
                  type="button"
                  class="inline-flex justify-center rounded-md border border-transparent bg-blue-100 px-4 py-2 text-sm font-medium text-blue-900 hover:bg-blue-200 focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2"
                  @click="createNewProject"
                >
                  Create
                </button>
                <button
                  v-else
                  type="button"
                  class="inline-flex justify-center rounded-md border border-transparent bg-gray-300 px-4 py-2 text-sm font-medium text-black"
                  disabled
                >
                  Create
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
import { ref, onMounted } from "vue";
import axios from "axios";
import { authStore } from "@/store/authenticate";
import {
  TransitionRoot,
  TransitionChild,
  Dialog,
  DialogPanel,
  DialogTitle,
} from "@headlessui/vue";

const newProjectName = ref("");
const viewModal = ref(false);
const projectData = ref();
const datasetData = ref();
const error = ref();
const userID = ref();

function openModal() {
  viewModal.value = true;
  newProjectName.value = "";
}

function closeModal() {
  viewModal.value = false;
  newProjectName.value = "";
}

const errorMsg = ref("");

function createNewProject() {
  const valid = verifyProjectName(newProjectName.value);
  if (!valid) {
    errorMsg.value = "Invalid project name!"
    return
  }
  errorMsg.value = "";
  closeModal()
}

function verifyProjectName(name) {
  const nameInDB = ref(false)
  // if (name.indexOf(';') > -1) {
  //   return false
  // }
  axios.post("http://127.0.0.1:5000/collections/", 
  { project_name : name , user_id : userID.value })
  .then(
    (response) => (
      console.log(response.data),
      nameInDB.value = !response.data['success']
    )
    .catch(console.log(error))
  )
  return nameInDB.value
}

const viewOption = ref(0);

function newProjectButton() {
  router.push({ name: "collections" });
  selectMyCollections();
  openModal();
}

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
