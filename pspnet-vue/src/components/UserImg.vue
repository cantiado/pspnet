<!-- Author: Antonio Lang -->

<template>
    <div class="flex flex-wrap justify-center">
        <img class="object-cover h-48 w-48 p-1 bg-white border rounded max-w-sm" :src="imageData">
    </div>
    <!-- <div>
        <span>{{ label }}</span>
    </div> -->
</template>

<script>
export default {
    props: {
        imgURL: String,
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