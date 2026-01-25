<template>
  <div style="margin-top: 10px">
    <button v-if="isLast && submitted" @click="$emit('finish')">Abschließen</button>

    <button v-else @click="$emit('next')" :disabled="isLast || !submitted || loading">
      ➡️ Nächste Frage
    </button>
  </div>
</template>

<script>
  export default {
    props: {
      currentIndex: Number,
      total: Number,
      submitted: Boolean,
      loading: Boolean
    },
    computed: {
      isLast() {
        return this.currentIndex >= this.total - 1
      }
    }
  }
</script>
