<!-- Author: Antonio Lang, style by Carl Antiado -->

<template>
  <div class="flex flex-col justify-start items-center gap-2 bg-slate-100 border border-slate-200 p-2">
    <!-- <span class="text-lg"><b>Dataset:</b> {{ datasetName }}</span> -->
    <span class="text-lg"><b>Dataset:</b> {{ datasetName }} <b>| Upload ID:</b> {{ uploadID }}</span>
    <span>No. of Images: {{ numUploaded }}</span>
    <div class="flex flex-row justify-center flex-wrap gap-3">
      <div v-for="(imgURL, index) in imgURLs">
        <img
          class="object-cover h-48 w-48 p-1 bg-white border rounded max-w-sm"
          :src="imgURL"
        />
        <div v-if="labels[index]">
          {{ labels[index] }}
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    datasetName: String,
    imgURLs: Array,
    numUploaded: Number,
    uploadID: String,
    labels: Array,
  },
  setup() {
    let name = "UserImg";
    return { name };
  },
  data() {
    return {
      verified_image: false,
      imageData: this.imgURL,
    };
  },
};
</script>

<style></style>
