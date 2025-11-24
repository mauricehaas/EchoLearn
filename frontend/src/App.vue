<template>
  <div id="app-container">
    <AppHeader />

    <main>
      <router-view />
    </main>

    <AppFooter />
  </div>
</template>

<script>
  import AppHeader from './components/AppHeader.vue'
  import AppFooter from './components/AppFooter.vue'

  export default {
    components: {
      AppHeader,
      AppFooter
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
