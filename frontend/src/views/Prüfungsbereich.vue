<template>
  <div class="exam">
    <h1>Prüfungsbereich</h1>
    <Exam />
  </div>
</template>

<script>
  import Exam from '../components/Exam.vue'

  export default {
    name: 'Prüfung',
    components: { Exam }
  }
</script>
