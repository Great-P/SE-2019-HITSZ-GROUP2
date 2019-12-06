import Vue from 'vue';
import router from './router/';
import store from './store/';
import './registerServiceWorker';
import './plugins/storage';
import './plugins/vuetify';
import 'roboto-fontface/css/roboto/roboto-fontface.css';
import 'font-awesome/css/font-awesome.css';
import './theme/default.sass';
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
import SlideVerify from 'vue-monoplasty-slide-verify';
import md5 from 'js-md5';
import scroll from 'vue-seamless-scroll'
import VueElementLoading from 'vue-element-loading'

import App from './App.vue';
import vuetify from './plugins/vuetify';

Vue.config.productionTip = false;
Vue.use(ElementUI);
Vue.use(SlideVerify);
Vue.use(scroll);
Vue.component('VueElementLoading', VueElementLoading);
Vue.prototype.$md5 = md5;

const app = new Vue({
  router,
  store,
  vuetify,
  render: h => h(App),
});

app.$mount('#app');
router.beforeEach((to,from,next) => {
  // 如果即将进入的路由对象是登录页，则进行跳转，否则验证是否携带accessToken,如果有，则进
  // 行跳转，没有，则不允许跳转
  if(to.path === "/auth/login"||to.path==="/auth/register")
  {
      next();
  }
  else{
    if (sessionStorage.getItem('token') && sessionStorage.getItem('user'))
    {
        if(to.path === '/userinfo/usermanage')
        {
          if(sessionStorage.getItem('token')===md5(sessionStorage.getItem("user")+'3'))
            next();
          else
          {
            ElementUI.Message.error({
              message: '您不具有权限浏览',
            });
            next("/");
          }
        }
        else if(to.path==="/fileupload")
        {
            if(sessionStorage.getItem('token')===md5(sessionStorage.getItem("user")+'2')||sessionStorage.getItem('token')===md5(sessionStorage.getItem("user")+'3'))
                next();
            else
            {
              ElementUI.Message.error({
                message: '您不具有权限浏览',
              });
              next("/")
            }
        }
        else
        {
           if(sessionStorage.getItem('token')===md5(sessionStorage.getItem("user")+'1')||sessionStorage.getItem('token')===md5(sessionStorage.getItem("user")+'2')||sessionStorage.getItem('token')===md5(sessionStorage.getItem("user")+'3'))
              next();
           else
           {
             ElementUI.Message.error({
               message: '您还未登录',
             });
             setTimeout(() => {
               next("/auth/login");
             }, 1000);
           }
        }
    }
    else
    {
        ElementUI.Message.error({
          message: '您还未登录',
        });
        setTimeout(() => {
            next("/auth/login");
        }, 1000);

    }
  }
});