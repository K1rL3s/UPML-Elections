<template>
  <div class="logo text-center">
    <slot></slot>
  </div>
</template>

<script>
export default {
  username: "Logo",
};
</script>

<style lang="scss" scoped>
.logo {
  font-family: Roboto, sans-serif;
  font-weight: 700;
  font-size: calc(15px + 0.7vw);
}
</style>
