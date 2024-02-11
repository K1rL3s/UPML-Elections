<template>
  <div class="container">
    <div class="large-12 medium-12 small-12 cell">
      <label
        >File
        <q-file v-model="file"></q-file>
      </label>
      <button v-on:click="submitFile()">Submit</button>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import constants from "src/js/constants";

export default {
  data() {
    return {
      file: null,
    };
  },

  methods: {
    submitFile() {
      let formData = new FormData();
      formData.append("name", "asd");
      formData.append("file", this.file);

      axios
        .post(
          constants.serverIp + "images",

          formData,
          {
            headers: {
              "Content-Type": "multipart/form-data",
            },
          }
        )
        .then((req) => {
          console.log(req.data);
        })
        .catch(function () {
          console.log("FAILURE!!");
        });
    },
  },
};
</script>
