<template>
  <q-layout class="flex justify-center items-center">
    <q-card class="q-pa-xl">
      <q-form
        class="flex column justify-center items-center"
        @submit="onSubmit"
      >
        <h3 class="q-mb-sm">Вход</h3>
        <q-input
          type="text"
          v-model="username"
          model-value=""
          label="Логин"
          class="q-mb-md"
          lazy-rules
          :rules="[
            (val) => !!val || 'Это поле обязательное',
          ]"
        />
        <q-input
          type="password"
          v-model="password"
          model-value=""
          label="Пароль"
          class="q-mb-md"
          lazy-rules
          :rules="[(val) => !!val || 'Это поле обязательное']"
        />
        <q-btn color="primary" class="q-mt-sm" type="submit">Вход</q-btn>
        <a href="/" class="q-mt-md">На главную</a>
      </q-form>
    </q-card>
  </q-layout>
</template>

<script>
import { ref } from "vue";
import axios from "axios";
import constants from "src/js/constants";
import { mapMutations } from "vuex";
import { useQuasar } from "quasar";

export default {
  name: "LoginLayout",
  setup() {
    let $q = useQuasar();
    return {
      triggerNotification(message, type) {
        $q.notify({
          type: type,
          message: message,
        });
      },
    };
  },
  mounted() {
    // let username = null, password = null
    if (this.$route.params.name) {
      this.username = this.$route.params.name;
      this.password = this.$route.params.password;
    }
  },
  data() {
    return {
      username: null,
      password: null,
      serverIp: constants.serverIp,
    };
  },
  methods: {
    ...mapMutations("mainStore", ["login"]),
    onSubmit() {
      axios
        .post(constants.serverIp + "login", {
          login: this.username,
          password: this.password,
        },
        {
          headers: {"Session-Id": this.sessionId}
        })
        .then((req) => {
          let sessionId = req.data.session_id;
          this.login(sessionId)
          this.$router.push("/")
        })
        .catch((err) => {
          console.log(err);
          this.triggerNotification("Неправильный логин или пароль", "negative");
        });
    },
  },
};
</script>

<style scoped>
.q-card {
  border-radius: 20px;
}

.q-btn {
  width: 100%;
}

.q-input {
  width: 100%;
}

a {
  color: black;
}
</style>
