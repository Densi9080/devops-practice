<script setup>
import { ref, onMounted } from 'vue'
import { getGenres, createGenre as apiCreateGenre} from '../api'

const genres = ref([])
const loading = ref(false)
const error = ref('')
const form = ref({ name: ''})
const orderError = ref('')
const orderSuccess = ref(false)

function resetForm() {
  form.value = { name: ''}
}
async function load() {
  loading.value = true
  error.value = ''
  try {
    const [g] = await Promise.all([getGenres()])
    genres.value = g.data.results ?? g.data
  } catch (e) {
    error.value = 'Ошибка загрузки: ' + e.message
  } finally {
    loading.value = false
  }
}

async function create() {
  try {
    await apiCreateGenre(form.value)
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
    <h2>Список жанров</h2>

    <form class="book-form" @submit.prevent="create()">
      <h3>Добавить жанр</h3>
      <input v-model="form.name" placeholder="Название" required />
      <button type="submit">Сохранить</button>
    </form>

    <p v-if="loading">Загрузка…</p>
    <p v-else-if="error" class="error">{{ error }}</p>

    <div v-else class="grid">
      <article v-for="g in genres" :key="g.id" class="card">
        <p class="card-author">{{ g.name || 'Без названия' }}</p>
      </article>
    </div>
  </div>
</template>
<style scoped>
</style>
