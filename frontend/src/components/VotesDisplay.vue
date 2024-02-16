<template>
  <div
    v-if="candidatesVotes"
    class="votes-display"
    :style="{
      'grid-template-columns': `repeat(${columnsTemplate})`,
      'grid-template-rows': `repeat(${rowsTemplate})`,
    }"
  >
    <div
      class="candidate-bar-part flex items-center justify-center text-center"
      :style="{ 'background-color': this.colors.at(-2) }"
    >
      {{ this.candidatesVotes[0][0].toFixed(1) + "%" }}
      ({{ this.candidatesVotes[0][1] }})
    </div>
    <div
      class="candidate-bar-part flex items-center justify-center text-center"
      :style="{ 'background-color': this.colors.at(-1) }"
    >
      {{ this.candidatesVotes[1][0].toFixed(1) + "%" }}
      ({{ this.candidatesVotes[1][1] }})
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
    if (!this.candidatesVotes) {
      this.getVotes();
    }
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
  computed: {
    gridSettings() {
      if (!this.candidatesVotes) {
        this.getVotes();
      }
      let settings = `${this.candidatesVotes.length},`;
      return (
        settings +
        this.candidatesVotes
          .map((el) => {
            return el[0];
          })
          .join("% ") +
        "%"
      );
    },
    rowsTemplate() {
      if (this.windowWidth < 768) {
        return this.gridSettings;
      }
      return "1, auto";
    },
    columnsTemplate() {
      if (this.windowWidth < 768) {
        return "1, auto";
      }
      return this.gridSettings;
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
