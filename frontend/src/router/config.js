import { AuthLayout, DefaultLayout, ChatLayout } from '@/components/layouts'

export const publicRoute = [
  {
    path: '*',
    component: () =>
      import(/* webpackChunkName: "errors-404" */ '@/views/error/NotFound.vue'),
  },
  {
    path: '/auth',
    component: AuthLayout,
    meta: {
      title: 'Login',
    },
    redirect: '/auth/login',
    hidden: true,
    children: [
      {
        path: 'login',
        name: 'login',
        meta: {
          title: 'Login',
        },
        component: () =>
          import(/* webpackChunkName: "login" */ '@/views/auth/Login.vue'),
      },
      {
        path: 'register',
        name: 'register',
        meta: {
          title: 'register',
        },
        component: () =>
          import(/* webpackChunkName: "login" */ '@/views/auth/register.vue'),
      },
    ],
  },

  {
    path: '/login',
    redirect:'/auth/login',
  },
  {
    path: '/404',
    name: '404',
    meta: {
      title: 'Not Found',
    },
    component: () =>
      import(/* webpackChunkName: "errors-404" */ '@/views/error/NotFound.vue'),
  },
  {
    path: '/500',
    name: '500',
    meta: {
      title: 'Server Error',
    },
    component: () =>
      import(/* webpackChunkName: "errors-500" */ '@/views/error/Error.vue'),
  },
];

export const protectedRoute = [
  {
    path: '/',
    component: DefaultLayout,
    meta: {
      title: 'Home',
      group: 'apps',
      icon: '',
    },
    redirect: '/dashboard',
    children: [
      {
        path: '/dashboard',
        name: 'Dashboard',
        meta: {
          title: 'Home',
          group: 'apps',
          icon: 'dashboard',
        },
        component: () =>
          import(/* webpackChunkName: "dashboard" */ '@/views/Dashboard.vue'),
      },
      {
        path: '/fileupload',
        meta: {
          title: '文件上传',
          group: 'apps',
          icon: 'media',
        },
        name: 'Media',
        props: route => ({
          type: route.query.type,
        }),
        component: () =>
          import(/* webpackChunkName: "media" */ '@/views/FileUpload.vue'),
      },


      {
        path: '/403',
        name: 'Forbidden',
        meta: {
          title: 'Access Denied',
          hiddenInMenu: true,
        },
        component: () =>
          import(/* webpackChunkName: "error-403" */ '@/views/error/Deny.vue'),
      },
    ],
  },

  //list
  {
    path: '/userinfo',
    component: DefaultLayout,
    redirect: '/userinfo/usermanage',
    meta: {
      title: '用户管理',
      icon: 'view_compact',
      group: 'cms',
    },
    children: [
      {
        path: '/userinfo/usermanage',
        name: 'ListTable',
        meta: {
          title: '用户数据',
        },
        component: () =>
          import(/* webpackChunkName: "table" */ '@/views/list/Table.vue'),
      },
      {
        path: '/userinfo/userinfo',
        name: 'userinfo',
        meta: {
          title: '个人信息',
        },
        component: () =>
          import(/* webpackChunkName: "table" */ '@/views/list/userinfo.vue'),
      },
    ],
  },

  //widgets
  {
    path: '/widgets',
    component: DefaultLayout,
    meta: {
      title: 'Widget',
      icon: 'widgets',
      group: 'advance',
    },
    redirect: '/widgets/chart',
    children: [
      {
        path: '/widgets/func3',
        name: '民生事件结办情况',
        meta: {
          title: '民生事件结办情况',
        },
        component: () =>
          import(/* webpackChunkName: "chart-widget" */ '@/views/widgets/NewNestedPie.vue'),
      },
      {
        path: '/widgets/func4',
        name: '热点社区分析',
        meta: {
          title: '热点社区分析',
        },
        component: () =>
          import(/* webpackChunkName: "list-widget" */ '@/views/widgets/MapUse.vue'),
      },
      {
        path: '/widgets/func1',
        name: '民生事件性质分类',
        meta: {
          title: '民生事件性质分类',
        },
        component: () =>
          import(/* webpackChunkName: "social-widget" */ '@/views/widgets/SpecialPieChartUse.vue'),
      },
      {
        path: '/widgets/func2',
        name: '街道民生事件结办情况',
        meta: {
          title: '街道民生事件结办情况',
        },
        component: () =>
          import(/* webpackChunkName: "statistic-widget" */ '@/views/widgets/StackedBarUse.vue'),
      },
      {
        path: '/widgets/func5',
        name: '滚动事件报警',
        meta: {
          title: '滚动事件报警',
        },
        component: () =>
          import(/* webpackChunkName: "statistic-widget" */ '@/views/widgets/ScrollPage.vue'),
      },
      {
        path: '/widgets/func6',
        name: '时间线概览',
        meta: {
          title: '时间线概览',
        },
        component: () =>
          import(/* webpackChunkName: "statistic-widget" */ '@/views/widgets/TimelineChart.vue'),
      },
    ],
  },


];
