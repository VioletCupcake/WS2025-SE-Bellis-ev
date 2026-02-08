const routes = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      // Home / Fall list
      { path: '', component: () => import('pages/IndexPage.vue') },
      { path: '/faelle', component: () => import('pages/FallListPage.vue') },

      // Fall create / detail / edit / close / delete
       { path: 'faelle/neu', component: () => import('pages/FallCreatePage.vue') },
      //  { path: 'faelle/:fallId', component: () => import('pages/FallDetailPage.vue') },
       { path: 'faelle/:fallId/edit', component: () => import('pages/FallEditPage.vue') },
      // { path: 'faelle/:fallId/close', component: () => import('pages/FallClosePage.vue') },
      // { path: 'faelle/:fallId/delete', component: () => import('pages/FallDeletePage.vue') },

      // Beratung (counseling sessions) inside Fall
      { path: 'faelle/:fallId/beratung/add', component: () => import('pages/BeratungCreatePage.vue') },
      // { path: 'beratung/:beratungId/edit', component: () => import('pages/BeratungEditPage.vue') },
      // { path: 'beratung/:beratungId/delete', component: () => import('pages/BeratungDeletePage.vue') },

      // Gewalttat (violence incidents) inside Fall
      { path: 'faelle/:fallId/gewalttat/add', component: () => import('pages/FallGewaltCreatePage.vue') },
      // { path: 'gewalttat/:gewalttatId/edit', component: () => import('pages/FallGewaltEditPage.vue') },
      // { path: 'gewalttat/:gewalttatId/delete', component: () => import('pages/FallGewaltDeletePage.vue') },

      // Folgen der Gewalt (consequences)
      { path: 'faelle/:fallId/folgen/add', component: () => import('pages/FallFolgeCreatePage.vue') },
      // { path: 'folgen/:folgenId/edit', component: () => import('pages/FallFolgeEditPage.vue') },
      // { path: 'folgen/:folgenId/delete', component: () => import('pages/FallFolgeDeletePage.vue') },

      // Neue Anfrage
      { path: 'anfragen/neu', component: () => import('pages/AnfrageCreatePage.vue') },
    ]
  }
]

export default routes
