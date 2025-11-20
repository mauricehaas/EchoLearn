<template>
  <div class="card">
    <h3>{{ card.question }}</h3>
    <p>{{ card.answer }}</p>
  </div>
</template>

<script>
  export default {
    name: 'Card',
    props: {
      card: {
        type: Object,
        required: true
      }
    }
  }
</script>

<style scoped lang="scss">
  .card {
    background-color: #f9f9f9;
    border-radius: 8px;
    padding: 20px;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
    width: 250px;
    transition:
      transform 0.2s ease,
      box-shadow 0.2s ease;
    cursor: default;

    h3 {
      font-size: 1.2rem;
      margin-bottom: 10px;
      color: #333;
    }

    p {
      font-size: 1rem;
      color: #555;
    }

    &:hover {
      transform: translateY(-5px);
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    }
  }
</style>
