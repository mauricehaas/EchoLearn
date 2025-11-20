<template>
  <button class="btn-primary" @click="$emit('click')">
    {{ text }}
  </button>
</template>

<script>
export default {
  name: 'ButtonPrimary',
  props: {
    text: {
      type: String,
      required: true
    }
  }
}
</script>

<style scoped lang="scss">
.btn-primary {
  background-color: #4a90e2;
  color: #fff;
  border: none;
  padding: 10px 20px;
  font-size: 1rem;
  border-radius: 6px;
  cursor: pointer;
  transition: background-color 0.2s ease;

  &:hover {
    background-color: #357ab8;
  }

  &:active {
    background-color: #2a5d8f;
  }
}
</style>
