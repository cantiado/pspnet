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
        id="file-list"
        :files="files"
        @destroy="(fileId) => deleteFile(fileId)"
        class="mt-3"
      />
      <div class="mt-3 flex flex-col gap-3">
        <div class="flex flex-col items-center">
          <h1 class="text-lg font-bold">Dataset Information</h1>
          <button
            @click="
              () => {
                datasetHelp = true;
              }
            "
            class="px-3 w-fit flex flex-row justify-center gap-2 items-center text-sm"
          >
            Click for details
            <InformationCircleIcon class="h-7 w-7" />
          </button>
        </div>
        <div class="grid grid-cols-2 gap-3 text-right">
          <label
            for="dataset-name"
            class="min-w-max block font-medium text-gray-900"
            >Dataset name:</label
          >
          <input
            v-model="datasetName"
            type="text"
            id="dataset-name"
            placeholder="Required"
            class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full px-2 py-1"
          />
          <label
            for="dataset-notes"
            class="min-w-max block font-medium text-gray-900"
            >Dataset notes:</label
          >
          <textarea
            v-model="datasetNotes"
            type="text"
            id="dataset-notes"
            placeholder="Optional"
            class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full px-2 py-1"
          ></textarea>
          <label
            for="dataset-geoloc"
            class="min-w-max block font-medium text-gray-900"
            >Dataset geolocation:</label
          >
          <input
            v-model="datasetGeoloc"
            type="text"
            id="dataset-geoloc"
            placeholder="Optional"
            class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full px-2 py-1"
          />
          <label
            for="publications"
            class="min-w-max block font-medium text-gray-900"
            >Publications:</label
          >
          <input
            v-model="publications"
            type="text"
            id="publications"
            placeholder="Optional"
            class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full px-2 py-1"
          />
          <label
            for="related-works"
            class="min-w-max block font-medium text-gray-900"
            >Related Works:</label
          >
          <textarea
            v-model="relatedWorks"
            type="text"
            id="related-works"
            placeholder="Optional"
            class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full px-2 py-1"
          ></textarea>
        </div>
        <RadioGroup id="radio-visibility" v-model="visibility">
          <RadioGroupLabel class="min-w-max block font-medium text-gray-900"
            >Visibility
            <span class="text-gray-500 text-sm"
              >(Required)</span
            ></RadioGroupLabel
          >
          <div class="mt-2 grid grid-cols-2 border-2">
            <RadioGroupOption v-slot="{ checked }" value="public">
              <RadioGroupLabel
                :class="{ 'bg-blue-200': checked }"
                class="block border"
                as="span"
                >Public</RadioGroupLabel
              >
            </RadioGroupOption>
            <!-- <RadioGroupOption v-slot="{ checked }" value="shared">
              <RadioGroupLabel
                :class="{ 'bg-blue-200': checked }"
                class="block border"
                as="span"
                >Shared</RadioGroupLabel
              >
            </RadioGroupOption> -->
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
              id="menu-button-model"
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
          id="button-identify"
          @click="postImages"
          class="py-1 min-w-max p-1 rounded-full"
          :class="
            !uploadedImages ||
            !datasetName ||
            !visibility ||
            !selectedModel ||
            loading
              ? 'bg-gray-200'
              : 'bg-green-300 hover:bg-green-200'
          "
          :disabled="!uploadedImages || !selectedModel || loading"
        >
          <div v-if="loading" role="status" class="flex flex-row justify-center items-center">
            <svg
              aria-hidden="true"
              class="w-6 h-6 mr-2 text-gray-200 animate-spin dark:text-gray-600 fill-blue-600"
              viewBox="0 0 100 101"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z"
                fill="currentColor"
              />
              <path
                d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z"
                fill="currentFill"
              />
            </svg>
            <span class="text-xl font-bold">Submitting...</span>
          </div>
          <span v-else class="m-3 text-xl font-bold">Identify</span>
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
    <div id="image-gallery" class="basis-2/3 p-5">
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
    <Dialog as="div" @close="reset" class="relative z-10">
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

              <div class="mt-4 flex flex-row gap-2 justify-start">
                <button
                  type="button"
                  class="inline-flex justify-center rounded-md border border-transparent bg-blue-100 px-4 py-2 text-sm font-medium text-blue-900 hover:bg-blue-200 focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2"
                  @click="
                    () => {
                      router.push({ name: 'jobs' });
                    }
                  "
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
  <TransitionRoot appear :show="!store.isAuthenticated()" as="template">
    <Dialog
      as="div"
      @close="
        () => {
          router.push({ name: 'login' });
        }
      "
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
                Identification for registered users only!
              </DialogTitle>
              <div class="mt-2">
                <p class="text-sm text-gray-500">
                  Before you can upload images to identify, you must first log
                  in to your account. If you are not a registered user, you can
                  create an account today!
                </p>
              </div>

              <div class="mt-4 flex flex-row gap-2 justify-start">
                <button
                  type="button"
                  class="inline-flex justify-center rounded-md border border-transparent bg-blue-100 px-4 py-2 text-sm font-medium text-blue-900 hover:bg-blue-200 focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2"
                  @click="
                    () => {
                      router.push({ name: 'login' });
                    }
                  "
                >
                  Login
                </button>
                <button
                  type="button"
                  class="text-xs font-normal px-4 py-2 rounded-md hover:bg-slate-200 focus:outline-none focus-visible:ring-2 focus-visible:ring-slate-500 focus-visible:ring-offset-2"
                  @click="
                    () => {
                      router.push({ name: 'register' });
                    }
                  "
                >
                  Create account
                </button>
              </div>
            </DialogPanel>
          </TransitionChild>
        </div>
      </div>
    </Dialog>
  </TransitionRoot>
  <TransitionRoot appear :show="datasetHelp" as="template">
    <Dialog
      as="div"
      @close="
        () => {
          datasetHelp = false;
        }
      "
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
                Dataset Information Descriptions
              </DialogTitle>
              <div class="mt-2 text-sm text-gray-500 flex flex-col gap-2">
                <p>
                  Dataset Name: Unique name for the dataset. Using an existing
                  name will try to add the uploaded images to the dataset with
                  the existing name.
                </p>
                <p>Dataset Notes: Additional information for the dataset.</p>
                <p>
                  Dataset Geolocation: Any format of location. (Ex: Reno, NV;
                  Coordinates; etc.)
                </p>
                <p>
                  Publications: Indication of any sponsorships, collaborations,
                  organizations, etc.
                </p>
                <p>
                  Related Works: Citations or references to other works,
                  sources, etc.
                </p>
                <p>
                  Visibility: For <em>Public</em>, everyone can view this
                  dataset. For <em>Private</em>, only those with permission can
                  view this dataset.
                </p>
              </div>

              <div class="mt-4 flex flex-row gap-2 justify-start">
                <button
                  type="button"
                  class="inline-flex justify-center rounded-md border border-transparent bg-blue-100 px-4 py-2 text-sm font-medium text-blue-900 hover:bg-blue-200 focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2"
                  @click="
                    () => {
                      datasetHelp = false;
                    }
                  "
                >
                  Close
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
import {
  ChevronDownIcon,
  InformationCircleIcon,
} from "@heroicons/vue/20/solid";
import ImageCard from "../components/ImageCard.vue";
import FileList from "../components/FileList.vue";
import { authStore } from "../store/authenticate";
import { useRouter } from "vue-router";
import { ref } from "vue";

