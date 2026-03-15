<template>
  <header class="header">
    <h1 class="logo">EchoLearn</h1>
    <nav class="nav">
      <router-link to="/" class="link">Home</router-link>
      <router-link to="/pruefung" class="link">Prüfung</router-link>
      <router-link to="/statistik" class="link">Statistik</router-link>
      <router-link to="/verwaltung" class="link admin">Verwaltung</router-link>
    </nav>
  </header>
</template>

<script>
  export default {}
</script>

<style scoped>
  .header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem 2rem;
    background: #fff;
    border-bottom: 1px solid #e5e7eb;
  }

  .logo {
    font-size: 1.4rem;
    font-weight: 600;
    letter-spacing: 0.5px;
  }

  .nav {
    display: flex;
    gap: 1.2rem;
  }

  .link {
    position: relative;
    text-decoration: none;
    color: #374151;
    font-weight: 500;
    padding: 0.4rem 0.6rem;
    transition: color 0.2s ease;
  }

  .link:hover {
    color: #2563eb;
  }

  .router-link-active {
    color: #2563eb;
  }

  .router-link-active::after {
    content: '';
    position: absolute;
    left: 0;
    bottom: -6px;
    width: 100%;
    height: 2px;
    background-color: #2563eb;
    border-radius: 2px;
  }

  .admin {
    font-weight: 600;
  }
</style>
