<script setup>
import { ref, onMounted } from 'vue'
import { getAuthors, createAuthor as apiCreateAuthor} from '../api'

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
    const [a] = await Promise.all([getAuthors()])
    authors.value = a.data.results ?? a.data
  } catch (e) {
    error.value = 'Ошибка загрузки: ' + e.message
  } finally {
    loading.value = false
  }
}

async function create() {
  try {
    await apiCreateAuthor(form.value)
    resetForm()
    await load()
  } catch (e) {
    error.value = 'Ошибка создания: ' + JSON.stringify(e.response?.data ?? e.message)
  }
}
onMounted(load)
</script>


<template>
  <div class="catalog">
    <h2>Список авторов</h2>

    <form class="book-form" @submit.prevent="create()">
      <h3>Добавить автора</h3>
      <input v-model="form.name" placeholder="ФИО" required />
      <input v-model="form.bio" placeholder="Биография" />
      <input v-model.number="form.birth_year" type="number" placeholder="Год рождения" />
      <button type="submit">Сохранить</button>
    </form>

    <p v-if="loading">Загрузка…</p>
    <p v-else-if="error" class="error">{{ error }}</p>

    <div v-else class="grid">
      <article v-for="a in authors" :key="a.id" class="card">
        <p class="card-author">{{ a.name || 'Без автора' }}</p>
        <p class="card-author">{{ a.bio || 'Без биографии' }}</p>
        <p class="card-author">{{ a.birth_year || 'Без года рождения' }}</p>
      </article>
    </div>
  </div>
</template>
<style scoped>
</style>