<!-- Author: Antonio Lang -->

<template>
    <div class="rectangle">
    <!-- <div class="inline-flex bg-green border rounded m-4"> -->
        <div v-for="imagePath in img_paths" class="inline-flex p-1 gap-1">
            <!-- <div>{{ imagePath }}</div> -->
            <UserImg :src_path="imagePath"/>
        </div>
        <div class="p-4">
            <div># Images: {{ ds_count }}</div>
            <div>Project: {{ ds_name }}</div>
        </div>
    </div>
</template>

<script>
import UserImg from './UserImg.vue'
import axios from 'axios';

export default {
    name : 'DataSetPrev',
    props: {
        ds_name: String,
        ds_count: Number,
        required: true
    },
    data() {
        return {
            img_paths: null,
            images: [{path: "user_images/sage.jpg"}, {path: "user_images/rabbit.jpg"}]
        }
    },
    mounted() {
        axios
        .get('http://127.0.0.1:5000/datasets/', this.ds_name)
        .then(response => (
            this.img_paths = response.data,
            console.log(this.img_paths),
            console.log(response)
            ))
        .catch(this.error = "Failed to retreive data")
    },
    components: {UserImg}
}
</script>

<style>
    .rectangle {
        border-radius: 10px;
        border-width: 1px;
        border-color: #b9e0a5;
        width:100%;
        display: flex;
        margin:4;
    }
</style>