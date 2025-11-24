<template>
  <div class="table-container">
    <h2>Users</h2>
    <table>
      <thead>
        <tr>
          <th>ID</th>
          <th>Username</th>
          <th>Rolle</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="u in paginatedUsers" :key="u.id">
          <td>{{ u.id }}</td>
          <td>{{ u.username }}</td>
          <td>{{ u.role }}</td>
        </tr>
      </tbody>
    </table>

    <!-- Pagination Controls -->
    <div class="pagination">
      <button @click="prevPage" :disabled="currentPage === 1">Prev</button>
      <span>Page {{ currentPage }} of {{ totalPages }}</span>
      <button @click="nextPage" :disabled="currentPage === totalPages">Next</button>
    </div>
  </div>
</template>

<script>
  import { ref, computed, onMounted } from 'vue'

  export default {
    setup() {
      const users = ref([])
      const currentPage = ref(1)
      const perPage = 5 // Anzahl der User pro Seite

      onMounted(async () => {
        const res = await fetch('http://localhost:8000/users/')
        users.value = await res.json()
      })

      const totalPages = computed(() => Math.ceil(users.value.length / perPage))

      const paginatedUsers = computed(() => {
        const start = (currentPage.value - 1) * perPage
        return users.value.slice(start, start + perPage)
      })

      const nextPage = () => {
        if (currentPage.value < totalPages.value) currentPage.value++
      }

      const prevPage = () => {
        if (currentPage.value > 1) currentPage.value--
      }

      return { users, currentPage, totalPages, paginatedUsers, nextPage, prevPage }
    }
  }
</script>
