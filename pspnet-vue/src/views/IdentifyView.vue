<!-- Author: Carl Antiado -->
<template>
  <div class="w-full h-[79vh] flex flex-row">
    <div class="basis-1/3 p-5 h-full overflow-auto">
      <!-- flex flex-col gap-2 -->
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
      <FileList
        :files="files"
        @destroy="(fileId) => deleteFile(fileId)"
        class="mt-3"
      />
      <div class="mt-3 flex flex-col gap-3">
        <h1 class="text-lg font-bold">Dataset Information</h1>
        <div class="grid grid-cols-2 gap-3 text-right">
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
          <label
            for="dataset-notes"
            class="min-w-max block font-medium text-gray-900 dark:text-white"
            >Dataset notes:</label
          >
          <textarea
            v-model="datasetNotes"
            type="text"
            id="dataset-notes"
            placeholder="Optional"
            class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full px-2 py-1 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
          ></textarea>
          <label
            for="dataset-geoloc"
            class="min-w-max block font-medium text-gray-900 dark:text-white"
            >Dataset geolocation:</label
          >
          <input
            v-model="datasetGeoloc"
            type="text"
            id="dataset-geoloc"
            placeholder="Name, coords., etc."
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
      <div class="mt-3">
        <span v-if="!uploadedImages" class="text-red-400 text-sm"
          >Please upload images.
        </span>
        <span v-else-if="!datasetName" class="text-red-400 text-sm">
          Please enter a dataset name.
        </span>
        <span v-else-if="!visibility" class="text-red-400 text-sm">
          Please select a visibility setting.
        </span>
        <span v-else-if="!selectedModel" class="text-red-400 text-sm"
          >Please select a model.
        </span>
        <span v-if="errorMsg" class="text-red-400 text-sm">{{ errorMsg }}</span>
      </div>
      <div class="grid items-center gap-4 mt-3 grid-cols-2">
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
              class="absolute right-0 mt-2 w-full h-25 overflow-auto origin-top-right divide-y divide-gray-100 rounded-md bg-white shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none"
            >
              <div v-for="model in models" class="px-1 py-1">
                <MenuItem v-slot="{ active }">
                  <button
                    @click="setModel(model)"
                    :class="[
                      active ? 'bg-green-200' : 'text-gray-900',
                      'group flex w-full justify-center items-center rounded-md px-2 py-2 text-sm',
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
            !uploadedImages || !datasetName || !visibility || !selectedModel
              ? 'bg-gray-200'
              : 'bg-green-300 hover:bg-green-200'
          "
          :disabled="!uploadedImages || !selectedModel"
        >
          <span class="m-3 text-xl font-bold">Identify</span>
        </button>
      </div>
      <div class="mt-10 flex justify-center items-center">
        <button
          @click="reset"
          class="inline-flex justify-center rounded-md border border-transparent bg-red-400 px-4 py-2 text-sm font-bold text-slate-900 hover:bg-red-200 focus:outline-none focus-visible:ring-2 focus-visible:ring-slate-500 focus-visible:ring-offset-2"
        >
          RESET
        </button>
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
  <TransitionRoot appear :show="successfulSubmit" as="template">
    <Dialog
      as="div"
      @close="() => (successfulSubmit = false)"
      class="relative z-10"
    >
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
                Upload successful!
              </DialogTitle>
              <div class="mt-2">
                <p class="text-sm text-gray-500">
                  Your images were successfully submitted. You can monitor the
                  status of your images' identification in your Job Status page,
                  or you can submit another set of images.
                </p>
              </div>

              <div class="mt-4 flex flex-row gap-2">
                <button
                  type="button"
                  class="inline-flex justify-center rounded-md border border-transparent bg-blue-100 px-4 py-2 text-sm font-medium text-blue-900 hover:bg-blue-200 focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2"
                  @click="() => (successfulSubmit = false)"
                >
                  Job Status
                </button>
                <button
                  type="button"
                  class="text-xs font-normal px-4 py-2 rounded-md hover:bg-slate-200 focus:outline-none focus-visible:ring-2 focus-visible:ring-slate-500 focus-visible:ring-offset-2"
                  @click="reset"
                >
                  New dataset
                </button>
              </div>
            </DialogPanel>
          </TransitionChild>
        </div>
      </div>
    </Dialog>
  </TransitionRoot>
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
  TransitionRoot,
  TransitionChild,
  Dialog,
  DialogPanel,
  DialogTitle,
} from "@headlessui/vue";
import { ChevronDownIcon } from "@heroicons/vue/20/solid";
import ImageCard from "../components/ImageCard.vue";
import FileList from "../components/FileList.vue";

var id = 0;

export default {
  components: {
    Menu,
    MenuButton,
    MenuItem,
    MenuItems,
    ChevronDownIcon,
    ImageCard,
    FileList,
    RadioGroup,
    RadioGroupLabel,
    RadioGroupOption,
    RadioGroupDescription,
    TransitionRoot,
    TransitionChild,
    Dialog,
    DialogPanel,
    DialogTitle,
  },
  data() {
    return {
      uploadedImages: false,
      selectedModel: "",
      models: [{ name: "Model 1" }, { name: "Model 2" }, { name: "Model3" }],
      files: {}, // { id: { name, path, object } }
      FILETYPES: "image/png, image/jpeg",
      datasetName: "",
      datasetNotes: "",
      datasetGeoloc: "",
      visibility: "",
      successfulSubmit: false,
      errorMsg: "",
    };
  },
  computed: {},
  mounted() {},
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
        // console.log("after upload:", this.files);
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
      // console.log("after upload:", this.files);
      this.modifyFileList();
    },
    deleteFile(fileId) {
      delete this.files[fileId];
      if (Object.keys(this.files).length == 0) this.uploadedImages = false;
      // console.log("after delete:", this.files);
      this.modifyFileList();
    },
    modifyFileList() {
      const imageInput = document.getElementById("image-input");
      var newFileList = new DataTransfer();
      for (const fileId in this.files) {
        newFileList.items.add(this.files[fileId].object);
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
      fetch(url, {
        method: "POST",
        mode: "no-cors",
        body: images,
      })
        .then((res) => {
          // console.log(res)
          // console.log("successfully posted images");
          this.errorMsg = "";
          this.successfulSubmit = true;
        })
        .catch((err) => {
          console.log(err);
          this.errorMsg = "An error occured when submitting. Try again.";
        });
    },
    reset() {
      this.uploadedImages = false;
      this.selectedModel = "";
      this.files = {};
      this.modifyFileList()
      this.datasetName = "";
      this.datasetNotes = "";
      this.datasetGeoloc = "";
      this.visibility = "";
      this.successfulSubmit = false;
      this.errorMsg = "";
    },
  },
};
</script>
