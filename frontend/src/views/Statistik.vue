<template>
  <div class="statistik">
    <h1>Statistik</h1>
    <ExamStats />
  </div>
</template>

<script>
  import ExamStats from '../components/ExamStats.vue'

  export default {
    name: 'Statistik',
    components: { ExamStats }
  }
</script>
