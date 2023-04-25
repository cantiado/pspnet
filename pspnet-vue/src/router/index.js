import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import LoginView from "../views/LoginView.vue";
import RegisterView from "../views/RegisterView.vue";
import IdentifyView from "../views/IdentifyView.vue";
import UserProfile from "../views/UserProfile.vue";
import AccountSettingsView from "../views/AccountSettingsView.vue";
import GallaryView from "../views/GallaryView.vue";
import JobsView from "../views/JobsView.vue";
import Explore from "../views/ExploreDataView.vue";
import AboutView from "../views/AboutView.vue";
import ResetView from "../views/ResetView";
import ForgotView from "../views/ForgotView";
import CollectionsView from "../views/CollectionsView.vue";

const routes = [
  {
    path: "/",
    name: "home",
    component: HomeView,
  },
  {
    path: "/login",
    name: "login",
    component: LoginView,
  },
  {
    path: "/reset/:resetToken",
    name: "resetPassword",
    component: ResetView,
  },
  {
    path: "/forgot",
    name: "forgot",
    component: ForgotView,
  },
  {
    path: "/about",
    component: AboutView,
    children: [
      {
        path: "",
        name: "about",
        component: () => import("../components/AboutSection.vue"),
      },
      {
        path: "abstract",
        name: "abstract",
        component: () => import("../components/AbstractSection.vue"),
      },
      {
        path: "background",
        name: "background",
        component: () => import("../components/BackgroundSection.vue"),
      },
      {
        path: "goals",
        name: "goals",
        component: () => import("../components/GoalsSection.vue"),
      },
      {
        path: "dataset",
        name: "dataset",
        component: () => import("../components/DatasetSection.vue"),
      },
      {
        path: "model",
        name: "model",
        component: () => import("../components/ModelSection.vue"),
      },
      {
        path: "research",
        name: "research",
        component: () => import("../components/ResearchSection.vue"),
      },
      {
        path: "resources",
        name: "resources",
        component: () => import("../components/ResourcesSection.vue"),
      },
    ],
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    // component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
  },
  {
    path: "/register",
    name: "register",
    component: RegisterView,
  },
  {
    path: "/profile",
    name: "profile",
    component: UserProfile,
  },
  {
    path: "/identify",
    name: "identify",
    component: IdentifyView,
  },
  {
    path: "/gallary",
    name: "gallary",
    component: GallaryView,
  },
  {
    path: "/settings",
    name: "settings",
    component: AccountSettingsView,
  },
  {
    path: "/jobs",
    name: "jobs",
    component: JobsView,
  },
  {
    path: "/explore",
    name: "explore",
    component: Explore,
    // children: [
    //   {
    //     path: "",
    //     name: "explore",
    //     component: Explore
    //   },
    //   {
    //     path: "/:id",
    //     name: "singleDataset",
    //     component: () => import("../components/DatasetView.vue"),
    //   }
    // ]
  },
  {
    path: "/explore/:dsName",
    name: "singleDataset",
    component: () => import("../components/DatasetView.vue"),
    props: true,
  },
  {
    path: "/collections",
    component: CollectionsView,
    children: [
      {
        path: "",
        name: "collections",
        component: () => import("../components/MyCollections.vue"),
      },
      {
        path: ":projectName",
        name: "singleProject",
        component: () => import("../components/SingleProject.vue"),
        props: true,
      },
      {
        path: "shared",
        name: "shared",
        component: () => import("../components/SharedCollections.vue"),
      },
      {
        path: "affiliates",
        name: "affiliates",
        component: () => import("../components/Affiliates.vue"),
      },
    ],
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
