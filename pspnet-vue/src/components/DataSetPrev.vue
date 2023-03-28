<!-- Author: Antonio Lang -->

<template>
  <div
    class="p-3 flex flex-row gap-3 border-[#b9e0a5] border-4 rounded-md justify-start"
  >
    <div class="flex flex-row gap-2">
      <div v-if="img_paths" v-for="imgPath in img_paths" class="imgContainer">
        <div class="imgHolder">
          <img
            class="object-cover h-48 w-48 p-1 bg-white border rounded max-w-sm"
            :src="imgPath"
          />
        </div>
      </div>
    </div>
    <div class="w-full flex flex-col gap-2 justify-start items-start text-ellipsis overflow-hidden ...">
      <span class="text-xl"><b>Name:</b> {{ ds_name }}</span>
      <span># Images: {{ ds_count }}</span>
      <span v-if="location">Location: {{ location }}</span>
      <p class="text-sm italic text-justify">{{ description }}</p>
    </div>
  </div>
</template>

<script>
import UserImg from "./UserImg.vue";
import { ref } from "vue";

export default {
  name: "DataSetPrev",
  props: {
    ds_name: String,
    ds_count: Number,
    img_paths: Array,
    location: String,
    description: String,
    required: true,
  },
  setup(props) {
    const img_paths = ref(props.img_paths);
    const ds_name = ref(props.ds_name);
    const ds_count = ref(props.ds_count);
    const location = ref(props.location);
    const description = ref(props.description);
    const error = ref("");

    return { ds_name, ds_count, img_paths, location, description };
  },
  components: { UserImg },
};
</script>

<style>
/* .rectangle {
  border-radius: 10px;
  border-width: 3px;
  border-color: #b9e0a5;
  width: 100%;
  display: flex;
  margin: 4px;
  padding: 4px;
}
.rectangle .imgContainer {
  display: flex;
  flex-wrap: wrap;
}
.rectangle .imgContainer .object-cover {
  width: 100%;
  height: 100%;
}
.rectangle .imgHolder {
  width: 150px;
  height: 150px;
}
.details {
  align-items: center;
  padding: 7px;
  height: 150px;
  overflow-y: scroll;
} */
</style>
