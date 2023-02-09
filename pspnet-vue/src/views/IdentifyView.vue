<!-- Author: Carl Antiado -->
<template>
  <div class="w-full flex flex-row flex-wrap">
    <div class="basis-1/3 flex flex-col p-5">
      <form method="POST" action="" enctype="multipart/form-data">
        <div id="file-upload" class="flex items-center justify-center font-sans">
          <label for="dropzone-file" class="mx-auto cursor-pointer flex w-full max-w-lg flex-col items-center rounded-xl border-2 border-dashed border-blue-400 bg-white p-6 text-center">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-10 w-10 text-blue-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
            </svg>
            <h2 class="mt-4 text-xl font-medium text-gray-700 tracking-wide">Choose Images</h2>
            <p class="mt-2 text-gray-500 tracking-wide">Upload or drag & drop your file PNG or JPEG. </p>
            <input @change="uploadImages" id="dropzone-file" type="file" accept="image/png, image/jpeg" class="hidden" multiple />
          </label>
        </div>
        <div v-if="!uploadedImages" class="m-5 flex flex-col items-center">
          <button disabled class="w-5/6 h-10 bg-gray-200 rounded-full">
            <span class="text-xl font-bold">
              Identify
            </span>
          </button>
          <span>Please upload image(s)</span>
        </div>
        <div v-else-if="!selectedModel" class="m-5 flex flex-col items-center">
          <button disabled class="w-5/6 h-10 bg-gray-200 rounded-full">
            <span class="text-xl font-bold">
              Identify
            </span>
          </button>
          <span>Please select a model</span>
        </div>
        <div v-else class="m-5 flex flex-col items-center">
          <button class="w-5/6 h-10 bg-green-300 hover:bg-green-200 rounded-full">
            <span class="text-xl font-bold">
              Identify
            </span>
          </button>
        </div>
      </form>
      <span class="text-xl m-5">Settings</span>
      <Menu as="div" class="relative inline-block">
        <div class="grid grid-cols-2 gap-4 text-right items-center">
          <span class="">Choose model:</span>
          <MenuButton class="inline-flex justify-end rounded-md bg-gray-200 px-4 py-2 font-medium hover:bg-gray-100 focus:outline-none focus-visible:ring-2 focus-visible:ring-black focus-visible:ring-opacity-75">
            {{ selectedModel ? selectedModel : "Choose a model" }}
            <ChevronDownIcon
            class="ml-2 -mr-1 h-5 w-5"
            aria-hidden="true"
            />
          </MenuButton>
        </div>
        <transition
          enter-active-class="transition duration-100 ease-out"
          enter-from-class="transform scale-95 opacity-0"
          enter-to-class="transform scale-100 opacity-100"
          leave-active-class="transition duration-75 ease-in"
          leave-from-class="transform scale-100 opacity-100"
          leave-to-class="transform scale-95 opacity-0"
        >
          <MenuItems
            class="absolute right-0 mt-2 w-40 origin-top-right divide-y divide-gray-100 rounded-md bg-white shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none"
          >
            <div v-for="model in models" class="px-1 py-1">
              <MenuItem v-slot="{ active }">
                <button @click="setModel(model)"
                  :class="[
                    active ? 'bg-green-200' : 'text-gray-900',
                    'group flex w-full items-center rounded-md px-2 py-2 text-sm',
                  ]"
                >
                  {{ model.name }}
                </button>
              </MenuItem>
            </div>
          </MenuItems>
        </transition>
      </Menu>
    </div>
    <div v-if="uploadedImages" class="basis-2/3 grid grid-cols-3 gap-4 p-5">
      <ImageCard v-for="file of files" @destroy="deleteFile(file)" :filePath="file.path" :fileName="file.name"/>
    </div>
    <div v-else class="basis-2/3 p-5">
      <div class="h-full flex flex-col place-content-center rounded-xl border-2 border-dashed border-slate-500 bg-white">
        <span class="text-xl text-slate-500">No images uploaded</span>
      </div>
    </div>
  </div>
</template>

<script>
import { Menu, MenuButton, MenuItem, MenuItems } from '@headlessui/vue'
import { ChevronDownIcon } from '@heroicons/vue/20/solid'
import ImageCard from "../components/ImageCard.vue"

var id = 0;

export default {
  components: {
    Menu, MenuButton, MenuItem, MenuItems, ChevronDownIcon, ImageCard
  },
  data() {
    return {
      uploadedImages: false,
      selectedModel: '',
      models: [
        { name: 'Model 1' },
        { name: 'Model 2' },
        { name: 'Model 3' },
        { name: 'Model 4' },
      ],
      // dropzoneFile: null,
      files: {}
    }
  },
  computed: {

  },
  mounted() {
    // this.dropzoneFile = document.getElementById('dropzone-file');
  },
  methods: {
    setModel(model) {
      this.selectedModel = model.name;
    },
    uploadImages(event) {
      if (event.target.files.length != 0) {
        this.uploadedImages = true;
        for (let file of event.target.files) {
          this.files[id] = { id: id, name: file.name, path: URL.createObjectURL(file), object: file };
          id++;
          // this.files.push({ name: file.name, path: URL.createObjectURL(file) })
        }
      }
      console.log("after upload:", this.files)
      // else {
      //   this.uploadedImages = false;
      // }
    },
    deleteFile(file) {
      delete this.files[file.id];
      console.log(this.files);
      if (Object.keys(this.files).length == 0) this.uploadedImages = false;
      console.log("after delete:", this.files)
      // this.files = this.files.filter((f) => f !== file);
      // console.log(this.files)
      // console.log(this.dropzoneFile.files)
      // for (const f of this.dropzoneFile.files) {
      //   console.log(f)
      // }
      // if (this.files.length == 0) this.uploadedImages = false;
    }
  }
}
</script>