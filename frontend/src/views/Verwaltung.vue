<template>
  <div class="verwaltung-page">
    <h1>Verwaltung</h1>
    <QuestionsTable />
  </div>
</template>

<script>
  import QuestionsTable from '../components/QuestionsTable.vue'

  export default {
    name: 'Verwaltung',
    components: { QuestionsTable, QuestionsTable }
  }
</script>

<style scoped>
  .verwaltung-page {
    max-width: 800px;
    margin: 20px auto;
    padding: 10px;
  }
</style>
