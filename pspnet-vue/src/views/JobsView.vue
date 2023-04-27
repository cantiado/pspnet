<template>
  <div class="w-full flex flex-col justify-start items-center gap-3 p-5">
    <!-- delete this once jobs are implemented -->

    <!--  -->
    <h1 class="text-2xl font-bold">Current Jobs</h1>
    <div class="max-w-750 w-3/4 border" id="currentJobsTable">
      <div class="grid grid-cols-3 border-2 p-2">
        <span class="font-bold">Job ID</span>
        <span class="font-bold">Dataset Name</span>
        <span class="font-bold">Position in Queue</span>
      </div>
      <div v-for="job in currentJobs" class="border" :key="job.id">
        <button
          @click="
            selectedCurrentJob != job.id
              ? setCurrentJob(job.id)
              : setCurrentJob(-1)
          "
          class="grid grid-cols-3 w-full hover:bg-green-200 items-center"
          :class="selectedCurrentJob == job.id ? 'bg-slate-200' : 'bg-white'"
        >
          <span>{{ job.id }}</span>
          <span>{{ job.datasetName }}</span>
          <span>{{ job.eta }}</span>
        </button>
        <div
          class="flex flex-row justify-start gap-5"
          :class="{ hidden: selectedCurrentJob != job.id }"
        >
          <div class="p-3 gap-2 border-t flex flex-col items-start bg-slate-50">
            <span>Sumbitted: {{ job.start }}</span>
            <div class="flex flex-row gap-5">
              <span>Images: {{ job.numImages }}</span>
              <span>Model: {{ job.model }}</span>
              <span>Visibility: {{ job.visibility }}</span>
              <span
                >Geolocation:
                {{ job.datasetGeoloc ? job.datasetGeoloc : "None" }}</span
              >
            </div>
            <p class="text-justify">
              Additional Notes:
              {{ job.datasetNotes ? job.datasetNotes : "None" }}
            </p>
          </div>
        </div>
      </div>
    </div>
    <h1 class="text-2xl font-bold">Completed Jobs</h1>
    <div class="max-w-750 w-3/4 border" id="currentJobsTable">
      <div class="grid grid-cols-3 border-2 p-2">
        <span class="font-bold">Job ID</span>
        <span class="font-bold">Dataset Name</span>
        <span class="font-bold">Finished</span>
      </div>
      <div v-for="job in completedJobs" class="border" :key="job.id">
        <button
          @click="
            selectedCompletedJob != job.id
              ? setCompletedJob(job.id)
              : setCompletedJob(-1)
          "
          class="grid grid-cols-3 w-full hover:bg-green-200 items-center"
          :class="selectedCompletedJob == job.id ? 'bg-slate-200' : 'bg-white'"
        >
          <span>{{ job.id }}</span>
          <span>{{ job.datasetName }}</span>
          <span>{{ job.end }}</span>
        </button>
        <div
          :class="{ hidden: selectedCompletedJob != job.id }"
          class="p-3 gap-2 border-t flex flex-col items-start bg-slate-50"
        >
          <span>Submitted: {{ job.start }}</span>
          <span>Duration: {{ job.duration }} sec</span>
          <div class="flex flex-row gap-5">
            <span>Images: {{ job.numImages }}</span>
            <span>Model: {{ job.model }}</span>
            <span>Visibility: {{ job.visibility }}</span>
            <span
              >Geolocation:
              {{ job.datasetGeoloc ? job.datasetGeoloc : "None" }}</span
            >
          </div>
          <p class="text-justify">
            Additional Notes: {{ job.datasetNotes ? job.datasetNotes : "None" }}
          </p>
          <div class="flex-row space-x-4">
            <a :href="'http://127.0.0.1:5000/download/' + job.id">
              <button class="px-3 py-1 border bg-green-200 my-5">
                Download CSV
              </button>
            </a>
            <router-link
              :to="{
                name: 'singleDataset',
                params: { dsName: job.datasetName },
                props: true,
              }"
            >
              <button class="px-3 py-1 border bg-green-200 my-5">
                View Dataset
              </button>
            </router-link>
          </div>
        </div>
        <!-- <a
          :href="'http://127.0.0.1:5000/download/' + job.id"
          class="border bg-green-200 my-5">
          Download csv</a> -->
      </div>
    </div>
  </div>
</template>

<script setup>
import { authStore } from "../store/authenticate";
import { useRouter } from "vue-router";
import { ref, onMounted, onBeforeMount, onBeforeUnmount } from "vue";
import { getCurrentJobs } from "@/api";
import { getFinishedJobs } from "@/api";

const currentJobs = ref([]);

const completedJobs = ref([]);

const selectedCurrentJob = ref(-1);
const selectedCompletedJob = ref(-1);

const store = authStore();

const getJobs = async () => {
  try {
    const currentJobRes = await getCurrentJobs(
      localStorage.getItem("userToken")
    );
    currentJobs.value = currentJobRes.data;
    const finishedJobRes = await getFinishedJobs(
      localStorage.getItem("userToken")
    );
    completedJobs.value = finishedJobRes.data;
    for (const job of completedJobs.value) {
      const endTime = new Date(job.end + " UTC");
      job.end = `${endTime.getFullYear()}-${String(endTime.getMonth()).padStart(
        2,
        "0"
      )}-${endTime.getDate()} \
      ${String(endTime.getHours()).padStart(2, "0")}:${String(
        endTime.getMinutes()
      ).padStart(2, "0")}`;

      const startTime = new Date(job.start + " UTC");
      job.start = `${startTime.getFullYear()}-${String(
        startTime.getMonth()
      ).padStart(2, "0")}-${startTime.getDate()} \
      ${String(startTime.getHours()).padStart(2, "0")}:${String(
        startTime.getMinutes()
      ).padStart(2, "0")}`;

      job.duration = Math.round(
        (endTime.getTime() - startTime.getTime()) / 1000
      );
    }
  } catch (err) {
    console.log(err);
  }
};

