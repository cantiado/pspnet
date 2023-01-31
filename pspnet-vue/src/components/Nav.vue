<template>
  <div class="grid">
    <div class="justify-start flex-grow-1">
      <nav class="bg-green-200 text-left flex justify-start">
        <slot></slot>
      </nav>
    </div>
  </div>
  
</template>

<script>
export default {
  setup(){
    let name = 'Nav'
    return {name}
  }
}
</script>

<style>
  /* .grid {
    display: grid;
    position: sticky;
    left: 0;
    top: 0;
    width: -webkit-fill-available;
    height: auto;
  }
  .bg-green-200 {
    background: #b9e0a5;
  } */
</style>