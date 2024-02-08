<template>
  <div
    class="candidate-wrapper flex column justify-center items-center"
    v-if="!(candidate.name.includes('Против') && role === 2)"
  >
    <div class="candidate shadow-10 flex column justify-center items-center">
      <div class="image-wrapper flex column justify-center">
        <img
          :src="serverIp + 'images/' + candidate.image"
          alt="Фото кандидата"
        />
      </div>
      <h4 class="q-my-sm">{{ candidate.name + " " + candidate.surname }}</h4>
      <div class="color-line" :style="{ 'background-color': color }" />
    </div>
    <q-btn
      :style="{ 'background-color': color }"
      class="q-mt-md"
      v-if="sessionId && !isVoted && role !== 2"
      @click="vote"
    >
      Проголосовать
    </q-btn>
  </div>
</template>

<script>
import { mapGetters, mapMutations } from "vuex";
import axios from "axios";
import constants from "src/js/constants";

export default {
  username: "Elected",
  props: {
    candidate: {
      default: {
        name: "Voloďa",
        surname: "Simkin",
        image: "http://www.rosphoto.com/images/u/articles/1510/4_8.jpg",
        offlineVotes: 10000,
        onlineVotes: 10000,
      },
    },
    color: { default: "red" },
  },
  data() {
    return {
      serverIp: constants.serverIp,
    };
  },
  methods: {
    ...mapMutations("mainStore", ["mutateVote"]),
    vote() {
      axios
        .post(constants.serverIp + "vote/", {
          session_id: this.sessionId,
          candidate_id: this.candidate.candidateId,
        })
        .then((req) => {
          console.log(req);
        })
        .catch((req) => {
          console.log(req);
        });
      this.mutateVote();
    },
  },
  computed: {
    ...mapGetters("mainStore", ["sessionId", "isVoted", "role"]),
  },
};
</script>

<style scoped>
.candidate-wrapper {
  max-width: 23%;
  margin-left: 1%;
  margin-right: 1%;
}

.candidate {
  border-radius: 10px;
  overflow: hidden;
}

.image-wrapper {
  flex-grow: 1;
}

img {
  width: 100%;
}

.candidate {
  text-align: center;
}

.color-line {
  height: 20px;
  width: 100%;
}

.candidate-wrapper {
  flex-grow: 1;
}
</style>
