<template>
  <div class="text-left flex flex-col gap-3 h-full">
    <h1 class="text-2xl font-bold border-b-2 pb-3">Connected Researchers</h1>
    <table v-if="affiliates.length" class="table-fixed">
      <thead>
        <tr class="bg-slate-100">
          <th class="pl-3 py-2">Name</th>
          <th class="py-2">Email</th>
          <th class="pr-3 py-2">Role</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="affiliate in affiliates" class="border-b-2 border-slate-300">
          <td class="pl-3">{{ affiliate.name }}</td>
          <td class="">{{ affiliate.email }}</td>
          <td class="pr-3">{{ affiliate.role }}</td>
        </tr>
      </tbody>
    </table>
    <div
      v-else
      class="flex flex-col gap-3 justify-start items-center text-center h-full"
    >
      <span class="mt-32 text-xl font-bold">No affiliates found!</span>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from "axios";
import { authStore } from "@/store/authenticate";

const affiliates = ref([]);

// Seeding affiliates
// const seedAffiliate = {
//   name: "First Last",
//   email: "someEmail@gmail.com",
//   role: "researcher",
//   projects: ["proj1", "proj2", "proj3"],
//   datasets: ["ds1", "ds2", "ds3", "ds4"],
// };
// var seededAffiliates = [];
// for (let i = 0; i < 25; i++) {
//   seededAffiliates.push(seedAffiliate);
// }
// affiliates.value = seededAffiliates;

onMounted(async () => {
  const data = await authStore().userData();
  if (data) {
    await axios.post("http://127.0.0.1:5000/collections/affiliates/", {id:data.id})
    .then(
      (response) => (
        affiliates.value = response.data['affiliates'],
        console.log(response.data)
      )
    ).catch(console.log("Error"))
  }
});
</script>