//setInterval is not advised, can be bad if getJobstakes longer than the interval
const interval_id = setInterval(getJobs, 2000);

onBeforeUnmount(() => {
  clearInterval(interval_id);
});

function setCurrentJob(id) {
  selectedCurrentJob.value = id;
}
function setCompletedJob(id) {
  selectedCompletedJob.value = id;
}

onBeforeMount(() => {
  if (!store.isAuthenticated()) {
    const router = useRouter();
    router.push({ name: "login" });
  }
});

onMounted(() => {
  currentJobs.value.sort((jobA, jobB) => {
    if (jobA.start < jobB.start) return -1;
    if (jobA.start > jobB.start) return 1;
    return 0;
  });
  completedJobs.value.sort((jobA, jobB) => {
    if (jobA.end < jobB.end) return 1;
    if (jobA.end > jobB.end) return -1;
    return 0;
  });
});
</script>

<!-- <script>
import { authStore } from "../store/authenticate";
import { useRouter } from "vue-router";
export default {
  data() {
    return {
      currentJobs: [
        {
          id: 6,
          datasetName: "my-dataset",
          datasetNotes: "this dataset is to demo",
          datasetGeoloc: "",
          visibility: "public",
          model: "Model 1",
          numImages: 25,
          start: new Date("February 23, 2023 11:00:00"),
          eta: "00hr 00min 15sec",
        },
        {
          id: 7,
          datasetName: "my-latest-dataset",
          datasetNotes:
            "this dataset is newer and better. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec sit amet neque ac purus mollis porttitor. Vestibulum massa ligula, tincidunt at velit id, pulvinar luctus dui. Phasellus rutrum, ipsum nec vestibulum posuere, risus massa elementum quam, eget maximus est tortor nec diam. Suspendisse faucibus nulla felis. Nullam pellentesque felis turpis, ut consectetur dui pharetra vitae. Maecenas non dolor sit amet nisi tempus rutrum. Curabitur pulvinar quis mauris non egestas. Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
          datasetGeoloc: "",
          visibility: "public",
          model: "Model 1",
          numImages: 35,
          start: new Date("February 23, 2023 11:15:00"),
          eta: "00hr 05min 00sec",
        },
      ],
      completedJobs: [
        {
          id: 1,
          datasetName: "my-first-dataset",
          datasetNotes: "gotta start somewhere",
          datasetGeoloc: "",
          visibility: "public",
          model: "Model 1",
          numImages: 5,
          start: new Date("February 16, 2023 9:00:00"),
          end: new Date("February 16, 2023 9:01:00"),
        },
        {
          id: 2,
          datasetName: "my-second-dataset",
          datasetNotes: "",
          datasetGeoloc: "",
          visibility: "public",
          model: "Model 1",
          numImages: 15,
          start: new Date("February 17, 2023 9:00:00"),
          end: new Date("February 17, 2023 9:01:00"),
        },
        {
          id: 3,
          datasetName: "my-third-dataset",
          datasetNotes: "my first private dataset",
          datasetGeoloc: "",
          visibility: "private",
          model: "Model 1",
          numImages: 22,
          start: new Date("February 18, 2023 9:00:00"),
          end: new Date("February 18, 2023 9:01:00"),
        },
        {
          id: 4,
          datasetName: "my-fourth-dataset",
          datasetNotes: "my first shared dataset",
          datasetGeoloc: "",
          visibility: "shared",
          model: "Model 1",
          numImages: 8,
          start: new Date("February 19, 2023 9:00:00"),
          end: new Date("February 19, 2023 9:01:00"),
        },
        {
          id: 5,
          datasetName: "my-fifth-dataset",
          datasetNotes: "i ran out of thoughts to write about",
          datasetGeoloc: "",
          visibility: "public",
          model: "Model 1",
          numImages: 14,
          start: new Date("February 20, 2023 9:00:00"),
          end: new Date("February 20, 2023 9:01:00"),
        },
      ],
      selectedCurrentJob: -1,
      selectedCompletedJob: -1,
    };
  },
  beforeMount() {
    const store = authStore();
    if (!store.isAuthenticated()) {
      const router = useRouter();
      router.push({ name: "login" });
    }
  },
  mounted() {
    this.currentJobs.sort((jobA, jobB) => {
      if (jobA.start < jobB.start) return -1;
      if (jobA.start > jobB.start) return 1;
      return 0;
    });
    this.completedJobs.sort((jobA, jobB) => {
      if (jobA.end < jobB.end) return 1;
      if (jobA.end > jobB.end) return -1;
      return 0;
    });
  },
  methods: {
    setCurrentJob(id) {
      this.selectedCurrentJob = id;
    },
    setCompletedJob(id) {
      this.selectedCompletedJob = id;
    },
  },
};
</script> -->
