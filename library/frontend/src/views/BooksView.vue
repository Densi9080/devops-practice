<script setup>
import { ref, onMounted } from 'vue'
import { getBooks, getAuthors, createBook as apiCreateBook, deleteBook} from '../api'

const books = ref([])
const authors = ref([])
const loading = ref(false)
const error = ref('')
const form = ref({ title: '', price: 0, year: null, author_id: '' })
const orderError = ref('')
const orderSuccess = ref(false)

function resetForm() {
  form.value = { title: '', price: 0, year: null, author_id: '' }
}
async function load() {
  loading.value = true
  error.value = ''
  try {
    const [b, a] = await Promise.all([getBooks(), getAuthors()])
    books.value = b.data.results ?? b.data
    authors.value = a.data.results ?? a.data
  } catch (e) {
    error.value = 'Ошибка загрузки: ' + e.message
  } finally {
    loading.value = false
  }
}

async function createBook() {
  try {
    await apiCreateBook(form.value)
    resetForm()
    await load()
  } catch (e) {
    error.value = 'Ошибка создания: ' + JSON.stringify(e.response?.data ?? e.message)
  }
}

async function removeBook(id) {
  if (!confirm('Удалить книгу?')) return
  try {
    await deleteBook(id)
    await load()
  } catch (e) {
    error.value = 'Ошибка удаления: ' + e.message
  }
}

onMounted(load)
</script>

<template>
  <div class="catalog">
    <h2>Каталог книг</h2>

    <form class="book-form" @submit.prevent="createBook">
      <h3>Добавить книгу</h3>
      <input v-model="form.title" placeholder="Название" required />
      <input v-model.number="form.price" type="number" step="0.01" placeholder="Цена" />
      <input v-model.number="form.year" type="number" placeholder="Год" />
      <select v-model="form.author_id" required>
        <option disabled value="">Автор…</option>
        <option v-for="a in authors" :key="a.id" :value="a.id">{{ a.name }}</option>
      </select>
      <button type="submit">Сохранить</button>
    </form>

    <p v-if="loading">Загрузка…</p>
    <p v-else-if="error" class="error">{{ error }}</p>

    <div v-else class="grid">
      <article v-for="b in books" :key="b.id" class="card">
        <router-link :to="`/books/${b.id}`" class="card-title">
          {{ b.title }}
        </router-link>
        <p class="card-author">{{ b.author?.name || 'Без автора' }}</p>
        <p class="card-meta">
          <span>{{ b.year || '—' }}</span>
          <span class="price">{{ b.price }} ₽</span>
        </p>
        <button class="btn-delete" @click="removeBook(b.id)">Удалить</button>
      </article>
    </div>
  </div>
</template>
<style scoped>
</style>