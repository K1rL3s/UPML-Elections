<template>
  <div class="create-candidate flex">
    <q-input :model-value="name" hint="Имя кандидата"></q-input>
    <q-input model-value="surname"></q-input>
    <q-file
      rounded
      bottom-slots
      v-model="model"
      label="Фото кандидата"
      counter
      max-files="12"
    >
      <template v-slot:append>
        <q-icon
          v-if="model !== null"
          name="close"
          @click.stop="model = null"
          class="cursor-pointer"
        />
        <q-icon name="search" @click.stop />
      </template>
    </q-file>
    <q-btn icon="close"></q-btn>
  </div>
</template>

<script>
import { ref } from "vue";

export default {
  name: "CreateCandidate",
  data() {
    return {
      name: ref(null),
    };
  },
};
</script>

<style lang="scss" scoped>
.create-candidate {
  * {
    margin-left: 10px;
    margin-right: 10px;
  }
}
</style>
