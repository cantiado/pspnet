<template>
  <div class="flex flex-col h-screen">
    <Nav>
      <router-link class = "mx-2 col-span-1" :to="{name: 'home'}">Home</router-link> 
      <router-link class = "mx-2 col-span-2" :to="{name: 'about'}">About</router-link> 
      <router-link class = "mx-2 col-span-3" :to="{name: 'login'}">Login</router-link>
    </Nav>
    <div class="flex flex-grow">
      <router-view/>
    </div>
  </div>
</template>

<script>
import Nav from "./components/Nav.vue"

export default {
  components: {Nav}
}
</script>


<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

nav {
  padding: 30px;
}

nav a {
  font-weight: bold;
  color: #2c3e50;
}

nav a.router-link-exact-active {
  color: #42b983;
}
</style>
