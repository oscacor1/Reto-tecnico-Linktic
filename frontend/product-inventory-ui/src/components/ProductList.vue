<template>
  <section>
    <header class="list-header">
      <h2>Productos</h2>
      <div class="pagination">
        <button :disabled="page === 1 || loading" @click="prevPage">Anterior</button>
        <span>Página {{ page }}</span>
        <button :disabled="!hasMore || loading" @click="nextPage">Siguiente</button>
      </div>
    </header>

    <p v-if="error" class="error">{{ error }}</p>
    <p v-if="loading">Cargando productos...</p>

    <ul v-if="!loading && products.length">
      <li
        v-for="p in products"
        :key="p.id"
        @click="$emit('select', p.id)"
        class="product-item"
      >
        <strong>{{ p.attributes.name }}</strong>
        <span>\${{ p.attributes.price.toFixed(2) }}</span>
      </li>
    </ul>
    <p v-else-if="!loading">No hay productos.</p>
  </section>
</template>

<script setup>
import { ref, watchEffect } from 'vue'
import { listProducts } from '../api/client'

const emit = defineEmits(['select'])

const products = ref([])
const loading = ref(false)
const error = ref('')
const page = ref(1)
const size = ref(5)
const hasMore = ref(false)

async function load() {
  loading.value = true
  error.value = ''
  try {
    const data = await listProducts(page.value, size.value)
    products.value = data.data || []
    const total = data.meta?.total ?? products.value.length
    hasMore.value = page.value * size.value < total
  } catch (err) {
    console.error(err)
    error.value = 'No fue posible cargar los productos.'
  } finally {
    loading.value = false
  }
}

function nextPage() {
  page.value += 1
  load()
}

function prevPage() {
  if (page.value > 1) {
    page.value -= 1
    load()
  }
}

watchEffect(load)
</script>

<style scoped>
.list-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1rem;
}
.pagination button {
  margin: 0 0.25rem;
}
.product-item {
  display: flex;
  justify-content: space-between;
  padding: 0.5rem 0.75rem;
  margin-bottom: 0.5rem;
  background: #ffffff;
  border-radius: 0.375rem;
  cursor: pointer;
}
.product-item:hover {
  background: #e5e7eb;
}
.error {
  color: #b91c1c;
}
</style>
