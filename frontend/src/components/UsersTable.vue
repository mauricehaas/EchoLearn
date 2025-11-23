<template>
  <div>
    <h2>Users</h2>
    <table border="1">
      <thead>
        <tr>
          <th>ID</th>
          <th>Username</th>
          <th>Role</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="u in users" :key="u.id">
          <td>{{ u.id }}</td>
          <td>{{ u.username }}</td>
          <td>{{ u.role }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
  import { ref, onMounted } from 'vue'

  export default {
    setup() {
      const users = ref([])

      onMounted(async () => {
        const res = await fetch('http://localhost:8000/users/')
        users.value = await res.json()
      })

      return { users }
    }
  }
</script>
