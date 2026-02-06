

const routes = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '', component: () => import('pages/IndexPage.vue') },
      //{ path: 'faelle', component: () => import('pages/FallListPage.vue') },
      { path: 'faelle/neu', component: () => import('pages/FallCreatePage.vue') }
    ]
  }
]

export default routes
