<template>
  <div
    v-if="candidatesPercentage"
    class="percentage-display"
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
  username: "PercentageDisplay",
  props: {
    colors: {
      required: true,
    },
    candidates: {
      required: true,
    },
  },

  mounted() {
    this.getPercentage();
    this.$nextTick(() => {
      window.addEventListener("resize", this.onResize);
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
    getPercentage() {
      axios.get(constants.serverIp + "percentage").then((req) => {
        this.candidatesPercentage = req.data;
      });
    },
  },
  computed: {
    candidatesCount() {
      if (this.candidates) {
        return Object.keys(this.candidates).length;
      }
      return 0;
    },
    gridSettings() {
      if (!this.candidatesPercentage) {this.getPercentage()};
      let settings = `${this.candidatesCount},`;
      return (
        settings +
        this.candidatesPercentage
          .map((el) => {
            return el[1];
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
.percentage-display {
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
  .percentage-display {
    height: 100vh;
  }
}
</style>
