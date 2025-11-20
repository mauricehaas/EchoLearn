<template>
  <div id="app">
    <Header />

    <main>
      <router-view />
    </main>

    <Footer />
  </div>
</template>

<script>
  import Header from './components/AppHeader.vue'
  import Footer from './components/AppFooter.vue'

  export default {
    components: {
      Header,
      Footer
    }
  }
</script>

<style scoped lang="scss">
  #app {
    display: flex;
    flex-direction: column;
    min-height: 100vh;

    main {
      flex: 1;
      padding: 20px;
    }
  }
</style>
