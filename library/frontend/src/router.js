import { createRouter, createWebHistory } from 'vue-router'
import BooksView from './views/BooksView.vue'
import BookDetailView from './views/BookDetailView.vue'
import OrdersView from './views/OrdersView.vue'

export default createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: BooksView },
    { path: '/books/:id', component: BookDetailView, props: true },
    { path: '/orders', component:  OrdersView},
  ],
})
