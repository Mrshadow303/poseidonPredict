import Vue from 'vue';
import Vuex from 'vuex';
import router, { resetRouter } from "../router";
import createPersistedState from 'vuex-persistedstate';

Vue.use(Vuex);

function addNewRoute(menuList) {
    console.log("menuList: ", menuList);
    let routes = router.options.routes;
    console.log("routes: ", routes);
    routes.forEach(routeItem => {
        if (routeItem.path == "/Index") {
            menuList.forEach(menu => {
                console.log("menuComponent: ", menu.menuComponent);
                let componentPath = `@/components/${menu.menuComponent}.vue`;
                console.log("componentPath: ", componentPath);

                let childRoute = {
                    path: '/' + menu.menuClick,
                    name: menu.menuName,
                    meta: {
                        title: menu.menuName
                    },
                    component: () => import(/* webpackChunkName: "[request]" */ `@/components/${menu.menuComponent}`)
                };

                // 检查是否存在相同的 name 或 path
                let duplicate = routeItem.children.find(child => child.name === childRoute.name || child.path === childRoute.path);
                if (duplicate) {
                    console.error(`发现重复路径: name - ${childRoute.name}, path - ${childRoute.path}`);
                    return;
                }

                console.log("childRoute: ", childRoute);
                routeItem.children.push(childRoute);
                console.log("routeItem.children: ", routeItem.children);
            });
        }
    });

    resetRouter();
    router.addRoutes(routes);
}

export default new Vuex.Store({
    state: {
        menu: []
    },
    mutations: {
        setMenu(state, menuList) {
            state.menu = menuList;
            addNewRoute(menuList);
        }
    },
    getters: {
        getMenu(state) {
            return state.menu;
        }
    },
    plugins: [createPersistedState()]
});
