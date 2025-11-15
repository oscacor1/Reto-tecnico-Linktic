<template>
  <main class="container">
    <h1>Productos e Inventario</h1>
    <ProductsView />
  </main>
</template>

<script setup>
import ProductsView from './views/ProductsView.vue'
</script>

<style>
body {
  font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  margin: 0;
  padding: 0;
  background: #f3f4f6;
}
.container {
  max-width: 960px;
  margin: 0 auto;
  padding: 2rem;
}
h1 {
  margin-bottom: 1.5rem;
}
</style>
