<template>
  <footer class="app-footer">
    <p>&copy; 2025 EchoLearn.</p>
    <nav>
      <a href="#">Impressum</a> |
      <a href="#">Datenschutz</a>
    </nav>
  </footer>
</template>

<script>
  export default {}
</script>

<style scoped>
  .app-footer {
    text-align: center;
    padding: 15px 20px;
    background-color: #f5f5f5;
    color: #555;
    font-size: 0.9rem;
    border-top: 1px solid #ddd;
    margin-top: 40px;
  }

  .app-footer a {
    color: #555;
    text-decoration: none;
    margin: 0 5px;
  }

  .app-footer a:hover {
    text-decoration: underline;
  }
</style>
