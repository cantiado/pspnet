<!-- Author: Carl Antiado -->
<template>
  <div class="w-full h-[79vh] flex flex-row">
    <div class="basis-1/3 p-5 flex flex-col gap-2">
      <div @drop="dropImages" @dragover="(event) => event.preventDefault()">
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
      </div>
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
        <!-- TODO: add notes, geolocation -->
        
      </div>
      <div
        class="grid items-center gap-4"
        :class="
          !uploadedImages || !selectedModel ? 'grid-cols-3' : 'grid-cols-2'
        "
      >
        <Menu as="div" class="relative inline-block">
          <div class="flex flex-row gap-4 text-right items-center">
            <MenuButton
              class="inline-flex w-full justify-end rounded-md bg-gray-200 px-4 py-2 font-medium hover:bg-gray-100 focus:outline-none focus-visible:ring-2 focus-visible:ring-black focus-visible:ring-opacity-75"
            >
              <span class="flex w-full justify-center">
                {{ selectedModel ? selectedModel : "Select model" }}
              </span>

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
              class="absolute left-0 mt-2 w-40 h-25 overflow-auto origin-top-right divide-y divide-gray-100 rounded-md bg-white shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none"
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
          @click="postImages"
          class="py-1 min-w-max p-1 rounded-full"
          :class="
            !uploadedImages || !selectedModel
              ? 'bg-gray-200'
              : 'bg-green-300 hover:bg-green-200'
          "
          :disabled="!uploadedImages || !selectedModel"
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
    <div class="basis-2/3 p-5">
      <div
        v-if="uploadedImages"
        class="h-full grid grid-cols-3 gap-4 p-1 overflow-auto auto-rows-max border-4"
      >
        <ImageCard
          v-for="(file, id) in files"
          @destroy="deleteFile(id)"
          :filePath="file.path"
          :fileName="file.name"
        />
      </div>
      <div
        v-else
        class="h-full flex flex-col place-content-center rounded-xl border-2 border-dashed border-slate-500 bg-white"
      >
        <span class="text-xl text-slate-500">No images uploaded</span>
      </div>
    </div>
  </div>
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
      models: [{ name: "Model 1" }, { name: "Model 2" }, { name: "Model3" }],
      files: {}, // { id: { name, path, object } }
      FILETYPES: "image/png, image/jpeg",
      datasetName: "",
      visibility: "",
    };
  },
  computed: {},
  mounted() {
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
            name: file.name,
            path: URL.createObjectURL(file),
            object: file,
          };
          id++;
        }
        console.log("after upload:", this.files);
        this.modifyFileList();
      }
    },
    dropImages(event) {
      event.preventDefault();
      if (event.dataTransfer.items) {
        [...event.dataTransfer.items].forEach((item, i) => {
          if (item.kind === "file") {
            const file = item.getAsFile();
            if (this.FILETYPES.includes(file.type)) {
              this.files[id] = {
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
      if (Object.keys(this.files).length == 0) this.uploadedImages = false;
      console.log("after delete:", this.files);
      this.modifyFileList();
    },
    modifyFileList() {
      const imageInput = document.getElementById("image-input");
      var newFileList = new DataTransfer();
      for (const { object } of this.files) {
        newFileList.items.add(object);
      }
      imageInput.files = newFileList.files;
    },
    postImages() {
      const url = "http://127.0.0.1:5000/identify";
      const imageInput = document.getElementById("image-input");
      const images = new FormData();
      for (const image of imageInput.files) {
        images.append("image-input", image);
      }
      const response = fetch(url, {
        method: "POST",
        body: images,
      })
        .then(() => console.log("successfully posted images"))
        .catch((err) => console.log(err));
    },
  },
};
</script>