const uploadedImages = ref(false);
const selectedModel = ref("");
const models = ref([{ name: "YOLOv5" }]);
const files = ref({});
const FILETYPES = ref("image/jpeg"); //"image/png, image/jpeg"
const datasetHelp = ref(false);
const datasetName = ref("");
const datasetNotes = ref("");
const datasetGeoloc = ref("");
const visibility = ref("");
const successfulSubmit = ref(false);
const errorMsg = ref("");
const loading = ref(false);
const publications = ref("");
const relatedWorks = ref("");

const store = authStore();
const router = useRouter();

var id = 0;

function setModel(model) {
  selectedModel.value = model.name;
}

function uploadImages(event) {
  if (event.target.files.length != 0) {
    uploadedImages.value = true;
    for (let file of event.target.files) {
      files.value[id] = {
        name: file.name,
        path: URL.createObjectURL(file),
        object: file,
      };
      id++;
    }
    // console.log("after upload:", this.files);
    modifyFileList();
  }
}

function dropImages(event) {
  event.preventDefault();
  if (event.dataTransfer.items) {
    [...event.dataTransfer.items].forEach((item, i) => {
      if (item.kind === "file") {
        const file = item.getAsFile();
        if (FILETYPES.value.includes(file.type)) {
          files.value[id] = {
            name: file.name,
            path: URL.createObjectURL(file),
            object: file,
          };
          id++;
        } else
          console.log(`File ${file.name} is not of type "${this.FILETYPES}"`);
      }
    });
    uploadedImages.value = true;
  }
  // console.log("after upload:", this.files);
  modifyFileList();
}

