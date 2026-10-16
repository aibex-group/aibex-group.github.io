(() => {
  "use strict";

  document.querySelectorAll(".publication-explorer").forEach((explorer) => {
    const form = explorer.querySelector(".publication-filters");
    const search = form.elements.query;
    const clear = explorer.querySelector(".publication-clear");
    const count = explorer.querySelector(".publication-count");
    const entries = [...explorer.querySelectorAll(".publication-entry")];
    const yearGroups = [...explorer.querySelectorAll(".publication-year")];

    const update = () => {
      const query = search.value.trim().toLocaleLowerCase();
      const year = form.querySelector("[data-filter-year][aria-pressed='true']").dataset.filterYear;
      const type = form.querySelector("[data-filter-type][aria-pressed='true']").dataset.filterType;
      let visibleCount = 0;

      entries.forEach((entry) => {
        const matches =
          (!query || entry.dataset.search.toLocaleLowerCase().includes(query)) &&
          (!year || entry.dataset.year === year) &&
          (!type || entry.dataset.type === type);

        entry.hidden = !matches;
        if (matches) visibleCount += 1;
      });

      yearGroups.forEach((group) => {
        group.hidden = !group.querySelector(".publication-entry:not([hidden])");
      });

      count.textContent = `${visibleCount} ${visibleCount === 1 ? "publication" : "publications"}`;
      clear.disabled = !query && !year && !type;
    };

    form.addEventListener("input", update);
    form.addEventListener("submit", (event) => event.preventDefault());
    form.addEventListener("click", (event) => {
      const filterButton = event.target.closest("[data-filter-year], [data-filter-type]");
      if (!filterButton) return;

      const attribute = filterButton.hasAttribute("data-filter-year") ? "data-filter-year" : "data-filter-type";
      form.querySelectorAll(`[${attribute}]`).forEach((button) => button.setAttribute("aria-pressed", "false"));
      filterButton.setAttribute("aria-pressed", "true");
      update();
    });
    clear.addEventListener("click", () => {
      form.reset();
      form.querySelectorAll("[data-filter-year], [data-filter-type]").forEach((button) => button.setAttribute("aria-pressed", "false"));
      form.querySelector('[data-filter-year=""]').setAttribute("aria-pressed", "true");
      form.querySelector('[data-filter-type=""]').setAttribute("aria-pressed", "true");
      search.focus();
      update();
    });

    update();
  });
})();
