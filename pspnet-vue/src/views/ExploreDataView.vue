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
                        v-model="searchInput"
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
                        @change="searchFilter"
                        />
                    </div>
                </div>
                <!-- following div component from tailwind elements -->
                <Menu as="div" class="dropdown">
                    <MenuButton as="div" class="dropdown-toggle
                        px-6
                        py-2.5
                        bg-[#b9e0a5]
                        text-black
                        font-medium
                        text-xs
                        leading-tight
                        uppercase
                        rounded
                        shadow-md
                        hover:bg-green-800 hover:shadow-lg
                        focus:bg-green-800 focus:shadow-lg focus:outline-none focus:ring-0 text-white
                        active:bg-[#b9e0a5] active:shadow-lg active:text-black
                        transition
                        duration-150
                        ease-in-out
                        flex
                        items-center
                        whitespace-nowrap
                        ">Filters</MenuButton>
                    <MenuItems class="dropdown">
                        <!-- Use the `active` state to conditionally style the active item. -->
                        <MenuItem
                            v-for="link in links"
                            :key="link.href"
                            as="div"
                            v-slot="active"
                            class="group flex w-full items-center justify-center rounded-md px-2 py-2 text-sm hover:bg-gray-100"
                            @click="applyFilter(link.filter)">
                            {{ link.label }}
                        </MenuItem>
                    </MenuItems>
                </Menu>
            </div>
            <div class="container">
                <li v-for="(value, index) in filteredData" datasets>
                    <DataSetPrev :ds_name="index" :ds_count="value"/>
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
        const error = ref('')
        const active = ref(true)
        const searchInput = ref('')
        const filteredData = ref('')
        const ds_info = ref('')
        const links = [
            { filter: 'img l 5', label: 'Fewer than 5 images'},
            { filter: 'class eq 1', label: 'Single-Class Datasets'}
        ]

        const searchFilter = () => {
            filteredData.value = Object.fromEntries(Object.entries(ds_info.value).filter(([k,v]) => k.includes(searchInput.value)))
            console.log(filteredData.value)
        }

        const applyFilter = (filter) => {
            if (filter == "img l 5") {
                console.log("Filter datasets with fewer than 5 images")
                // Adapted from: https://9to5answer.com/how-to-filter-a-dictionary-by-value-in-javascript
                filteredData.value = Object.fromEntries(Object.entries(ds_info.value).filter(([k,v]) => v<5));
            }
            if (filter == "class eq 1") {
                console.log("Filter datasets with one class")
            }
        }

        onMounted(async () => {
            axios
            .get('http://127.0.0.1:5000/explore/')
            .then(response => (
                ds_info.value = response.data['ds_info'],
                filteredData.value = response.data['ds_info'],
                console.log(response.data)
                ))
            .catch(error.value = "Failed to retreive data")
    
        })
        return { ds_info, filteredData, error, active, links, searchInput, applyFilter, searchFilter}
    },
    components: {DataSetPrev, Menu, MenuButton, MenuItem, MenuItems}
}
</script>

<style>
.container {
    border-width: 3px;
    border-radius: 10px;
    gap: 20px;
    display: grid;
    height: 120%;
    overflow-y: scroll;
    margin: 17px;
    padding: 10px;
}
.container li {
    list-style-type: none;
}
.dropdown {
    border-color: aquamarine;
}
</style>