<!-- Author: Carl Antiado -->
<template>
  <div class="w-full flex flex-row">
    <div class="basis-1/3 h-[79vh] p-5 flex flex-col gap-2">
      <label
        class="p-5 flex items-center justify-center gap-4 border-2 rounded-xl border-dashed border-blue-400 cursor-pointer"
        for="image-input"
      >
        <svg
          class="h-10 w-10 text-blue-500"
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
          stroke-width="2"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"
          />
        </svg>
        <div class="flex flex-col">
          <h1 class="text-xl">Choose Images</h1>
          <p class="text-sm">Upload or drag & drop (PNG or JPEG)</p>
        </div>
      </label>
      <input
        @change="uploadImages"
        class="hidden"
        id="image-input"
        type="file"
        name="image-input"
        :accept="FILETYPES"
        multiple
      />
      <List :files="files" @destroy="(fileId) => deleteFile(fileId)" />
      <div>
        <h1 class="text-lg font-bold">Dataset Information</h1>
        <div class="flex gap-3 items-center">
          <label
            for="dataset-name"
            class="min-w-max block font-medium text-gray-900 dark:text-white"
            >Dataset name:</label
          >
          <input
            v-model="datasetName"
            type="text"
            id="dataset-name"
            placeholder="example-dataset-name"
            class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full px-2 py-1 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
          />
        </div>
        <RadioGroup v-model="visibility">
          <RadioGroupLabel class="sr-only">Dataset visibility</RadioGroupLabel>
          <div class="grid grid-cols-3 border-2">
            <RadioGroupOption v-slot="{ checked }" value="public">
              <RadioGroupLabel
                :class="{ 'bg-blue-200': checked }"
                class="block border"
                as="span"
                >Public</RadioGroupLabel
              >
            </RadioGroupOption>
            <RadioGroupOption v-slot="{ checked }" value="shared">
              <RadioGroupLabel
                :class="{ 'bg-blue-200': checked }"
                class="block border"
                as="span"
                >Shared</RadioGroupLabel
              >
            </RadioGroupOption>
            <RadioGroupOption v-slot="{ checked }" value="private">
              <RadioGroupLabel
                :class="{ 'bg-blue-200': checked }"
                class="block border"
                as="span"
                >Private</RadioGroupLabel
              >
            </RadioGroupOption>
          </div>
        </RadioGroup>
      </div>
      <div class="grid grid-cols-3 items-center gap-4">
        <Menu as="div" class="relative inline-block">
          <div class="flex flex-row gap-4 text-right items-center">
            <MenuButton
              class="inline-flex justify-end rounded-md bg-gray-200 px-4 py-2 font-medium hover:bg-gray-100 focus:outline-none focus-visible:ring-2 focus-visible:ring-black focus-visible:ring-opacity-75"
            >
              {{ selectedModel ? selectedModel : "Select model" }}
              <ChevronDownIcon class="ml-2 -mr-1 h-5 w-5" aria-hidden="true" />
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
                  <button
                    @click="setModel(model)"
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
        <button
          class="py-1 min-w-max p-1 bg-green-300 hover:bg-green-200 rounded-full"
        >
          <span class="m-3 text-xl font-bold">Identify</span>
        </button>
        <span v-if="!uploadedImages" class="mt-1 text-red-400 text-sm"
          >Please upload images.</span
        >
        <span v-else-if="!selectedModel" class="mt-1 text-red-400 text-sm"
          >Please select a model.</span
        >
      </div>
    </div>
    <div
      v-if="uploadedImages"
      class="basis-2/3 h-[79vh] grid grid-cols-3 gap-4 m-5 overflow-auto auto-rows-max border-2"
    >
      <ImageCard
        v-for="file of files"
        @destroy="deleteFile(file)"
        :filePath="file.path"
        :fileName="file.name"
      />
    </div>
    <div v-else class="basis-2/3 p-5">
      <div
        class="h-full flex flex-col place-content-center rounded-xl border-2 border-dashed border-slate-500 bg-white"
      >
        <span class="text-xl text-slate-500">No images uploaded</span>
      </div>
    </div>
  </div>
  <!-- <div class="w-full flex flex-row flex-wrap">
    <div class="basis-1/3 h-[79vh] flex flex-col p-5">
      <form class="flex flex-col" method="POST" action="http://127.0.0.1:5000/identify" enctype="multipart/form-data">
        <div  @drop="dropImages" @dragover="(event) => event.preventDefault()" id="file-upload" class="flex items-center justify-center font-sans">
          <label for="dropzone-file" class="mx-auto cursor-pointer flex w-full max-w-lg flex-row gap-x-1 items-center rounded-xl border-2 border-dashed border-blue-400 bg-white p-3 text-center">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-10 w-10 text-blue-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
            </svg>
            <h2 class="text-xl font-medium text-gray-700 tracking-wide">Choose Images</h2>
            <p class="text-gray-500 tracking-wide">Upload or drag & drop your file PNG or JPEG. </p>
            <input @change="uploadImages" id="dropzone-file" type="file" name="dropzone-file" :accept="FILETYPES" class="hidden" multiple />
          </label>
        </div>
        <List :items="files" @destroy="(file) => deleteFile(file)" />
        <div>
          <div v-if="!uploadedImages" class="p-5 flex flex-col items-center">
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
    <div v-if="uploadedImages" class="basis-2/3 h-[79vh] grid grid-cols-3 gap-4 p-5 overflow-auto auto-rows-max">
      <ImageCard v-for="file of files" @destroy="deleteFile(file)" :filePath="file.path" :fileName="file.name"/>
    </div>
    <div v-else class="basis-2/3 p-5">
      <div class="h-full flex flex-col place-content-center rounded-xl border-2 border-dashed border-slate-500 bg-white">
        <span class="text-xl text-slate-500">No images uploaded</span>
      </div>
    </div>
  </div> -->
