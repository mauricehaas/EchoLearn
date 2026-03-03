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
    components: { QuestionsTable }
  }
</script>
