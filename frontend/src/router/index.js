import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Lernbereich from '../views/Lernbereich.vue'
import Prüfungsbereich from '../views/Prüfungsbereich.vue'
import Verwaltung from '../views/Verwaltung.vue'
import Statistik from '../views/Statistik.vue'

const routes = [
  { path: '/', name: 'Home', component: Home },
  { path: '/lernen', name: 'Lernbereich', component: Lernbereich },
  { path: '/verwaltung', name: 'Verwaltung', component: Verwaltung },
  { path: '/pruefung', name: 'Prüfungsbereich', component: Prüfungsbereich },
  { path: '/statistik', name: 'Statistik', component: Statistik }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
