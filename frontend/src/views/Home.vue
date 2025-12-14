<template>
  <div class="home">
    <section class="welcome">
      <h1>Willkommen bei EchoLearn</h1>
      <p>Starte direkt mit einer Prüfung oder sieh dir deinen Lernfortschritt an.</p>
    </section>

    <section class="actions">
      <router-link to="/pruefung" class="card">
        <h2>📝 Prüfung starten</h2>
        <p>Teste dein Wissen mit einer neuen Prüfung.</p>
      </router-link>

      <router-link to="/statistik" class="card">
        <h2>📊 Statistik</h2>
        <p>Sieh dir deinen Lernfortschritt und Bewertungen an.</p>
      </router-link>
    </section>
  </div>
</template>

<style scoped>
  .home {
    max-width: 900px;
    margin: 0 auto;
    padding: 2rem;
  }

  .welcome {
    text-align: center;
    margin-bottom: 3rem;
  }

  .actions {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
    gap: 1.5rem;
  }

  .card {
    display: block;
    padding: 1.5rem;
    border-radius: 12px;
    background: #ffffff;
    text-decoration: none;
    color: inherit;
    box-shadow: 0 6px 16px rgba(0, 0, 0, 0.08);
    transition:
      transform 0.2s ease,
      box-shadow 0.2s ease;
  }

  .card:hover {
    transform: translateY(-4px);
    box-shadow: 0 10px 24px rgba(0, 0, 0, 0.12);
  }

  .card h2 {
    margin-bottom: 0.5rem;
  }
</style>
