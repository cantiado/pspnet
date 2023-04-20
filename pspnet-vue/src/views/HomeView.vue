<template>
  <div class="w-full h-full hero-img">
    <div
      class="w-full h-full p-5 backdrop-blur-md flex flex-col gap-10 items-center justify-start"
    >
      <h1
        class="w-fit py-5 text-slate-100 text-6xl font-semibold drop-shadow-lg"
      >
        Plant and Soil Property Network
      </h1>
      <div class="flex flex-row justify-center items-stretch gap-16">
        <div
          id="home-about-card"
          @click="redirect('/about')"
          class="w-1/4 p-5 bg-slate-100 rounded-lg border-2 border-slate-200 drop-shadow-lg cursor-pointer hover:bg-slate-200"
        >
          <h2 class="text-2xl mb-3">About</h2>
          <p>Learn more about the project</p>
        </div>
        <div
          id="home-explore-card"
          @click="redirect('/explore')"
          class="w-1/4 p-5 bg-slate-100 rounded-lg border-2 border-slate-200 drop-shadow-lg cursor-pointer hover:bg-slate-200"
        >
          <h2 class="text-2xl mb-3">Explore</h2>
          <p>Check out user-contributed datasets</p>
        </div>
        <div
          id="home-identify-card"
          @click="redirect('/identify')"
          class="w-1/4 p-5 bg-slate-100 rounded-lg border-2 border-slate-200 drop-shadow-lg cursor-pointer hover:bg-slate-200"
        >
          <h2 class="text-2xl mb-3">Identify</h2>
          <p>Upload images to identify and contibute</p>
        </div>
      </div>
    </div>
    <!-- <img class="w-full" src="../assets/plant_soil_(Shutterstock).jpg" /> -->
  </div>
  <!-- <link
      href="https://unpkg.com/material-components-web@latest/dist/material-components-web.min.css"
      rel="stylesheet"
    />
    <link
      rel="stylesheet"
      href="https://fonts.googleapis.com/icon?family=Material+Icons"
    />
  <main>
    <div class="mdc-layout-grid">
      <div class="mdc-layout-grid__inner">
        <div class="mdc-layout-grid__cell--span-12">
          <section class="font-medium text-4xl mt-0 mb-2 text-black-600">
            <h1>Plant and Soil Property Classification Network</h1>
          </section>
        </div>
        <div class="mdc-layout-grid__cell--span-3">
          <div class="mdc-card container">
            <h2 class="text-xl">About</h2>
            <p>
              Learn more about the project and its mission here!
            </p>
          </div>
        </div>
        <div class="mdc-layout-grid__cell--span-3">
          <div class="mdc-card container">
            <h2 class="text-xl">Dataset</h2>
            <p>
              Curious about our dataset? Read more on the About page!
            </p>
          </div>
        </div>
        <div class="mdc-layout-grid__cell--span-3">
          <div class="mdc-card container">
            <h2 class="text-xl">Identify</h2>
            <p>
              Have an image you want to be classified? Try it against our models here.
            </p>
          </div>
        </div>
        <div class="mdc-layout-grid__cell--span-3">
          <div class="mdc-card container">
            <h2 class="text-xl">Contributions</h2>
            <p>
              Explore public contributions to the dataset from citizen scientists all around the world!
            </p>
          </div>
        </div>
      </div>
    </div>
  </main> -->
  <!-- add Vue footer -->
</template>

<script setup>
import { useRouter } from "vue-router";

const router = useRouter();

function redirect(path) {
  router.push(path);
}
</script>

<!-- <script>
import { useRouter } from 'vue-router';

export default {
  name: 'HomeView',
  setup() {
    const router = useRouter();
    const redirect = function(path) {
      router.push(path);
    }
    return {redirect}
  }
}
</script> -->

<style>
.hero-img {
  background-image: url("../assets/plant_soil_(Shutterstock).jpg");
  background-size: cover;
  background-repeat: no-repeat;
  background-position-y: 75%;
  background-position-x: center;
}
</style>
