<template>
  <div class="stats">
    <h1>Statistik</h1>
    <StatsTable />
  </div>
</template>

<script>
  import StatsTable from '../components/StatsTable.vue'

  export default {
    name: 'Statistik',
    components: { StatsTable }
  }
</script>
