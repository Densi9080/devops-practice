<template>
  <div style="max-width:900px;margin:0 auto;padding:20px;font-family:sans-serif">
    <h1>Онлайн библиотека</h1>
    <nav style="margin-bottom:16px">
      <router-link to="/">Каталог</router-link>
      <router-link to="/orders">Заказы</router-link>
      <router-link to="/authors">Авторы</router-link>
      <router-link to="/genres">Жанры</router-link>
    </nav>
    <router-view />
  </div>
</template>
