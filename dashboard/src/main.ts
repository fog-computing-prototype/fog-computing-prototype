import { createApp } from "vue";
import App from "./App.vue";
import "./index.css";
import { dom, library } from "@fortawesome/fontawesome-svg-core";
import { faCircle } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import router from "./router";
library.add(faCircle);

createApp(App).use(router).component("fa", FontAwesomeIcon).mount("#app");
