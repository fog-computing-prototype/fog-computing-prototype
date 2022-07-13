import { RouteRecordRaw, createRouter, createWebHistory } from "vue-router";
import HomeView from "@/views/HomeView.vue";

const routes: Array<RouteRecordRaw> = [
  {
    path: "/",
    name: "Home",
    component: HomeView,
  },
  {
    path: "/settings",
    name: "Settings",
    component: () => import("@/views/SettingsView.vue"),
  },
  {
    path: "/:pathMatch(.*)*",
    name: "Page not found",
    component: () => import("@/views/PageNotFoundView.vue"),
  },
];

const router = createRouter({
  // history: createWebHistory(process.env.BASE_URL),
  // history: createWebHistory(import.meta.env.BASE_URL),
  // history: createWebHistory("/fog-computing-prototype/"),
  history: createWebHistory(),
  routes,
});
export default router;
