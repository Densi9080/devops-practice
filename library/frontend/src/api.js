import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api/',
})

export default api
export function getBooks() {
  return api.get('books/')
}
export function getBook(id) {
  return api.get(`books/${id}/`)
}
export function getGenres() {
  return api.get('genres/')
}
export function getReviews(bookId) {
  return api.get('reviews/', { params: { book: bookId } })
}
export function getAuthors() {
  return api.get('authors/')
}
export function getOrders() {
  return api.get('orders/')
}
export async function createBook(data) {
  return api.post('books/', data)
}
export async function deleteBook(id) {
  return api.delete(`books/${id}/`)
}
export async function updateBook(id, data) {
  return api.patch(`books/${id}/`, data)
}
export async function createReview(data) {
  return api.post('reviews/', data)
}
export async function createOrder(userId, bookId) {
  const { data } = await api.post('orders/', {
    user: userId,
    book: bookId,
    status: 'new',
  })
  return data
}
export async function createAuthor(data) {
  const { data: created } = await api.post('authors/', data)
  return created
}

export async function createGenre(data) {
  const { data: created } = await api.post('genres/', data)
  return created
}