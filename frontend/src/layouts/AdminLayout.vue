<template>
  <q-layout>
    <div
      class="limiter flex column justify-center items-center"
      v-if="role !== 0"
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
            :rules="[(val) => !!val || 'Поле обязательное']"
            @update:model-value="changeCandidateData(id)"
          />
          <q-input
            v-model="candidatesSettingsList[id].surname"
            label="Фамилия кандидата"
            :rules="[(val) => !!val || 'Поле обязательное']"
            @update:model-value="changeCandidateData(id)"
          />
          <q-input
            v-model="candidatesSettingsList[id].patronymic"
            label="Отчество кандидата"
            :rules="[(val) => !!val || 'Поле обязательное']"
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
import { toggleVoteDisplay } from "src/store/MainStore/mutations";

export default {
  name: "Admin",
  mounted() {
    this.isVoteDisplayChecked = this.isVoteDisplayShown;
    this.isNameShowed = this.isNameShown;
    axios
      .get(constants.serverIp + "candidates/")
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
    axios.get(constants.serverIp + "end/").then((req) => {
      this.isEnded = req.data.is_end;
    });
  },
  data() {
    return {
      candidatesCount: 0,
      candidatesSettingsList: [],
      isVoteDisplayChecked: null,
      isNameShowed: null,
      candidatesShow: [],
      isEnded: false,
      selectOptions: ["Мужской", "Женский"],
    };
  },
  methods: {
    ...mapMutations("mainStore", [
      "toggleVoteDisplay",
      "toggleNameShow",
      "changeCandidatesShown",
      "changeWinnerName",
      "toggleVoteDisplay",
    ]),
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
            name: "",
            surname: "",
            patronymic: "",
            gender: "Мужской",
            image: "",
            votes: 0,
          });
        });
    },
    toggleEnd() {
      axios
        .post(
          constants.serverIp + "end",
          {},
          {
            headers: {
              "Session-Id": this.sessionId,
            },
          }
        )
        .then((req) => {
          this.isEnded = req.data.is_end;
          this.changeWinnerName(req.data.winner_name);
          console.log(req.data);
        });
    },
    toggleShowVotes() {
      this.isVoteDisplayChecked = !this.isVoteDisplayChecked;
      this.toggleVoteDisplay();
    },
    deleteCandidate(id) {
      axios.delete(
        constants.serverIp + "candidates/" + this.candidatesSettingsList[id].id,
        {},
        {
          headers: {
            "Session-Id": this.sessionId,
          },
        }
      );
      this.candidatesSettingsList.splice(id, 1);
    },
    changeCandidateData(id) {
      let jsonData = {};
      jsonData["id"] = this.candidatesSettingsList[id].id;
      jsonData["name"] = this.candidatesSettingsList[id].name;
      jsonData["surname"] = this.candidatesSettingsList[id].surname;
      jsonData["patronymic"] = this.candidatesSettingsList[id].patronymic;
      jsonData["gender"] =
        this.candidatesSettingsList[id].gender === "Мужской" ? 1 : 0;
      if (
        this.candidatesSettingsList[id].image &&
        typeof this.candidatesSettingsList[id].image !== "string"
      ) {
        jsonData["image"] = this.candidatesSettingsList[id].image;
      }
      jsonData["votes"] = this.candidatesSettingsList[id].votes;
      axios
        .put(constants.serverIp + "candidates/", jsonData, {
          headers: {
            "Content-Type": "application/json",
          },
        })
        .then((req) => {
          console.log(req);
        });
    },
  },
  computed: {
    ...mapGetters("mainStore", [
      "sessionId",
      "isVoteDisplayShown",
      "isNameShown",
      "role",
    ]),
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
