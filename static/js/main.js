import { initAccessibility } from "./components/accessibility.js";
import { initCarousels } from "./components/carousel.js";
import { initNavToggle } from "./components/nav-toggle.js";
import { initStartupFilters } from "./components/startup-filters.js";

document.documentElement.classList.add("js");

initNavToggle();
initCarousels();
initAccessibility();
initStartupFilters();
