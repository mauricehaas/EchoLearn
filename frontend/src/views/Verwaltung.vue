<template>
  <div class="verwaltung-page">
    <h1>Verwaltung</h1>
    <QuestionsTable />
    <UsersTable />
  </div>
</template>

<script>
  import QuestionsTable from '../components/QuestionsTable.vue'
  import UsersTable from '../components/UsersTable.vue'

  export default {
    name: 'Verwaltung',
    components: { QuestionsTable, UsersTable }
  }
</script>
