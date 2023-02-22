<!-- Author: Antonio Lang -->
<!-- Dropdown filter menu adapted from vue headless ui and tailwind-->

<template>
    <div class="p-10">
        <div class="grid gap-4">
            <div class="flex-row">
                <!-- following div component from tailwind elements -->
                <div class="flex justify-center">
                    <div class="mb-3 xl:w-96">
                        <input
                        type="search"
                        class="
                            form-control
                            block
                            w-full
                            px-3
                            py-1.5
                            text-base
                            font-normal
                            text-gray-700
                            bg-white bg-clip-padding
                            border border-solid border-gray-300
                            rounded
                            transition
                            ease-in-out
                            m-0
                            focus:text-gray-700 focus:bg-white focus:border-blue-600 focus:outline-none
                        "
                        id="searchBar"
                        placeholder="Dataset name"
                        />
                    </div>
                </div>
                <!-- following div component from tailwind elements -->
                <Menu as="div" class="dropdown">
                    <MenuButton as="div" class="dropdown-toggle
                        px-6
                        py-2.5
                        bg-blue-600
                        text-white
                        font-medium
                        text-xs
                        leading-tight
                        uppercase
                        rounded
                        shadow-md
                        hover:bg-blue-700 hover:shadow-lg
                        focus:bg-blue-700 focus:shadow-lg focus:outline-none focus:ring-0
                        active:bg-blue-800 active:shadow-lg active:text-white
                        transition
                        duration-150
                        ease-in-out
                        flex
                        items-center
                        whitespace-nowrap
                        ">Filters</MenuButton>
                    <MenuItems>
                        <!-- Use the `active` state to conditionally style the active item. -->
                        <MenuItem
                            v-for="link in links"
                            :key="link.href"
                            as="template"
                            v-slot="active"
                        >
                            <a
                            :href="link.href"
                            :class="{ 'bg-blue-500 text-white': active, 'bg-white text-black': !active }"
                            >
                            {{ link.label }}
                            </a>
                        </MenuItem>
                    </MenuItems>
                </Menu>
            </div>
            <div class="container">
                <li v-for="(value, index) in ds_names" datasets>
                    <DataSetPrev :ds_name="value" :ds_count="ds_counts[index]"/>
                </li>
            </div>
            
        </div>
    </div>

</template>

<script>
import DataSetPrev from '@/components/DataSetPrev.vue';
import axios from 'axios';
import { onMounted } from 'vue';
import { ref } from '@vue/reactivity';
import { Menu, MenuButton, MenuItems, MenuItem } from '@headlessui/vue'

export default {
    name : 'ExploreDataView',
    setup() {
        const ds_names = ref('')
        const ds_counts = ref('')
        const error = ref('')
        const active = ref(true)
        const links = [
            { href: '.', label: 'Press me!'},
            { href: '.', label: 'Placeholder2!'}
        ]
        onMounted(async () => {
            axios
            .get('http://127.0.0.1:5000/explore/')
            .then(response => (
                ds_names.value = response.data['ds_names'],
                ds_counts.value = response.data['ds_counts'],
                console.log(ds_names.value)
                ))
            .catch(error.value = "Failed to retreive data")
    
        })
        return { ds_names, ds_counts, error, active, links }
    },
    components: {DataSetPrev, Menu, MenuButton, MenuItems, MenuItems}
}
</script>

<style>
.container {
    border-width: 2px;
    border-radius: 10px;
    gap: 20px;
    display: grid;
    height: 650px;
    overflow-y: scroll;
    margin: 17px;
    padding: 10px;
}
.container li {
    list-style-type: none;
}
</style>