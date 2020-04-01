import Vue from 'vue'
import Router from 'vue-router'
import HelloWorld from '@/components/HelloWorld'
import QccSpiderDem from "../components/Spider_Dem/QccSpiderDem";
import SpiderDem from "../components/Spider_Dem/SpiderDem";

Vue.use(Router)

export default new Router({
  mode:'history',
  routes: [
    {
      path: '/',
      name: 'HelloWorld',
      component: HelloWorld,
      children:[
        {
          path:'/Spider',
          name:'SpiderDem',
          component:SpiderDem,
        }
      ],

    }
  ]
})
