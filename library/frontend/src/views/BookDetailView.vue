<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { getBook, getReviews, updateBook, createReview, createOrder } from '../api'

const props = defineProps({ id: String })
const route = useRoute()

const book = ref(null)
const reviews = ref([])
const editForm = ref({ title: '', price: 0 })
const reviewForm = ref({ rating: 5, text: '' })
const editError = ref('')
const reviewError = ref('')
const orderError=ref('')
const orderSuccess=ref(null)
function currentBookId() {
  return props.id || route.params.id
}

async function load() {
  const bookId = currentBookId()
  try {
    const [b, r] = await Promise.all([getBook(bookId), getReviews(bookId)])
    book.value = b.data
    reviews.value = r.data.results ?? r.data
    editForm.value = { title: b.data.title, price: b.data.price }
  } catch (e) {
    console.error(e)
  }
}

async function saveBook() {
  editError.value = ''
  try {
    await updateBook(book.value.id, editForm.value)
    await load()
  } catch (e) {
    editError.value = 'Ошибка сохранения: ' + JSON.stringify(e.response?.data ?? e.message)
  }
}

async function addReview() {
  reviewError.value = ''
  try {
    await createReview({
      book: book.value.id,
      rating: reviewForm.value.rating,
      text: reviewForm.value.text,
    })
    reviewForm.value = { rating: 5, text: '' }
    await load()
  } catch (e) {
    reviewError.value = 'Ошибка отзыва: ' + JSON.stringify(e.response?.data ?? e.message)
  }
}

async function orderBook() {
  orderError.value = ''
  orderSuccess.value = false
  const userId = 1
  const bookId = route.params.id

  try {
    await createOrder(userId, bookId)
    orderSuccess.value = true
  } catch (e) {
    orderError.value = 'Ошибка заказа: ' + JSON.stringify(e.response?.data ?? e.message)
  }
}
onMounted(load)
</script>
<template>
  <div class="detail">
    <router-link to="/" class="back">← Назад</router-link>

    <div v-if="book">
      <h2>{{ book.title }}</h2>
      <p><b>Автор:</b> {{ book.author?.name || '—' }}</p>
      <p><b>Год:</b> {{ book.year || '—' }}</p>
      <p><b>Цена:</b> {{ book.price }} ₽</p>
      <p v-if="book.description">{{ book.description }}</p>
      <button @click="orderBook()">Заказать</button>

      <details class="edit-block">
        <summary>Редактировать</summary>
        <form class="inline-form" @submit.prevent="saveBook">
          <input v-model="editForm.title" placeholder="Название" />
          <input v-model.number="editForm.price" type="number" step="0.01" placeholder="Цена" />
          <button type="submit">Сохранить</button>
        </form>
        <p v-if="editError" class="error">{{ editError }}</p>
      </details>

      <h3>Отзывы</h3>
      <form class="inline-form" @submit.prevent="addReview">
        <input
          v-model.number="reviewForm.rating"
          type="number"
          min="1"
          max="5"
          placeholder="Оценка"
        />
        <input v-model="reviewForm.text" placeholder="Текст отзыва" />
        <button type="submit">Оставить отзыв</button>
      </form>
      <p v-if="reviewError" class="error">{{ reviewError }}</p>

      <ul class="reviews">
        <li v-for="r in reviews" :key="r.id">
          ⭐ {{ r.rating }} — {{ r.text }} <span class="user">({{ r.user }})</span>
        </li>
        <li v-if="!reviews.length" class="empty">Пока нет отзывов</li>
      </ul>
    </div>
    <p v-else>Загрузка…</p>
  </div>
</template>
<style scoped>
</style>