<!-- Button adapted from https://flowbite.com/docs/components/navbar/ -->
<template>
  <button type="button" class="profileIcon" >
    <span class="sr-only">Open user menu</span>
      <img class="w-8 h-8 rounded-full" src="@/assets/login_image.jpg" alt="user photo">
  </button>
  <div class="z-50 py-1 rounded-md shadow-xs">
    <a
      href="#"
      class="block px-4 py-2 text-sm leading-5 text-gray-700 transition duration-150 ease-in-out hover:bg-gray-100 focus:outline-none focus:bg-gray-100"
      role="menuitem"
    >
      Your Profile
    </a>
    <a
      href="#"
      class="block px-4 py-2 text-sm leading-5 text-gray-700 transition duration-150 ease-in-out hover:bg-gray-100 focus:outline-none focus:bg-gray-100"
      role="menuitem"
    >
      Settings
    </a>
    <a
      href="#"
      class="block px-4 py-2 text-sm leading-5 text-gray-700 transition duration-150 ease-in-out hover:bg-gray-100 focus:outline-none focus:bg-gray-100"
      role="menuitem"
    >
      Sign out
    </a>
  </div>

  
</template>

<script>
export default {
  name: 'ProfileIcon'
}
</script>

<style lang="postcss" scoped>

.profileIcon {
  @apply flex mr-3 text-sm bg-gray-300 rounded-full md:mr-0 focus:ring-4 focus:ring-gray-300
}

</style>