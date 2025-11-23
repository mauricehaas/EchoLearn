<template>
  <div class="table-container">
    <h2>Questions</h2>

    <!-- Modal -->
    <div v-if="editing" class="modal-backdrop">
      <div class="modal-content">
        <h3>Edit Question #{{ editForm.id }}</h3>

        <label>Frage:</label>
        <input v-model="editForm.question" />

        <label>Antwort:</label>
        <input v-model="editForm.answer" />

        <div class="modal-buttons">
          <button class="primary" @click="saveEdit" type="button">Save</button>
          <button class="cancel" @click="cancelEdit" type="button">Cancel</button>
        </div>
      </div>
    </div>

    <!-- Tabelle -->
    <table>
      <thead>
        <tr>
          <th>ID</th>
          <th>Frage</th>
          <th>Antwort</th>
          <th>Aktionen</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="q in paginatedQuestions" :key="q.id">
          <td>{{ q.id }}</td>
          <td>{{ q.question }}</td>
          <td>{{ q.answer }}</td>
          <td class="actions">
            <button @click="startEdit(q)" class="edit" type="button">Bearbeiten</button>
            <button @click="deleteQuestion(q.id)" class="delete" type="button">Löschen</button>
          </td>
        </tr>
      </tbody>
    </table>

    <!-- Pagination -->
    <div class="pagination">
      <button @click="prevPage" :disabled="currentPage === 1" type="button">Prev</button>
      <span>Page {{ currentPage }} of {{ totalPages }}</span>
      <button @click="nextPage" :disabled="currentPage === totalPages" type="button">Next</button>
    </div>
  </div>
</template>

<script>
  import { ref, computed, onMounted } from 'vue'

  export default {
    setup() {
      const questions = ref([])
      const currentPage = ref(1)
      const perPage = 10

      const editing = ref(false)
      const editForm = ref({ id: null, question: '', answer: '' })

      // Fragen laden
      async function loadQuestions() {
        const res = await fetch('http://localhost:8000/questions/')
        questions.value = await res.json()
      }

      onMounted(loadQuestions)

      // Pagination
      const totalPages = computed(() => Math.ceil(questions.value.length / perPage))

      const paginatedQuestions = computed(() => {
        const start = (currentPage.value - 1) * perPage
        return questions.value.slice(start, start + perPage)
      })

      const nextPage = () => {
        if (currentPage.value < totalPages.value) currentPage.value++
      }

      const prevPage = () => {
        if (currentPage.value > 1) currentPage.value--
      }

      // DELETE
      const deleteQuestion = async (id) => {
        await fetch(`http://localhost:8000/questions/${id}`, {
          method: 'DELETE'
        })

        await loadQuestions() // Liste neu laden
      }

      // EDIT START
      const startEdit = (q) => {
        editing.value = true
        editForm.value = { ...q }
      }

      const cancelEdit = () => {
        editing.value = false
      }

      // SAVE EDIT → PATCH
      const saveEdit = async () => {
        await fetch(`http://localhost:8000/questions/${editForm.value.id}`, {
          method: 'PATCH',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            question: editForm.value.question,
            answer: editForm.value.answer
          })
        })

        editing.value = false
        await loadQuestions() // Liste aktualisieren
      }

      return {
        questions,
        currentPage,
        totalPages,
        paginatedQuestions,
        nextPage,
        prevPage,

        editing,
        editForm,
        startEdit,
        saveEdit,
        cancelEdit,
        deleteQuestion
      }
    }
  }
</script>
