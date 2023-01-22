<!-- Author: Antonio Lang -->

<template>
    <div>
        <h1>"First Name" "Last Name"</h1>
        <p>Created account on MM/DD/YYYY</p>
        <p>Verified Labeler: "Yes/No"</p>
        <p>No. of Contributions: "#""</p>
    </div>
    <div class="user-bio">
        <p>This information will be referenced from the user database.</p>
    </div>
    <div class="user-image-gallery">
        <h2>Images Contributed</h2>
            <p>These contributions will be referenced from the image database.</p>
            <ul class="mdc-image-list my-image-list">
                <li class="mdc-image-list__item">
                  <div class="mdc-image-list__image-aspect-container">
                    <img class="mdc-image-list__image" src="../assets/sage.jpg">
                  </div>
                  <div class="mdc-image-list__supporting">
                    <span class="mdc-image-list__label">"Un/verified"</span>
                  </div>
                </li>
                <li class="mdc-image-list__item">
                    <div class="mdc-image-list__image-aspect-container">
                      <img class="mdc-image-list__image" src="../assets/sage.jpg">
                    </div>
                    <div class="mdc-image-list__supporting">
                      <span class="mdc-image-list__label">"Un/verified"</span>
                    </div>
                  </li>
              </ul>
    </div>
    <!-- Reference user's name, account creation data, verifier, bio from database -->
    <!-- count number of contributions from image database -->
    <!-- Display images from the image database with label -->
</template>

<script>

</script>

<style>

</style>