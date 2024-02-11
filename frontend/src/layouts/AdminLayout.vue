<template>
  <q-layout>
    <div
      class="limiter flex column justify-center items-center"
      v-if="hasAccess"
    >
      <h3>Создать кандидата</h3>
      <q-btn color="primary" @click="addCandidate">Добавить кандидата</q-btn>
      <div class="form-wrapper flex justify-center">
        <q-form
          class="candidate-settings float column justify-center q-ma-md"
          v-for="(link, id) in candidatesSettingsList"
          :key="link"
          @submit="changeCandidateData(id)"
        >
          <q-input
            v-model="candidatesSettingsList[id].name"
            label="Имя кандидата"
            @update:model-value="changeCandidateData(id)"
          />
          <q-input
            v-model="candidatesSettingsList[id].surname"
            label="Фамилия кандидата"
            @update:model-value="changeCandidateData(id)"
          />
          <q-file
            v-model="candidatesSettingsList[id].image"
            accept=".jpg, .png, image/*"
            @update:model-value="changeCandidateData(id)"
            label="Новое фото кандидата"
          />
          <q-select
            v-model="candidatesSettingsList[id].gender"
            :options="selectOptions"
            label="Пол"
            @update:model-value="changeCandidateData(id)"
          />
          <div class="flex q-my-sm">
            <q-input
              v-model="candidatesSettingsList[id].votes"
              label="Количество очных голосов"
              @update:model-value="changeCandidateData(id)"
            />
            <div class="change-votes-btns flex column reverse">
              <q-btn icon="expand_more" @click="changeVotes(id, '-')"></q-btn>
              <q-btn icon="expand_less" @click="changeVotes(id, '+')"></q-btn>
            </div>
          </div>

          <q-btn icon="close" @click="deleteCandidate(id)"
            >Удалить Кандидата</q-btn
          >
        </q-form>
      </div>
      <q-checkbox
        label="Подвести итоги"
        @update:model-value="toggleEnd()"
        v-model="isEnded"
        :model-value="isEnded"
      />
      <q-checkbox
        label="Показать распределение голосов"
        @update:model-value="toggleShowVotes()"
        v-model="isVoteDisplayChecked"
        :model-value="isVoteDisplayChecked"
      />
    </div>
    <div
      class="unautorised flex column justify-center items-center text-center"
      v-else
    >
      <h1>У вас недостаточно полномочий</h1>
    </div>
  </q-layout>
</template>

<script>
import axios from "axios";
import constants from "src/js/constants";
import { mapGetters, mapMutations } from "vuex";

export default {
  name: "Admin",
  mounted() {
    axios
      .get(constants.serverIp + "login", {
        headers: { "Session-Id": this.sessionId },
      })
      .then((req) => {
        this.hasAccess = true;
      })
      .catch((req) => {
        this.hasAccess = false;
      });

    axios.get(constants.serverIp + "result").then((req) => {
      this.isEnded = req.data.is_end;
      this.isVoteDisplayChecked = req.data.is_show_votes;
      this.isShowVotes = req.data.is_show_votes;
    });

    axios
      .get(constants.serverIp + "candidates", {
        headers: { "Session-Id": this.sessionId },
      })
      .then((req) => {
        for (let i in req.data) {
          if (req.data[i].gender) {
            req.data[i].gender = "Мужской";
          } else {
            req.data[i].gender = "Женский";
          }
        }

        this.candidatesSettingsList = req.data;
      })
      .catch((req) => {
        console.log(req);
      });
  },

  data() {
    return {
      candidatesCount: 0,
      candidatesSettingsList: [],
      isVoteDisplayChecked: null,
      isShowVotes: false,
      hasAccess: false,
      candidatesShow: [],
      isEnded: false,
      selectOptions: ["Мужской", "Женский"],
    };
  },
  methods: {
    ...mapMutations("mainStore", []),
    changeVotes(id, action) {
      if (action === "+") {
        this.candidatesSettingsList[id].votes++;
      } else {
        this.candidatesSettingsList[id].votes--;
      }
      this.changeCandidateData(id);
    },

    addCandidate() {
      axios
        .post(
          constants.serverIp + "candidates",
          {},
          {
            headers: {
              "Session-Id": this.sessionId,
            },
          }
        )
        .then((req) => {
          this.candidatesSettingsList.push({
            id: req.data.id,
            name: "",
            surname: "",
            gender: "Мужской",
            image: req.data.image,
            votes: 0,
          });
        });
    },

    toggleEnd() {
      this.isEnded = !this.isEnded;
      this.updateResult();
    },
    toggleShowVotes() {
      this.isVoteDisplayChecked = !this.isVoteDisplayChecked;
      this.updateResult();
    },

    updateResult() {
      axios
        .put(
          constants.serverIp + "result",
          {
            is_end: this.isEnded,
            is_show_votes: this.isVoteDisplayChecked,
          },
          {
            headers: {
              "Session-Id": this.sessionId,
            },
          }
        )
        .then((req) => {
          this.isEnded = req.data.is_end;
          this.isShowVotes = req.data.is_show_votes;
          this.isVoteDisplayChecked = req.data.is_show_votes;
          console.log(req.data);
        });
    },
    deleteCandidate(id) {
      axios
        .delete(
          constants.serverIp +
            "candidates/" +
            this.candidatesSettingsList[id].id,
          {
            headers: {
              "Session-Id": this.sessionId,
            },
          }
        )
        .then((req) => {
          this.candidatesSettingsList.splice(id, 1);
        })
        .catch((req) => {
          console.log(123123);
          console.log(req);
        });
    },
    changeCandidateData(id) {
      console.log(this.candidatesSettingsList);
      let formData = new FormData();
      formData.append("candidate_id", this.candidatesSettingsList[id].id);
      if (this.candidatesSettingsList[id].name)
        formData.append("name", this.candidatesSettingsList[id].name);
      if (this.candidatesSettingsList[id].surname)
        formData.append("surname", this.candidatesSettingsList[id].surname);
      if (this.candidatesSettingsList[id].gender)
        formData.append(
          "gender",
          this.candidatesSettingsList[id].gender === "Мужской" ? 1 : 0
        );
      if (
        this.candidatesSettingsList[id].image &&
        typeof this.candidatesSettingsList[id].image !== "string"
      ) {
        formData.append("image", this.candidatesSettingsList[id].image);
      }
      if (this.candidatesSettingsList[id].votes)
        formData.append("votes", this.candidatesSettingsList[id].votes);
      axios
        .put(constants.serverIp + "candidates", formData, {
          headers: {
            "Session-Id": this.sessionId,
            "Content-Type": "application/json",
          },
        })
        .then((req) => {
          console.log(req);
        });
    },
  },
  computed: {
    ...mapGetters("mainStore", ["sessionId"]),
  },
};
</script>

<style lang="scss" scoped>
.unautorised {
  width: 100vw;
  height: 100vh;
}

h1 {
  font-size: 5vw !important;
}

.change-votes-btns {
  .q-btn {
    width: 10px;
    height: 10px;
  }
}
</style>
