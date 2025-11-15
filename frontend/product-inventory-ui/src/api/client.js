import axios from 'axios'

const apiBaseUrl = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8001'
const inventoryBaseUrl = import.meta.env.VITE_INVENTORY_BASE_URL || 'http://localhost:8002'
const apiKey = import.meta.env.VITE_API_KEY || 'super-secret-key'

const http = axios.create({
  headers: {
    'X-API-Key': apiKey,
    'Accept': 'application/vnd.api+json',
    'Content-Type': 'application/vnd.api+json'
  }
})

export async function listProducts(page = 1, size = 10) {
  const resp = await http.get(`${apiBaseUrl}/api/v1/products`, {
    params: {
      'page[number]': page,
      'page[size]': size
    }
  })
  return resp.data
}

export async function getProduct(id) {
  const resp = await http.get(`${apiBaseUrl}/api/v1/products/${id}`)
  return resp.data
}

export async function getInventory(productId) {
  const resp = await http.get(`${inventoryBaseUrl}/api/v1/inventory/${productId}`)
  return resp.data
}

export async function purchaseProduct(productId, quantity) {
  const payload = {
    data: {
      type: 'purchases',
      attributes: { quantity }
    }
  }
  const resp = await http.post(`${inventoryBaseUrl}/api/v1/inventory/${productId}/purchase`, payload)
  return resp.data
}
