<template>
  <div style="margin-top: 10px; display: inline-flex; align-items: center; gap: 8px">
    <button v-if="isLast && submitted" @click="finishExam" :disabled="localLoading || loading">
      {{ localLoading ? 'Lädt…' : 'Abschließen' }}
    </button>

    <button v-else @click="$emit('next')" :disabled="isLast || !submitted || loading">
      ➡️ Nächste Frage
    </button>
    <span v-if="localLoading" class="spinner"></span>
  </div>
</template>

<script>
  export default {
    props: {
      currentIndex: Number,
      total: Number,
      submitted: Boolean,
      loading: Boolean,
      examId: String
    },
    data() {
      return {
        finishMessage: '',
        localLoading: false
      }
    },
    computed: {
      isLast() {
        return this.currentIndex >= this.total - 1
      }
    },
    methods: {
      async finishExam() {
        if (!this.examId) {
          console.error('examId fehlt!')
          return
        }

        this.localLoading = true

        try {
          const res = await fetch(`http://localhost:8000/exam/evaluate_exam`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ unique_exam_id: this.examId })
          })

          if (!res.ok) throw new Error(res.status)

          const data = await res.json()
          this.finishMessage = data.final_feedback || 'Prüfung abgeschlossen.'
          this.$emit('finish', this.finishMessage)
        } catch (err) {
          console.error('Fehler beim Abschließen:', err)
          this.$emit('finish', 'Fehler beim Abschließen der Prüfung.')
        } finally {
          this.localLoading = false
        }
      }
    }
  }
</script>

<style scoped>
  button {
    margin-right: 10px;
  }
</style>
