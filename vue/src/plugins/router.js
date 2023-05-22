import * as VueRouter from 'vue-router';

const login_interface = () => import("@/components/login_interface.vue");
const anchor_interface = () => import("@/components/anchor_interface.vue");
const chairman_interface = () => import ("@/components/chairman_interface.vue");

const routes = [
    {path: '/', redirect: '/interface/login'},
    {path: '/interface/login', component: login_interface, name: 'login_interface', meta: {title: '登录界面'}},
    {
        path: '/interface/anchor/:account',
        component: anchor_interface,
        name: 'anchor_interface',
        meta: {title: '主播界面'}
    },
    {
        path: '/interface/chairman/:account',
        component: chairman_interface,
        name: 'chairman_interface',
        meta: {title: '公会界面'}
    },
]

export const router = VueRouter.createRouter({
    history: VueRouter.createWebHashHistory(),
    routes
})

router.beforeEach((to, from, next) => {
    if (to.meta.title) {
        document.title = to.meta.title
    }
    next();
})
