<template>
  <header>
    <h1>EchoLearn</h1>
    <nav>
      <router-link to="/">Home</router-link>
      <router-link to="/pruefung">Prüfungsbereich</router-link>
      <router-link to="/verwaltung">Verwaltung</router-link>
      <router-link to="/statistik">Statistik</router-link>
    </nav>
  </header>
</template>

<script>
  export default {}
</script>

<style scoped>
  header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px 20px;
    background-color: #f5f5f5;
    border-bottom: 1px solid #333;
  }

  nav a {
    margin-left: 10px;
    text-decoration: none;
    color: #333;
  }
</style>
