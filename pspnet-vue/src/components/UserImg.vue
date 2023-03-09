<!-- Author: Antonio Lang -->

<template>
    <div class="rectangle grid">
        <div v-for="imgURL in imgURLs">
            <img class="object-cover h-48 w-48 p-1 bg-white border rounded max-w-sm" :src="imgURL">
        </div>
        <div class="details w-48">
            <div>Upload ID: {{ uploadID }}</div>
            <div># Images: {{ numUploaded }}</div>
        </div>
    </div>
</template>

<script>
export default {
    props: {
        imgURLs: Array,
        numUploaded: Number,
        uploadID: Number,
        required: true
    },
    setup() {
        let name = 'UserImg'
        return {name}
    },
    data() {
        return {
            verified_image: false,
            imageData: this.imgURL
        }
    }
}
</script>

<style>

</style>