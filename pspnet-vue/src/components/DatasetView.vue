<template>
    <div class="background" @click="closeView">
        <div class="window">
            <div class="dsName text-2xl font-bold">{{ ds_name }}</div>
            <div class="imgContainer inline-grid grid-cols-3 gap-3">
                <div v-if="img_paths" v-for="path in img_paths" class="individualImg">
                        <img class="object-cover h-48 w-48 p-1 bg-white border rounded max-w-sm" 
                        :src="require(`../assets/${path}`)">
            </div>
        </div>
        </div>
    </div>


</template>

<script>
import axios from 'axios';
import { ref } from 'vue';
import UserImg from './UserImg.vue';
import { onMounted } from 'vue';

export default {

    props: {
        ds_name: String
    },
    setup(props, {emit}) {
        const img_paths = ref([])
        const ds_name = ref(props.ds_name)
        const error = ref('')
        onMounted(async () => {
            if (ds_name.value) {
                await axios.post('http://127.0.0.1:5000/datasetview/',
                {ds_name: ds_name.value}
                )
                .then(response => (
                    img_paths.value = response.data))
                .catch(error.value = "Failed to retreive data")
            }
        })

        const closeView = () => {
            emit("closeModal", true)
        }

        return {img_paths, closeView, emit}
    },
    components: {UserImg}
}
</script>

<style>
.background {
    background: rgba(0,0,0,0.25);
    top: 0;
    left: 0;
    position: fixed;
    width: 100%;
    height: 100%;
}
.window {
    background: white;
    position:relative;
    margin: 125px auto;
    border-width: 5px;
    border-radius: 5px;
    width: 60%;
    height: 60%;
    overflow-y: auto;
    padding: 15px;
}
.imgContainer {
    display: grid;
}
.individualImg {
    width: auto;
    position:relative;
}
.dsName {
    margin-bottom: 15px;
}
</style>