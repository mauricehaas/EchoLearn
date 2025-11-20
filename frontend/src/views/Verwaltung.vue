<template>
  <div class="verwaltung-page">
    <h1>Karteikarten-Verwaltung</h1>
    <CardForm @card-added="reloadCards" />
    <CardList ref="cardList" />
  </div>
</template>

<script>
  import CardForm from '../components/CardForm.vue'
  import CardList from '../components/CardList.vue'

  export default {
    name: 'Verwaltung',
    components: { CardForm, CardList },
    methods: {
      reloadCards() {
        this.$refs.cardList.fetchCards()
      }
    }
  }
</script>

<style scoped>
  .verwaltung-page {
    max-width: 800px;
    margin: 20px auto;
    padding: 10px;
  }
</style>
