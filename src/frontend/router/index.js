import { createRouter, createWebHistory } from 'vue-router'
import Home from '../pages/Home.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  // Add your new route here 👇
  {
    path: '/giftmuse-result',
    name: 'GiftMuseResult',
    component: () => import('../pages/GiftMuseResult.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
