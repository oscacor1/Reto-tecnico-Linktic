<template>
  <div class="layout">
    <div class="column">
      <ProductList @select="handleSelect" />
    </div>
    <div class="column detail-column">
      <ProductDetail :product="selectedProduct" />
      <InventoryInfo v-if="selectedId" :product-id="selectedId" />
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import ProductList from '../components/ProductList.vue'
import ProductDetail from '../components/ProductDetail.vue'
import InventoryInfo from '../components/InventoryInfo.vue'
import { getProduct } from '../api/client'

const selectedId = ref(null)
const selectedProduct = ref(null)

function handleSelect(id) {
  selectedId.value = Number(id)
}

watch(
  () => selectedId.value,
  async (value) => {
    if (!value) {
      selectedProduct.value = null
      return
    }
    try {
      const data = await getProduct(value)
      selectedProduct.value = data.data
    } catch (err) {
      console.error(err)
      selectedProduct.value = null
    }
  }
)
</script>

<style scoped>
.layout {
  display: grid;
  grid-template-columns: 1fr 1.2fr;
  gap: 1.5rem;
}
.detail-column {
  background: #ffffff;
  border-radius: 0.5rem;
  padding: 1rem;
}
</style>
