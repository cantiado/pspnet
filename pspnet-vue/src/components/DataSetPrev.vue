<!-- Author: Antonio Lang -->

<template>
    <div class="rectangle">
    <!-- <div class="inline-flex bg-green border rounded m-4"> -->
        <div class="inline-flex p-1 gap-1">
            <UserImg src_path="user_images/sage.jpg"/>
            <UserImg src_path="user_images/sage.jpg"/>
            <UserImg src_path="user_images/sage.jpg"/>
        </div>
        <div class="p-4">
            <div>No. Images: </div>
            <div>Project: </div>
        </div>
    </div>
</template>

<script>
import UserImg from './UserImg.vue'
export default {
    name : 'DataSetPrev',
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