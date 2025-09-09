tailwind.config = {
  theme: {
    extend: {
      colors: {
        "brand-orange": "#FF4F12",
        "brand-purple": "#7700FF",
        "brand-light": "#F4F4F5",
        "brand-deep-blue": "#1D1B1F",
        "brand-hover": "#2A282C",
        "brand-container": "#EEEEF0",
      },
    },
  },
};

// Функция для установки активной вкладки
function setActiveTab(clickedElement) {
  document.querySelectorAll(".sidebar-link").forEach((link) => {
    link.classList.remove("active");
  });
  clickedElement.classList.add("active");
}

// Новая функция для активации ссылки в sidebar по hx-get
function activateSidebarByHxGet(hxGetValue) {
  const links = document.querySelectorAll(".sidebar-link");
  links.forEach((link) => {
    const linkHxGet = link.getAttribute("hx-get");
    if (linkHxGet === hxGetValue) {
      setActiveTab(link);
    }
  });
}

// Обработчик кликов для синхронизации кнопки в header с sidebar
document.addEventListener("click", function (event) {
  const target = event.target.closest("[hx-get]");
  if (target && !target.classList.contains("sidebar-link")) {
    const hxGet = target.getAttribute("hx-get");
    if (hxGet) {
      activateSidebarByHxGet(hxGet);
    }
  }
});

// Обработчик для HTMX событий
document.addEventListener("htmx:afterRequest", function (event) {
  if (event.detail.successful) {
    const trigger = event.detail.elt;
    if (trigger && trigger.classList.contains("sidebar-link")) {
      setActiveTab(trigger);
    }
  }
});

// Инициализация при загрузке страницы
document.addEventListener("DOMContentLoaded", function () {
  const currentPath = window.location.pathname;
  const links = document.querySelectorAll(".sidebar-link");
  let activated = false;
  links.forEach((link) => {
    const hxGet = link.getAttribute("hx-get");
    if (hxGet && currentPath.includes(hxGet)) {
      setActiveTab(link);
      activated = true;
    }
  });
  if (!activated && links.length > 0) {
    setActiveTab(links[0]); // Активируем первую ссылку по умолчанию
  }
});

// Функция для обработки навигации назад/вперед
window.addEventListener("popstate", function (event) {
  const currentPath = window.location.pathname;
  const links = document.querySelectorAll(".sidebar-link");
  links.forEach((link) => {
    const hxGet = link.getAttribute("hx-get");
    if (hxGet && currentPath.includes(hxGet)) {
      setActiveTab(link);
    }
  });
});
