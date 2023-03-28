<template>
  <div class="w-full grid place-content-center">
    <div v-if="!good_msg" class="max-w-xs">
      <h1 class="text-4xl text-center">Forgot password</h1>
      <h2 class="text-1xl text-center">
        Password reset instructions will be sent to you by email
      </h2>

      <form class="form" @submit.prevent="handleSubmit">
        <input
          v-model="email"
          type="email"
          placeholder="Email"
          class="input"
          required
        />
        <button class="button bg-plant hover:bg-green-400 font-bold w-full">
          Submit
        </button>

        <div v-if="error_msg" class="error">{{ error_msg }}</div>
      </form>
    </div>

    <div v-if="good_msg" class="max-w-md">
      <EmailSuccess
        message="Success! Check your Email for password reset instructions"
      ></EmailSuccess>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { sendEmail } from "@/api";
import EmailSuccess from "@/components/EmailSuccess.vue";

const email = ref("");
const error_msg = ref("");
const good_msg = ref("");

async function handleSubmit() {
  try {
    const res = await sendEmail(email.value);
    good_msg.value = res.data.message;
  } catch (err) {
    error_msg.value = err.response.data.message;
  }
}
</script>

<!-- <script>
import { ref } from "vue";
import { sendEmail } from "@/api";
import EmailSuccess from "@/components/EmailSuccess.vue";

export default {
  name: "ForgotView",
  components: { EmailSuccess },
  setup() {
    const email = ref("");
    const error_msg = ref("");
    const good_msg = ref("");

    const handleSubmit = async () => {
      try {
        const res = await sendEmail(email.value);
        good_msg.value = res.data.message;
      } catch (err) {
        error_msg.value = err.response.data.message;
      }
    };
    return { handleSubmit, email, good_msg, error_msg };
  },
};
</script> -->

<style lang="postcss" scoped>
.form {
  @apply mt-7 mb-7  text-left p-0 max-w-xs;
}

.input {
  @apply rounded-xl my-2 bg-gray-100;
}

.button {
  @apply rounded-xl my-1;
}
</style>
