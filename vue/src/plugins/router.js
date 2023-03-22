import * as VueRouter from 'vue-router';

const login_interface = () => import("@/components/login_interface.vue");
const anchor_interface = () => import("@/components/anchor_interface.vue");
const chairman_interface = () => import ("@/components/chairman_interface.vue");

const routes = [
    {path: '/', redirect: '/interface/login'},
    {path: '/interface/login', component: login_interface, name: 'login_interface'},
    {path: '/interface/anchor/:account', component: anchor_interface, name: 'anchor_interface'},
    {path: '/interface/chairman/:account', component: chairman_interface, name: 'chairman_interface'},
]

export const router = VueRouter.createRouter({
    history: VueRouter.createWebHashHistory(),
    routes
})

router.beforeEach((to, from, next) => {
    next();
})
