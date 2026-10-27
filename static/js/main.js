import { initAccessibility } from "./components/accessibility.js";
import { initCarousels } from "./components/carousel.js";
import { initDialogs } from "./components/dialog.js";
import { initFileUploads } from "./components/file-upload.js";
import { initNavDropdowns } from "./components/nav-dropdown.js";
import { initNavToggle } from "./components/nav-toggle.js";
import { initStartupFilters } from "./components/startup-filters.js";

document.documentElement.classList.add("js");

initNavToggle();
initNavDropdowns();
initCarousels();
initAccessibility();
initStartupFilters();
initFileUploads();
initDialogs();
