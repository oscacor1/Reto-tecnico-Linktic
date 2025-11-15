import { mount } from '@vue/test-utils'
import { describe, it, expect, vi, beforeEach } from 'vitest'
import ProductList from '../../../src/components/ProductList.vue'
import * as api from '../../../src/api/client'

describe('ProductList', () => {
  beforeEach(() => {
    vi.restoreAllMocks()
  })

  it('loads and renders products', async () => {
    vi.spyOn(api, 'listProducts').mockResolvedValue({
      data: [
        {
          id: 1,
          attributes: { name: 'Prod 1', price: 10 }
        },
        {
          id: 2,
          attributes: { name: 'Prod 2', price: 20 }
        }
      ],
      meta: { total: 2 }
    })

    const wrapper = mount(ProductList)
    await new Promise(resolve => setTimeout(resolve, 0))

    expect(wrapper.findAll('li.product-item')).toHaveLength(2)
  })

  it('shows error message when api fails', async () => {
    vi.spyOn(api, 'listProducts').mockRejectedValue(new Error('network'))

    const wrapper = mount(ProductList)
    await new Promise(resolve => setTimeout(resolve, 0))

    expect(wrapper.text()).toContain('No fue posible cargar los productos.')
  })
})
