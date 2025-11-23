<template>
  <div>
    <h2>Questions</h2>
    <table border="1">
      <thead>
        <tr>
          <th>ID</th>
          <th>Question</th>
          <th>Answer</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="q in questions" :key="q.id">
          <td>{{ q.id }}</td>
          <td>{{ q.question }}</td>
          <td>{{ q.answer }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
  import { ref, onMounted } from 'vue'

  export default {
    setup() {
      const questions = ref([])

      onMounted(async () => {
        const res = await fetch('http://localhost:8000/questions/')
        questions.value = await res.json()
      })

      return { questions }
    }
  }
</script>
