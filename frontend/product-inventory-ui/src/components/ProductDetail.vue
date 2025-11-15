<template>
  <section v-if="product">
    <h2>{{ product.attributes.name }}</h2>
    <p>{{ product.attributes.description }}</p>
    <p><strong>Precio:</strong> \${{ product.attributes.price.toFixed(2) }}</p>
  </section>
  <p v-else>Selecciona un producto.</p>
</template>

<script setup>
defineProps({
  product: {
    type: Object,
    required: false
  }
})
</script>
