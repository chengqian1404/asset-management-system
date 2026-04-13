// 路由配置
import { createRouter, createWebHistory } from 'vue-router'
import { storage } from '../utils/storage'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('../pages/login/Login.vue'),
    meta: { requiresAuth: false, title: '登录' },
  },
  {
    path: '/',
    component: () => import('../components/layout/AdminLayout.vue'),
    meta: { requiresAuth: true },
    children: [
      {
        path: '',
        redirect: '/dashboard',
      },
      {
        path: 'dashboard',
        name: 'Dashboard',
        component: () => import('../pages/dashboard/Dashboard.vue'),
        meta: { title: '仪表板' },
      },
      {
        path: 'assets',
        name: 'AssetList',
        component: () => import('../pages/asset/AssetList.vue'),
        meta: { title: '资产列表' },
      },
      {
        path: 'assets/add',
        name: 'AssetAdd',
        component: () => import('../pages/asset/AssetAdd.vue'),
        meta: { title: '新增资产' },
      },
      {
        path: 'assets/:id/edit',
        name: 'AssetEdit',
        component: () => import('../pages/asset/AssetEdit.vue'),
        meta: { title: '编辑资产' },
      },
      {
        path: 'assets/:id',
        name: 'AssetDetail',
        component: () => import('../pages/asset/AssetDetail.vue'),
        meta: { title: '资产详情' },
      },
      {
        path: 'categories',
        name: 'CategoryList',
        component: () => import('../pages/category/CategoryList.vue'),
        meta: { title: '分类管理' },
      },
      {
        path: 'borrows',
        name: 'BorrowList',
        component: () => import('../pages/borrow/BorrowList.vue'),
        meta: { title: '借用管理' },
      },
      {
        path: 'borrows/add',
        name: 'BorrowAdd',
        component: () => import('../pages/borrow/BorrowAdd.vue'),
        meta: { title: '申请借用' },
      },
      {
        path: 'users',
        name: 'UserList',
        component: () => import('../pages/user/UserList.vue'),
        meta: { title: '用户管理', requiresAdmin: true },
      },
      {
        path: 'settings',
        name: 'Settings',
        component: () => import('../pages/settings/Settings.vue'),
        meta: { title: '系统设置', requiresAdmin: true },
      },
    ],
  },
  {
    path: '/:pathMatch(.*)*',
    redirect: '/dashboard',
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

// 路由守卫
router.beforeEach((to, from, next) => {
  const token = storage.getToken()
  const requiresAuth = to.meta.requiresAuth !== false

  if (requiresAuth && !token) {
    next('/login')
  } else if (to.path === '/login' && token) {
    next('/dashboard')
  } else {
    document.title = `${to.meta.title || '资产管理'} - 资产管理系统`
    next()
  }
})

export default router
