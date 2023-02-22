<!-- Button adapted from https://headlessui.com/vue/menu-->
<template>
  <Menu>

    <MenuButton class="profileIcon">
      <img class="w-8 h-8 rounded-full" src="@/assets/login_image.jpg" alt="user photo">
    </MenuButton>

    <transition
        enter-active-class="transition duration-100 ease-out"
        enter-from-class="transform scale-95 opacity-0"
        enter-to-class="transform scale-100 opacity-100"
        leave-active-class="transition duration-75 ease-in"
        leave-from-class="transform scale-100 opacity-100"
        leave-to-class="transform scale-95 opacity-0"
    >
      <MenuItems class="dropdown">

        <MenuItem v-for="routeName in routeNames" :key="routeName">
          <button class="group flex w-full items-center justify-center rounded-md px-2 py-2 text-sm hover:bg-gray-100" @click="goRoute(routeName)">{{routeName}}</button>
        </MenuItem>

        <MenuItem>
          <button class="group flex w-full items-center justify-center rounded-md px-2 py-2 text-sm hover:bg-gray-100" @click="handleLogout" >Logout</button>
        </MenuItem>

      </MenuItems>
    </transition>
  </Menu>
</template>

<script>
import { Menu, MenuButton, MenuItems, MenuItem } from '@headlessui/vue'
import { useRouter } from 'vue-router'
export default {
  name: 'ProfileIcon',
  components: {
    Menu,
    MenuButton,
    MenuItems,
    MenuItem
  },
  setup(){
    const routeNames = [
      'Settings',
      'Profile'
    ]

    const router = useRouter()
    const goRoute = (routeName) => {
      router.push({name : routeName.toLowerCase()})
    }
    const handleLogout = () => {
      localStorage.removeItem('userToken')
      router.go()
    }

    return { routeNames, goRoute, handleLogout}
  }
}
</script>

<style lang="postcss" scoped>

.profileIcon {
  @apply flex mr-3 text-sm bg-gray-300 rounded-full md:mr-0 focus:ring-4 focus:ring-gray-300
}

.dropdown {
  @apply absolute top-14 mt-2 w-32  divide-y divide-gray-100 rounded-md bg-white shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none
}

</style>