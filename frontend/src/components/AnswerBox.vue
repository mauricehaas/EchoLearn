<template>
  <div class="answer-box">
    <textarea
      :value="modelValue"
      @input="$emit('update:modelValue', $event.target.value)"
      placeholder="Deine erkannte Antwort"
      :disabled="locked"
    ></textarea>

    <div class="submit-container">
      <button class="submit" @click="$emit('submit')" :disabled="!modelValue || loading || locked">
        {{ loading ? 'Wird geprüft…' : '🚀 Antwort absenden' }}
      </button>

      <span v-if="loading" class="spinner"></span>
    </div>
  </div>
</template>

<script>
  export default {
    props: {
      modelValue: String,
      loading: Boolean,
      locked: Boolean
    },
    emits: ['update:modelValue', 'submit']
  }
</script>

<style scoped lang="scss">
  .answer-box {
    margin-top: 10px;
    max-width: 600px;

    textarea {
      width: 100%;
      min-height: 90px;
      resize: vertical;
      padding: 10px;
      font-size: 1rem;
      border-radius: 8px;
      border: 1px solid #ccc;
      box-sizing: border-box;

      &:focus {
        outline: none;
        border-color: #4a90e2;
      }
    }

    .submit-container {
      display: inline-flex;
      align-items: center;
      gap: 10px;
      margin-top: 8px;
    }

    button:disabled {
      background-color: #ddd;
      color: #888;
      cursor: not-allowed;
    }
  }
</style>
