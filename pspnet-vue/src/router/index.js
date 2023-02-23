import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import IdentifyView from '../views/IdentifyView.vue'
import UserProfile from '../views/UserProfile.vue'
import AccountSettingsView from '../views/AccountSettingsView.vue'
import GallaryView from '../views/GallaryView.vue'
import JobsView from '../views/JobsView.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/login',
    name: 'login',
    component: LoginView
  },
  {
    path: '/about',
    name: 'about',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
  },
  {
    path: '/register',
    name: 'register',
    component: RegisterView
  },
  {
    path: '/profile',
    name: 'profile',
    component: UserProfile
  },
  {
    path: '/identify',
    name: 'identify',
    component: IdentifyView
  },
  {
    path : '/gallary',
    name : 'gallary',
    component : GallaryView
  },
  {
    path : '/settings',
    name : 'settings',
    component : AccountSettingsView
  },
  {
    path : '/jobs',
    name : 'jobs',
    component : JobsView
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
