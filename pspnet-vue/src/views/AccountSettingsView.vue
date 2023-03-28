<template>
  <div class="w-full bg-gray-50 grid grid-cols-1 place-content-start">
    <h1 class="text-left ml-10 font-bold text-lg my-5">Account Settings</h1>
    <div class="divide-y-2 ml-10 max-w-screen-lg">
      <div class="flex justify-between grow card border-t-2">
        <div class="setting">Name</div>
        <div v-if="!toggleName">{{ name }}</div>
        <input
          v-else
          class="text-center"
          ref="nameInput"
          v-model="name"
          @blur="commitChange"
          @keyup.enter="commitChange"
          type="text"
        />
        <div class="update" @click="toggleNewName">Update</div>
      </div>

      <div class="flex justify-between grow card">
        <div class="setting">Email</div>
        <div v-if="!toggleEmail">{{ email }}</div>
        <input
          ref="emailInput"
          class="text-center"
          v-model="email"
          @blur="commitChange"
          @keyup.enter="commitChange"
          v-else
          type="text"
        />
        <div @click="toggleNewEmail" class="update">Update</div>
      </div>

      <div class="flex justify-between grow card">
        <div class="setting">Role</div>
        <div>{{ role }}</div>
        <div></div>
      </div>
    </div>

    <div v-if="error_msg" class="error">
      {{ error_msg }}
    </div>

    <div class="max-w-xs">
      <form class="ml-10" @submit.prevent="handleSubmit">
        <h1 class="text-left font-bold text-lg my-5">Change Password</h1>
        <input
          v-model="pass"
          class="rounded-xl my-2 bg-gray-100 input"
          type="password"
          placeholder="New Password"
          required
        />
        <input
          v-model="newpass"
          class="rounded-xl my-2 bg-gray-100 input"
          type="password"
          placeholder="Confirm New Password"
          required
        />
        <button class="button bg-plant hover:bg-green-400 font-bold w-full">
          Submit
        </button>
      </form>
    </div>
    <div class="error max-w-md" v-if="pass_err">
      {{ pass_err }}
    </div>

    <div v-if="good_msg" class="max-w-md">
      <EmailSuccess
        message="Your password was succesfully changed"
      ></EmailSuccess>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeMount, nextTick } from "vue";
import { authStore } from "@/store/authenticate";
import { update_user_settings } from "@/helpers";
import { useRouter } from "vue-router";
import EmailSuccess from "@/components/EmailSuccess.vue";
import { resetPass } from "@/api/";

const store = authStore();
const name = ref("");
const email = ref("");
const role = ref("");

const pass = ref("");
const newpass = ref("");

const error_msg = ref("");
const pass_err = ref("");
const good_msg = ref("");
//refs to DOM elements to focus inputs
const nameInput = ref(null);
const emailInput = ref(null);

const toggleEmail = ref(false);
const toggleName = ref(false);

async function commitChange() {
  toggleEmail.value = false;
  toggleName.value = false;
  if (name.value.split(" ").length != 2) {
    error_msg = "Please add first and last name";
  } else {
    await update_user_settings({
      email: email.value,
      firstname: name.value.split(" ")[0],
      lastname: name.value.split(" ")[1],
    });
  }
}

function toggleNewEmail() {
  toggleEmail.value = true;
  nextTick(() => {
    emailInput.value.focus();
  });
}

function toggleNewName() {
  toggleName.value = true;
  nextTick(() => {
    nameInput.value.focus();
  });
}

async function handleSubmit() {
  if (pass.value == newpass.value) {
    try {
      const res = await resetPass(
        { new_password: pass.value },
        localStorage.getItem("userToken")
      );
      good_msg.value = res.data.message;
    } catch (err) {
      pass_err.value = err.response.data.message;
    }
  } else {
    pass_err.value = "Passwords do not match";
  }
  pass.value = "";
  newpass.value = "";
}

onBeforeMount(() => {
  if (!store.isAuthenticated()) {
    const router = useRouter();
    router.push({ name: "login" });
  }
});

onMounted(async () => {
  const data = await store.userData();
  name.value = data.name;
  email.value = data.email;
  role.value = data.role;
});
</script>

<!-- <script>
import { ref } from "@vue/reactivity";
import { authStore } from "@/store/authenticate";
import { onMounted } from "@vue/runtime-core";
import { nextTick } from "vue";
import { update_user_settings } from "@/helpers";
import { useRouter } from "vue-router";
import EmailSuccess from "@/components/EmailSuccess.vue";
import { resetPass } from "@/api/";

export default {
  name: "AccountSettingsView",
  components: { EmailSuccess },
  setup() {
    const store = authStore();
    const name = ref("");
    const email = ref("");
    const role = ref("");

    const pass = ref("");
    const newpass = ref("");

    const error_msg = ref("");
    const pass_err = ref("");
    const good_msg = ref("");
    //refs to DOM elements to focus inputs
    const nameInput = ref(null);
    const emailInput = ref(null);

    const toggleEmail = ref(false);
    const toggleName = ref(false);

    onMounted(async () => {
      const data = await store.userData();
      name.value = data.name;
      email.value = data.email;
      role.value = data.role;
    });
    const commitChange = async () => {
      toggleEmail.value = false;
      toggleName.value = false;
      if (name.value.split(" ").length != 2) {
        error_msg = "Please add first and last name";
      } else {
        await update_user_settings({
          email: email.value,
          firstname: name.value.split(" ")[0],
          lastname: name.value.split(" ")[1],
        });
      }
    };

    const toggleNewEmail = () => {
      toggleEmail.value = true;
      nextTick(() => {
        emailInput.value.focus();
      });
    };
    const toggleNewName = () => {
      toggleName.value = true;
      nextTick(() => {
        nameInput.value.focus();
      });
    };

    const handleSubmit = async () => {
      if (pass.value == newpass.value) {
        try {
          const res = await resetPass(
            { new_password: pass.value },
            localStorage.getItem("userToken")
          );
          good_msg.value = res.data.message;
        } catch (err) {
          pass_err.value = err.response.data.message;
        }
      } else {
        pass_err.value = "Passwords do not match";
      }
      pass.value = "";
      newpass.value = "";
    };

    return {
      name,
      good_msg,
      newpass,
      pass_err,
      pass,
      email,
      role,
      toggleNewEmail,
      handleSubmit,
      toggleNewName,
      toggleName,
      toggleEmail,
      commitChange,
      nameInput,
      emailInput,
      error_msg,
    };
  },
  beforeMount() {
    const store = authStore();
    if (!store.isAuthenticated()) {
      const router = useRouter();
      router.push({ name: "login" });
    }
  },
};
</script> -->

<style lang="postcss" scoped>
input {
  @apply rounded-xl my-2 bg-gray-100;
}

.card {
  @apply h-20 items-center;
}

.update {
  @apply text-blue-400 hover:cursor-pointer;
}

.setting {
  @apply text-gray-500;
}

.button {
  @apply rounded-xl my-1;
}
</style>
