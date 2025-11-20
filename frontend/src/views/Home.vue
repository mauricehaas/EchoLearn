<template>
  <div class="home">
    <section class="welcome">
      <h1>Willkommen bei EchoLearn</h1>
      <p>Starte direkt mit deinen Karteikarten oder sieh dir deinen Lernfortschritt an.</p>
      <ButtonPrimary text="Zum Lernbereich" @click="goToLernbereich" />
    </section>

    <section class="preview">
      <h2>Beispiel-Karteikarten</h2>
      <div class="cards">
        <Card v-for="card in previewCards" :key="card.id" :card="card" />
      </div>
    </section>
  </div>
</template>

<script>
  import { useRouter } from 'vue-router'

  import Card from '../components/Card.vue'
  import ButtonPrimary from '../components/ButtonPrimary.vue'

  export default {
    components: { Card, ButtonPrimary },
    setup() {
      const router = useRouter()

      const previewCards = [
        { id: 1, question: 'Was ist Vue?', answer: 'Ein progressives JS-Framework.' },
        { id: 2, question: 'SCSS oder CSS?', answer: 'SCSS für bessere Struktur.' },
        { id: 3, question: 'Docker nutzen?', answer: 'Ja, für lokales Setup.' }
      ]

      const goToLernbereich = () => {
        router.push('/lernen')
      }

      return { previewCards, goToLernbereich }
    }
  }
</script>
