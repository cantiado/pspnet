<!-- Author: Antonio Lang -->

<template>
    <div class="flex flex-wrap justify-center">
        <img class="object-cover h-48 w-48 p-1 bg-white border rounded max-w-sm" :src="require(`../assets/${src_path}`)">
    </div>
    <div>
        <span>"Un/verified"</span>
    </div>
</template>

<script>
export default {
    props: ['src_path'],
    setup() {
        let name = 'UserImg'
        return {name}
    },
    data() {
        return {
            verified_image: false
        }
    }
}
</script>

<style>

</style>