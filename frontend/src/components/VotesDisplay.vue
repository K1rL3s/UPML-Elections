<template>
  <div
    class="votes-display"
    :style="{
      'grid-template-columns': `repeat(${columnsTemplate})`,
      'grid-template-rows': `repeat(${rowsTemplate})`,
    }"
  >
    <div
      class="candidate-bar-part flex items-center justify-center text-center"
      v-for="id in candidatesCount"
      :key="id"
      :style="{ 'background-color': this.colors[id - 1] }"
    >
      {{ this.candidatesPercentage[id - 1][1].toFixed(1) + "%" }}
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
    candidates: {
      required: true,
    },
  },
  mounted() {
    this.$nextTick(() => {
      window.addEventListener("resize", this.onResize);
    });
    axios.get(constants.serverIp + "percentage/").then((req) => {
      this.candidatesPercentage = req.data;
    });
  },
  data() {
    return {
      windowWidth: window.innerWidth,
      candidatesPercentage: null,
    };
  },
  methods: {
    onResize() {
      this.windowWidth = window.innerWidth;
    },
  },
  computed: {
    candidatesCount() {
      if (this.candidates) {
        return Object.keys(this.candidates).length;
      }
      return 0;
    },
    // candidatesPercentage() {
    //   if (this.candidates) {
    //     for (let candidate of this.candidates) {
    //       let candidateVotesCount = candidate.onlineVotes + candidate.offlineVotes
    //       // console.log(candidate)
    //     }
    //     return Object.values(this.candidates).map((object) => object.percentage)
    //   }
    //   return []
    // },
    gridSettings() {
      if (this.candidatesPercentage) {
        let settings = `${this.candidatesCount},`;
        console.log(this.candidatesPercentage);
        return (
          settings +
          this.candidatesPercentage
            .map((el) => {
              return el[1];
            })
            .join("% ") +
          "%"
        );
      }
      return null;
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
