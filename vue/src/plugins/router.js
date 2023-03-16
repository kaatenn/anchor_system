import * as VueRouter from 'vue-router';

const login_interface = () => import("@/components/login_interface.vue");
const anchor_interface = () => import("@/components/anchor_interface.vue");
const chairman_interface = () => import ("@/components/chairman_interface.vue");

const routes = [
    {path: '/', redirect: '/interface/login'},
    {path: '/interface/login', component: login_interface},
    {path: '/interface/anchor', component: anchor_interface},
    {path: '/interface/chairman', component: chairman_interface}
]

export const router = VueRouter.createRouter({
    history : VueRouter.createWebHashHistory(),
    routes
})

router.beforeEach((to, from, next) => {
    next();
})
