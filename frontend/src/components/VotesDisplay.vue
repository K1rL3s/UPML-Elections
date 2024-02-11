<template>
  <div
    v-if="candidatesVotes"
    class="votes-display"
    :style="{ 'grid-template-rows': '1, auto' }"
  >
    <div
      class="candidate-bar-part flex items-center justify-center text-center"
      :style="{ 'background-color': this.colors.at(-1) }"
    >
      {{ this.candidatesVotes }} голосов
    </div>
  </div>
</template>

<script>
import axios from "axios";
import constants from "src/js/constants";

export default {
  username: "VotesDisplay",
  props: {
    colors: {
      required: true,
    },
  },

  mounted() {
    this.getVotes();
    this.$nextTick(() => {
      window.addEventListener("resize", this.onResize);
    });
  },

  data() {
    return {
      windowWidth: window.innerWidth,
      candidatesVotes: null,
    };
  },
  methods: {
    onResize() {
      this.windowWidth = window.innerWidth;
    },
    getVotes() {
      axios.get(constants.serverIp + "votes").then((req) => {
        this.candidatesVotes = req.data;
      });
    },
  },
  beforeUnmount() {
    window.removeEventListener("resize", this.onResize);
  },
};
</script>

<style lang="scss" scoped>
.votes-display {
  width: 100%;
  min-height: 15px;
  display: grid;
  border-radius: 5px;
  overflow: hidden;
}

.candidate-bar-part {
  overflow: hidden;
  color: white;
  //font-size: 100%;
}

@media (max-width: 768px) {
  .votes-display {
    height: 100vh;
  }
}
</style>
