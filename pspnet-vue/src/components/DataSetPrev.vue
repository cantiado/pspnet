<!-- Author: Antonio Lang -->

<template>
    <div class="rectangle">
        <div v-if="img_paths" v-for="imgPath in img_paths" class="imgContainer">
            <div class="imgHolder">
                <img class="object-cover h-48 w-48 p-1 bg-white border rounded max-w-sm" :src="imgPath">
            </div>
        </div>
        <div class="details w-48">
            <div>Name: {{ ds_name }}</div>
            <div># Images: {{ ds_count }}</div>
            <div v-if="location">Location: {{ location }}</div>
            <div>{{ description }}</div>
        </div>
    </div>
</template>

<script>
import UserImg from './UserImg.vue'
import { ref } from 'vue';

export default {
    name : 'DataSetPrev',
    props: {
            ds_name: String,
            ds_count: Number,
            img_paths: Array,
            location: String,
            description: String,
            required: true
    },
    setup(props) {
        const img_paths = ref(props.img_paths)
        const ds_name = ref(props.ds_name)
        const ds_count = ref(props.ds_count)
        const location = ref(props.location)
        const description = ref(props.description)
        const error = ref('')

        return { ds_name, ds_count, img_paths, location, description }
    },
    components: {UserImg}
}
</script>

<style>
    .rectangle {
        border-radius: 10px;
        border-width: 3px;
        border-color: #b9e0a5;
        width:100%;
        display: flex;
        margin:4;
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
       margin-top: 15px;
    }
</style>