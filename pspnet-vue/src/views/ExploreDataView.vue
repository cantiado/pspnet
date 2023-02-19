<!-- Author: Antonio Lang -->

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
                        id="exampleSearch"
                        placeholder="Type query"
                        />
                    </div>
                </div>
                <!-- following div component from tailwind elements -->
                <div class="flex justify-center">
                    <div>
                        <div class="dropdown relative">
                        <button
                            class="
                            dropdown-toggle
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
                            "
                            type="button"
                            id="dropdownMenuButton1"
                            data-bs-toggle="dropdown"
                            aria-expanded="false"
                        >
                            Filters
                            <svg
                            aria-hidden="true"
                            focusable="false"
                            data-prefix="fas"
                            data-icon="caret-down"
                            class="w-2 ml-2"
                            role="img"
                            xmlns="http://www.w3.org/2000/svg"
                            viewBox="0 0 320 512"
                            >
                            <path
                                fill="currentColor"
                                d="M31.3 192h257.3c17.8 0 26.7 21.5 14.1 34.1L174.1 354.8c-7.8 7.8-20.5 7.8-28.3 0L17.2 226.1C4.6 213.5 13.5 192 31.3 192z"
                            ></path>
                            </svg>
                        </button>
                        <ul
                            class="
                            dropdown-menu
                            min-w-max
                            absolute
                            hidden
                            bg-white
                            text-base
                            z-50
                            float-left
                            py-2
                            list-none
                            text-left
                            rounded-lg
                            shadow-lg
                            mt-1
                            hidden
                            m-0
                            bg-clip-padding
                            border-none
                            "
                            aria-labelledby="dropdownMenuButton1"
                        >
                            <li>
                            <a
                                class="
                                dropdown-item
                                text-sm
                                py-2
                                px-4
                                font-normal
                                block
                                w-full
                                whitespace-nowrap
                                bg-transparent
                                text-gray-700
                                hover:bg-gray-100
                                "
                                href="#"
                                >Action</a
                            >
                            </li>
                            <li>
                            <a
                                class="
                                dropdown-item
                                text-sm
                                py-2
                                px-4
                                font-normal
                                block
                                w-full
                                whitespace-nowrap
                                bg-transparent
                                text-gray-700
                                hover:bg-gray-100
                                "
                                href="#"
                                >Another action</a
                            >
                            </li>
                            <li>
                            <a
                                class="
                                dropdown-item
                                text-sm
                                py-2
                                px-4
                                font-normal
                                block
                                w-full
                                whitespace-nowrap
                                bg-transparent
                                text-gray-700
                                hover:bg-gray-100
                                "
                                href="#"
                                >Something else here</a
                            >
                            </li>
                        </ul>
                        </div>
                    </div>
                </div>
            </div>
            <div class="container">
                <li v-for="(value, index) in ds_names" datasets>
                    <DataSetPrev :ds_name="value" :ds_count="ds_counts[index]"/>
                </li>
                <!-- <DataSetPrev/>
                <DataSetPrev/>
                <DataSetPrev/> -->
            </div>
        </div>
    </div>

</template>

<script>
import DataSetPrev from '@/components/DataSetPrev.vue';
import axios from 'axios';

export default {
    name : 'ExploreDataView',
    data() {
        return {
            ds_names: null,
            ds_counts: null,
            error: null
        }
    },
    mounted() {
        axios
        .get('http://127.0.0.1:5000/explore/')
        .then(response => (
            this.ds_names = response.data['ds_names'],
            this.ds_counts = response.data['ds_counts'],
            console.log(response),
            console.log(response.data['ds_names'])
            ))
        .catch(this.error = "Failed to retreive data")

    },
    components: {DataSetPrev}
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