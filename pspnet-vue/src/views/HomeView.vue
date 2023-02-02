<template>
  <link
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
  </main>
  <!-- add Vue footer -->
</template>

<script>
// @ is an alias to /src

export default {
  name: 'HomeView',
  components: {
  }
}
</script>

<style>
  .mdc-card-container {
    width: 150px;
    height: 100px;
  }
  .mdc-card {
    /* height:120px; */
    padding: 10px;
  }
</style>