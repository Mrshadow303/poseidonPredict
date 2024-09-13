import Vue from 'vue';
import VueRouter from 'vue-router';

Vue.use(VueRouter);

const routes = [
    {
        path: '/',
        name: 'login',
        component: () => import('@/components/Login.vue')
    },
    {
        path: '/Index',
        name: 'index',
        component: () => import('@/components/Index.vue'),
        children: [
            {
                path: '/Home',
                name: 'home',
                meta: {
                    title: '首页'
                },
                component: () => import('@/components/Home.vue')
            },
        ]
    }
];

const router = new VueRouter({
    mode: 'history',
    routes
});

export function resetRouter() {
    const newRouter = new VueRouter({
        mode: 'history',
        routes
    });
    router.matcher = newRouter.matcher; // reset router
}

const VueRouterPush = VueRouter.prototype.push;
VueRouter.prototype.push = function push(to) {
    return VueRouterPush.call(this, to).catch(err => err);
};

export default router;
