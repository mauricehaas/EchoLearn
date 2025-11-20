<template>
  <div>
    <h1>Lernbereich</h1>
    <p>Hier werden die Karteikarten angezeigt.</p>
    <Card v-for="card in previewCards" :key="card.id" :card="card" />
  </div>
</template>

<script>
import Card from '../components/Card.vue'

export default {
  components: { Card },

  setup() {
    const previewCards = [
      { id: 1, question: 'Was ist Vue?', answer: 'Ein progressives JS-Framework.' },
      { id: 2, question: 'SCSS oder CSS?', answer: 'SCSS für bessere Struktur.' },
      { id: 3, question: 'Docker nutzen?', answer: 'Ja, für lokales Setup.' }
    ]

    return { previewCards }
  }
}
</script>
