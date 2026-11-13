<template>
  <div class="orders">
    <h2>Мои заказы</h2>

    <p v-if="loading">Загрузка…</p>
    <p v-else-if="error" class="error">{{ error }}</p>
    <p v-else-if="!orders.length" class="empty">Заказов пока нет</p>

    <ul v-else class="order-list">
      <li v-for="o in orders" :key="o.id" class="order-card">
        <div class="order-head">
          <router-link :to="`/books/${o.book}`" class="book-link">
            Книга #{{ o.book }}
          </router-link>
          <span class="status" :class="statusClass(o.status)">
            {{ statusLabel(o.status) }}
          </span>
        </div>
        <p class="meta">
          Количество: <b>{{ o.quantity }}</b>
        </p>
        <p class="meta">
          Создан: {{ formatDate(o.created_at) }}
        </p>
      </li>
    </ul>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getOrders } from '../api'

const orders = ref([])
const loading = ref(false)
const error = ref('')

const STATUS_LABELS = {
  new: 'Новый',
  paid: 'Оплачен',
  shipped: 'Отправлен',
  cancelled: 'Отменён',
}

function statusLabel(status) {
  return STATUS_LABELS[status] || status
}

function statusClass(status) {
  return `status-${status}`
}

function formatDate(value) {
  if (!value) return '—'
  return new Date(value).toLocaleString('ru-RU')
}

async function load() {
  loading.value = true
  error.value = ''
  try {
    const { data } = await getOrders()
    orders.value = data.results ?? data
  } catch (e) {
    error.value = 'Ошибка загрузки: ' + (e.response?.data?.detail ?? e.message)
  } finally {
    loading.value = false
  }
}

onMounted(load)
</script>

<style scoped>
</style>