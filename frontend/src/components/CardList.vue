<template>
  <div class="card-list">
    <h2>Alle Karteikarten</h2>
    <div v-if="cards.length === 0">Keine Karten vorhanden.</div>
    <div v-for="card in cards" :key="card.id" class="card-item">
      <strong>Frage:</strong> {{ card.question }} <br />
      <strong>Antwort:</strong> {{ card.answer }} <br />
      <button @click="deleteCard(card.id)">Löschen</button>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      cards: []
    }
  },
  methods: {
    async fetchCards() {
      const res = await axios.get('http://localhost:8000/cards')
      this.cards = res.data
    },
    async deleteCard(id) {
      try {
        await axios.delete(`http://localhost:8000/cards/${id}`)
        this.fetchCards()
      } catch (err) {
        console.error(err)
      }
    }
  },
  mounted() {
    this.fetchCards()
  }
}
</script>

<style scoped>
.card-item {
  border: 1px solid #ccc;
  padding: 10px;
  margin-bottom: 10px;
}
</style>