</template>

<script>
import {
  Menu,
  MenuButton,
  MenuItem,
  MenuItems,
  RadioGroup,
  RadioGroupLabel,
  RadioGroupOption,
  RadioGroupDescription,
} from "@headlessui/vue";
import { ChevronDownIcon } from "@heroicons/vue/20/solid";
import ImageCard from "../components/ImageCard.vue";
import List from "../components/FileList.vue";

var id = 0;

export default {
  components: {
    Menu,
    MenuButton,
    MenuItem,
    MenuItems,
    ChevronDownIcon,
    ImageCard,
    List,
    RadioGroup,
    RadioGroupLabel,
    RadioGroupOption,
    RadioGroupDescription,
  },
  data() {
    return {
      uploadedImages: false,
      selectedModel: "",
      models: [{ name: "Model 1" }, { name: "Model 2" }],
      // dropzoneFile: null,
      files: {}, // { id: { name, path, object } }
      FILETYPES: "image/png, image/jpeg",
      datasetName: "",
      visibility: "",
    };
  },
  computed: {},
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
          this.files[id] = {
            // id: id,
            name: file.name,
            path: URL.createObjectURL(file),
            object: file,
          };
          id++;
          // this.files.push({ name: file.name, path: URL.createObjectURL(file) })
        }
        console.log("after upload:", this.files);
        this.modifyFileList();
      }
      // else {
      //   this.uploadedImages = false;
      // }
    },
    dropImages(event) {
      event.preventDefault();
      if (event.dataTransfer.items) {
        [...event.dataTransfer.items].forEach((item, i) => {
          if (item.kind === "file") {
            const file = item.getAsFile();
            // console.log(file)
            if (this.FILETYPES.includes(file.type)) {
              this.files[id] = {
                // id: id,
                name: file.name,
                path: URL.createObjectURL(file),
                object: file,
              };
              id++;
            } else
              console.log(
                `File ${file.name} is not of type "${this.FILETYPES}"`
              );
          }
        });
        this.uploadedImages = true;
      }
      console.log("after upload:", this.files);
      this.modifyFileList();
    },
    deleteFile(fileId) {
      delete this.files[fileId];
      // console.log(this.files);
      if (Object.keys(this.files).length == 0) this.uploadedImages = false;
      console.log("after delete:", this.files);
      this.modifyFileList();
      // this.files = this.files.filter((f) => f !== file);
      // console.log(this.files)
      // console.log(this.dropzoneFile.files)
      // for (const f of this.dropzoneFile.files) {
      //   console.log(f)
      // }
      // if (this.files.length == 0) this.uploadedImages = false;
    },
    modifyFileList() {
      const imageInput = document.getElementById("image-input");
      var newFileList = new DataTransfer();
      for (const { object } of this.files) {
        // for (const id in this.files) {
        // newFileList.items.add(this.files[id].object);
        newFileList.items.add(object);
      }
      // console.log("help", newFileList.files)
      imageInput.files = newFileList.files;
      // console.log("post", dropzoneFileInput.files)
    },
  },
};
</script>