function deleteFile(fileId) {
  delete files.value[fileId];
  if (Object.keys(files.value).length == 0) uploadedImages.value = false;
  // console.log("after delete:", this.files);
  modifyFileList();
}

function modifyFileList() {
  const imageInput = document.getElementById("image-input");
  var newFileList = new DataTransfer();
  for (const fileId in files.value) {
    newFileList.items.add(files.value[fileId].object);
  }
  imageInput.files = newFileList.files;
}

async function postImages() {
  loading.value = true;
  const url = "http://127.0.0.1:5001/identify";
  const imageInput = document.getElementById("image-input");
  const form = new FormData();
  for (const image of imageInput.files) {
    form.append("images", image);
  }
  form.set("dataset-name", datasetName.value);
  form.set("dataset-notes", datasetNotes.value);
  form.set("dataset-geoloc", datasetGeoloc.value);
  form.set("visibility", visibility.value);
  form.set("timestamp", Date.now());
  const userData = await store.userData();
  console.log("user data", userData);
  form.set("user-id", userData.id);
  fetch(url, {
    method: "POST",
    mode: "no-cors",
    body: form,
  })
    .then((res) => {
      // console.log(res)
      // console.log("successfully posted images");
      errorMsg.value = "";
      successfulSubmit.value = true;
    })
    .catch((err) => {
      console.log(err);
      errorMsg.value = "An error occured when submitting. Try again.";
    })
    .finally(() => {
      loading.value = false;
    });
}

function reset() {
  uploadedImages.value = false;
  selectedModel.value = "";
  files.value = {};
  modifyFileList();
  datasetName.value = "";
  datasetNotes.value = "";
  datasetGeoloc.value = "";
  visibility.value = "";
  successfulSubmit.value = false;
  errorMsg.value = "";
}
</script>

<!-- <script>
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
import { authStore } from "../store/authenticate";
import { useRouter } from "vue-router";

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
      models: [{ name: "YOLOv5" }],
      files: {}, // { id: { name, path, object } }
      FILETYPES: "image/jpeg",//"image/png, image/jpeg",
      datasetName: "",
      datasetNotes: "",
      datasetGeoloc: "",
      visibility: "",
      successfulSubmit: false,
      errorMsg: "",
      loading: false,
      store: authStore(),
      router: useRouter(),
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
    async postImages() {
      this.loading = true;
      const url = "http://127.0.0.1:5001/identify";
      const imageInput = document.getElementById("image-input");
      const form = new FormData();
      for (const image of imageInput.files) {
        form.append("images", image);
      }
      form.set("dataset-name", this.datasetName);
      form.set("dataset-notes", this.datasetNotes);
      form.set("dataset-geoloc", this.datasetGeoloc);
      form.set("visibility", this.visibility);
      const userData = await this.store.userData();
      console.log("user data", userData)
      form.set("user-id", userData.id);
      fetch(url, {
        method: "POST",
        mode: "no-cors",
        body: form,
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
        })
        .finally(() => {
          this.loading = false;
        });
    },
    reset() {
      this.uploadedImages = false;
      this.selectedModel = "";
      this.files = {};
      this.modifyFileList();
      this.datasetName = "";
      this.datasetNotes = "";
      this.datasetGeoloc = "";
      this.visibility = "";
      this.successfulSubmit = false;
      this.errorMsg = "";
    },
  },
};
</script> -->
