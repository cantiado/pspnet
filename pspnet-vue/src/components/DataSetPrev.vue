<!-- Author: Antonio Lang -->

<template>
    <div class="rectangle">
        <div v-if="img_paths" v-for="index in 4" :key="index" class="imgContainer">
            <div class="imgHolder">
                <img class="object-cover h-48 w-48 p-1 bg-white border rounded max-w-sm" :src="require(`../assets/${img_paths[index-1]}`)">
            </div>
        </div>
        <div class="details w-48">
            <div> Name: {{ ds_name }}</div>
            <div> # Images: {{ ds_count }}</div>
        </div>
    </div>
</template>

<script>
import UserImg from './UserImg.vue'
import axios from 'axios';
import { onMounted } from 'vue';
import { ref } from 'vue';

export default {
    name : 'DataSetPrev',
    props: {
            ds_name: String,
            ds_count: Number,
            required: true
    },
    setup(props) {
        const img_paths = ref('')
        const ds_name = ref(props.ds_name)
        const ds_count = ref(props.ds_count)
        const error = ref('')
        
        onMounted(async () => {
            await ds_name.value
            if (ds_name) {
                await axios.post('http://127.0.0.1:5000/datasets/',
                {ds_name: ds_name.value}
                )
                .then(response => (
                    img_paths.value = response.data))
                .catch(error.value = "Failed to retreive data")
            }
        })

        return { ds_name, ds_count, img_paths }
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