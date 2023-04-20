<template>
  <div class="text-left flex flex-col gap-3 h-full">
    <h1 class="text-2xl font-bold border-b-2 pb-3">Connected Researchers</h1>
    <div v-if="affiliates.length"></div>
    <div
      v-else
      class="flex flex-col gap-3 justify-start items-center text-center h-full"
    >
      <span class="mt-32 text-xl font-bold">No affiliates found!</span>
      <label class="text-lg" for="invite-email">Invite Researchers</label>
      <div class="w-1/2 flex">
        <button
          @click="submitEmails"
          class="bg-slate-100 hover:bg-blue-200 border-l-2 b-y-2 rounded-l-lg px-3 py-2"
          name="submit-email"
          type="submit"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 24 24"
            fill="currentColor"
            class="w-6 h-6"
          >
            <path
              d="M6.25 6.375a4.125 4.125 0 118.25 0 4.125 4.125 0 01-8.25 0zM3.25 19.125a7.125 7.125 0 0114.25 0v.003l-.001.119a.75.75 0 01-.363.63 13.067 13.067 0 01-6.761 1.873c-2.472 0-4.786-.684-6.76-1.873a.75.75 0 01-.364-.63l-.001-.122zM19.75 7.5a.75.75 0 00-1.5 0v2.25H16a.75.75 0 000 1.5h2.25v2.25a.75.75 0 001.5 0v-2.25H22a.75.75 0 000-1.5h-2.25V7.5z"
            />
          </svg>
        </button>
        <input
          v-model="emailInput"
          class="border-2 rounded-r-lg w-full px-3 py-2 focus:outline-none invalid:text-red-500 invalid:border-red-500"
          placeholder="person1@email.com, person2@email.com, ..."
          type="email"
          id="input-email"
          name="input-email"
          multiple
        />
      </div>
      <span v-if="errorMessage" class="text-red-500 italic">{{
        errorMessage
      }}</span>
      <span v-if="successMessage" class="text-green-500">{{
        successMessage
      }}</span>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";

const affiliates = ref([]);
const emailInput = ref("");
const errorMessage = ref("");
const successMessage = ref("");

function submitEmails() {
  successMessage.value = "";
  if (!emailInput.value) {
    console.log("empty");
    errorMessage.value = "Please enter email(s) before submitting";
    return;
  }
  if (!checkEmailValidity()) {
    errorMessage.value = "Please enter valid email(s) before submitting";
    return;
  }
  errorMessage.value = "";
  const emails = emailInput.value.split(",");
  for (const email of emails) {
    // send invite to each email
  }
  successMessage.value = "Successfully invited!";
}

function checkEmailValidity() {
  const emails = emailInput.value.split(",");
  for (const email of emails) {
    if (
      !/^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$/.test(
        email
      )
    ) {
      return false;
    }
  }
  return true;
}
</script>
