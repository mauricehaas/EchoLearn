<template>
  <div style="margin-top: 10px">
    <button v-if="isLast && submitted" @click="finishExam" :disabled="loading">Abschließen</button>
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
      loading: Boolean,
      examId: String
    },
    data() {
      return {
        finishMessage: ''
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

        try {
          const res = await fetch(`http://localhost:8000/exam/evaluate_exam`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({ unique_exam_id: this.examId })
          })

          if (!res.ok) throw new Error(res.status)

          const data = await res.json()
          this.finishMessage = data.final_feedback || 'Prüfung abgeschlossen.'

          this.$emit('finish', this.finishMessage)
        } catch (err) {
          console.error('Fehler beim Abschließen:', err)
          this.$emit('finish', 'Fehler beim Abschließen der Prüfung.')
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
