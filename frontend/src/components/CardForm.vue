<template>
  <div class="card-form">
    <h2>Karteikarte erstellen</h2>
    <form @submit.prevent="submitCard">
      <div>
        <label for="question">Frage:</label>
        <input id="question" v-model="question" required />
      </div>
      <div>
        <label for="answer">Antwort:</label>
        <input id="answer" v-model="answer" required />
      </div>
      <button type="submit">Speichern</button>
    </form>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      question: '',
      answer: ''
    }
  },
  methods: {
    async submitCard() {
      try {
        await axios.post('http://localhost:8000/cards', {
          question: this.question,
          answer: this.answer
        })
        this.$emit('card-added') // Parent kann Liste neu laden
        this.question = ''
        this.answer = ''
      } catch (err) {
        console.error(err)
        alert('Fehler beim Speichern der Karte')
      }
    }
  }
}
</script>

<style scoped>
.card-form {
  max-width: 500px;
  margin: 20px auto;
  display: flex;
  flex-direction: column;
  gap: 10px;
}
</style>
