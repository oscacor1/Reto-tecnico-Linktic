<template>
  <section v-if="productId">
    <h3>Inventario</h3>
    <p v-if="error" class="error">{{ error }}</p>
    <p v-if="loading">Consultando inventario...</p>
    <p v-if="!loading && !error">Cantidad disponible: {{ quantity }}</p>

    <form @submit.prevent="handlePurchase">
      <label>
        Cantidad a comprar:
        <input type="number" v-model.number="requestQty" min="1" />
      </label>
      <button type="submit" :disabled="loadingPurchase">Comprar</button>
    </form>
    <p v-if="purchaseMsg" class="info">{{ purchaseMsg }}</p>
  </section>
</template>

<script setup>
import { ref, watch } from 'vue'
import { getInventory, purchaseProduct } from '../api/client'

const props = defineProps({
  productId: {
    type: Number,
    required: false
  }
})

const quantity = ref(0)
const loading = ref(false)
const error = ref('')
const requestQty = ref(1)
const loadingPurchase = ref(false)
const purchaseMsg = ref('')

async function loadInventory() {
  if (!props.productId) return
  loading.value = true
  error.value = ''
  try {
    const data = await getInventory(props.productId)
    quantity.value = data.data.attributes.quantity
  } catch (err) {
    console.error(err)
    error.value = 'No fue posible consultar el inventario.'
  } finally {
    loading.value = false
  }
}

async function handlePurchase() {
  if (!props.productId) return
  loadingPurchase.value = true
  purchaseMsg.value = ''
  error.value = ''
  try {
    const data = await purchaseProduct(props.productId, requestQty.value)
    quantity.value = data.data.attributes.quantity
    purchaseMsg.value = 'Compra realizada con éxito.'
  } catch (err) {
    console.error(err)
    const apiError = err.response?.data?.errors?.[0]?.detail
    error.value = apiError || 'No fue posible realizar la compra.'
  } finally {
    loadingPurchase.value = false
  }
}

watch(
  () => props.productId,
  () => {
    purchaseMsg.value = ''
    requestQty.value = 1
    loadInventory()
  },
  { immediate: true }
)
</script>

<style scoped>
.error {
  color: #b91c1c;
}
.info {
  color: #047857;
}
form {
  margin-top: 0.5rem;
  display: flex;
  gap: 0.5rem;
  align-items: center;
}
input {
  width: 4rem;
}
</style>
