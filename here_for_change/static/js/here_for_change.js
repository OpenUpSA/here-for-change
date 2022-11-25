// for dropDowns
const ward_btn = document.querySelector("#ward-button");
const ward_dropdown = document.querySelector(".dropdown-panel");
const ward_items = document.querySelectorAll(".ward-item");

if (ward_btn) {
  ward_btn.addEventListener("click", () => {
    ward_dropdown.classList.remove("hidden");
  });
}

if (ward_items) {
  ward_items.forEach((ward_item) => {
    ward_item.addEventListener("click", (e) => {
      ward_btn.getElementsByTagName("span")[0].textContent = e.target.innerHTML;
      ward_dropdown.classList.add("hidden");
    });
  });
}

function onVisible(element, callback) {
  new IntersectionObserver((entries, observer) => {
    entries.forEach((entry) => {
      if (entry.intersectionRatio > 0) {
        callback(element);
        // observer.disconnect();
      }
    });
  }).observe(element);
}

if (ward_dropdown) {
  onVisible(ward_dropdown, () => {
    document.addEventListener("click", closeDropdown);
  });
}

function closeDropdown() {
  if (ward_dropdown) {
    ward_dropdown.classList.add("hidden");
  }
  if (lang_dropdown) {
    lang_dropdown.classList.add("hidden");
  }
  document.removeEventListener("click", closeDropdown);
}

const lang_btn = document.querySelector("#lang-button");
const lang_dropdown = document.querySelector("#lang-dropdown");
const lang_items = document.querySelectorAll(".lang-item");

if (lang_btn) {
  lang_btn.addEventListener("click", () => {
    lang_dropdown.classList.remove("hidden");
  });
}

if (lang_items) {
  lang_items.forEach((lang_item) => {
    lang_item.addEventListener("click", (e) => {
      lang_btn.getElementsByTagName(
        "span"
      )[0].textContent = e.target.getAttribute("data-lang");
      lang_dropdown.classList.add("hidden");
    });
  });
}

if (lang_dropdown) {
  onVisible(lang_dropdown, () => {
    document.addEventListener("click", closeDropdown);
  });
}

const trayTabs = document.getElementsByClassName("tray-tabs");
const tray = document.getElementsByClassName("nav-tray")[0];

if (!!tray) {
  tray.addEventListener("mouseover", () => {
    tray.classList.remove("top-[-50%]");
    tray.classList.add("toggle-tray");
  });

  tray.addEventListener("mouseout", () => {
    tray.classList.remove("toggle-tray");
    tray.classList.add("top-[-50%]");
  });

  for (let i = 0; i < trayTabs.length; i++) {
    trayTabs[i].addEventListener("mouseover", () => {
      const tray = document.getElementsByClassName("nav-tray")[0];
      tray.classList.remove("top-[-50%]");
      tray.classList.add("toggle-tray");
    });
    trayTabs[i].addEventListener("mouseout", () => {
      const trayMenu = document.getElementsByClassName("nav-tray")[0];
      trayMenu.classList.remove("toggle-tray");
      trayMenu.classList.add("top-[-50%]");
    });
  }
}

//for accordions
const btns = document.getElementsByClassName("tab-button");
const panels = document.getElementsByClassName("panel");
const icons = document.getElementsByClassName("tab-caret");
if (!!btns) {
  for (let i = 0; i < btns.length; i++) {
    btns[i].addEventListener("click", () => {
      if (panels[i].style.maxHeight) {
        panels[i].style.maxHeight = null;
        icons[i].classList.toggle("rotate-icon");
      } else {
        panels[i].style.display = "block";
        icons[i].classList.toggle("rotate-icon");
        panels[i].style.maxHeight = panels[i].scrollHeight + "px";
      }
    });
  }
}

//Survey container toggle
const showResultBtn = document.getElementsByClassName("show-results")[0];
const surveyContainer1 = document.getElementsByClassName(
  "survey-container-1"
)[0];
const surveyContainer2 = document.getElementsByClassName(
  "survey-container-2"
)[0];
const hideResultBtn = document.getElementsByClassName("hide-results")[0];

if (showResultBtn) {
  showResultBtn.addEventListener("click", () => {
    surveyContainer1.style.display = "none";
    surveyContainer2.style.display = "block";
  });
}

if (hideResultBtn) {
  hideResultBtn.addEventListener("click", () => {
    surveyContainer1.style.display = "block";
    surveyContainer2.style.display = "none";
  });
}

//other survey answer toggle
const otherBtn = document.getElementsByClassName("other-button")[0];
const otherInput = document.getElementsByClassName("other-input")[0];

if (otherBtn) {
  otherBtn.addEventListener("click", () => {
    if (otherInput.style.maxWidth) {
      otherInput.style.maxWidth = null;
      otherInput.style.padding = null;
    } else {
      otherInput.style.display = "block";
      otherInput.style.padding = "12px";
      otherInput.style.maxWidth = otherInput.scrollWidth + "px";
    }
  });
}

//Toc section onclick handler
const toc_btns = document.getElementsByClassName("toc-btn");
const toc_sections = document.getElementsByClassName("toc");

if (toc_btns) {
  for (let i = 0; i < toc_btns.length; i++) {
    toc_btns[i].addEventListener("click", (e) => {
      const targetId = e.currentTarget.href.split("#")[1];
      const targetEle = document.getElementById(targetId);
      targetEle.scrollIntoView({ behavior: "smooth", block: "start" });

      for (j = 0; j < toc_btns.length; j++) {
        toc_btns[j].classList.remove("btn-active");
        toc_btns[j].classList.add("btn-inactive");
      }
      e.currentTarget.classList.remove("btn-inactive");
      e.currentTarget.classList.add("btn-active");
    });
  }
}

//toc section onScroll handler
const links = document.querySelectorAll(".toc-btn");
const sections = document.querySelectorAll(".section");

function changeLinkState() {
  if (links && sections) {
    let index = sections.length;
    while (--index && window.scrollY + 200 < sections[index].offsetTop) {}
    links.forEach((link) => {
      link.classList.remove("btn-active");
      link.classList.add("btn-inactive");
    });

    links[index].classList.remove("btn-inactive");
    links[index].classList.add("btn-active");
  }
}

// window.addEventListener("scroll", changeLinkState);

// bar tooltips positioning
const spendingBar = document.getElementsByClassName("spending-bar");
const barTooltip = document.getElementsByClassName("barTooltip");
const barTooltipText = document.getElementsByClassName("barTooltipText");

if (barTooltip) {
  for (let i = 0; i < barTooltip.length; i++) {
    barTooltip[i].addEventListener("mouseover", () => {
      let spendingBarWidth = spendingBar[i].offsetWidth;
      let tooltipWidth = barTooltipText[i].offsetWidth;
      let leftSpace = (spendingBarWidth - tooltipWidth) / 2;

      barTooltipText[i].style.left = leftSpace + 62 + "px";
    });
  }
}

//info tooltips positioning

const tooltip = document.getElementsByClassName("tooltip");
const tooltipText = document.getElementsByClassName("tooltipText");

if (tooltip) {
  for (let i = 0; i < tooltip.length; i++) {
    tooltip[i].addEventListener("mouseover", () => {
      let tooltipWidth = tooltipText[i].offsetWidth;
      tooltipText[i].style.left = "-" + (tooltipWidth - 6) / 2 + "px";
    });
  }
}

// voting tooltips positioning
const voteTooltip = document.getElementsByClassName("voteTooltip");
const voteTooltipText = document.getElementsByClassName("voteTooltipText");

if (voteTooltip) {
  for (let i = 0; i < voteTooltip.length; i++) {
    voteTooltip[i].addEventListener("mouseover", () => {
      let containerWidth = voteTooltip[i].offsetWidth;
      let tooltipWidth = voteTooltipText[i].offsetWidth;
      let leftSpace = (tooltipWidth - containerWidth) / 2;

      voteTooltipText[i].style.left = "-" + leftSpace + "px";
    });
  }
}

//for side animation
function inView(element) {
  var windowHeight = window.innerHeight;
  var scrollY = window.scrollY || window.pageYOffset;
  var scrollPosition = scrollY + windowHeight;
  var elementHeight = element.clientHeight;
  var elementPosition =
    element.getBoundingClientRect().top + scrollY + elementHeight;
  if (scrollPosition > elementPosition) {
    return true;
  }
  return false;
}
var toc_element = document.getElementById("toc");
if (toc_element) {
  document.addEventListener("scroll", animate);
  function animate() {
    if (inView(toc_element)) {
      const sideAnime = document.getElementById("side-anime");
      const sideAnimeBanner = document.getElementById("side-anime-banner");

      sideAnime.classList.add("side-anime");
      sideAnimeBanner.classList.add("side-anime-banner");
    }
  }
}

//Councillor phone number formatting
const phone = document.getElementById("councillor-phone");
const councilNum = document.getElementById("council-num");
if (councilNum) {
  const councillorPhoneDjango = JSON.parse(councilNum.textContent);
  if (phone && councillorPhoneDjango) {
    phone.textContent = libphonenumber
      .parsePhoneNumber(councillorPhoneDjango)
      .formatNational();
  }
}

//Deputy mayor phone number formatting
const deputyMayorNum = document.getElementById("deputy-mayor-num");
if (deputyMayorNum) {
  const dmPhoneDjango = JSON.parse(deputyMayorNum.textContent);
  const deputyMayorPhone = document.getElementById("deputy-mayor-phone");
  const secDepMayorPhone = document.getElementById("sec-dep-mayor-phone");
  const secDepPhoneDjango = JSON.parse(
    document.getElementById("sec-dep-mayor-num").textContent
  );
  if (deputyMayorPhone && dmPhoneDjango) {
    deputyMayorPhone.textContent = libphonenumber
      .parsePhoneNumber(dmPhoneDjango)
      .formatNational();
  }

  if (secDepMayorPhone && secDepPhoneDjango) {
    secDepMayorPhone.textContent = libphonenumber
      .parsePhoneNumber(secDepPhoneDjango)
      .formatNational();
  }
}

const locationModal = document.querySelector("#location-modal");
const openModalBtn = document.querySelector("#open-modal");
const closeModalBtn = document.querySelector("#close-modal");

function openModal() {
  if (locationModal) {
    locationModal.classList.remove("hide-modal");
    locationModal.classList.add("show-modal");
  }
}

function closeModal() {
  if (locationModal) {
    locationModal.classList.remove("show-modal");
    locationModal.classList.add("hide-modal");
  }
}

if (locationModal) {
  locationModal.addEventListener("click", (e) => {
    const modalOverlay = document.querySelector("#modal-overlay");
    if (e.target === modalOverlay) {
      closeModal();
    }
  });
}

if (openModalBtn) {
  openModalBtn.addEventListener("click", openModal);
}

if (closeModalBtn) {
  closeModalBtn.addEventListener("click", closeModal);
}

let findCouncillorBtn = document.querySelector("#find-councillor");

if (findCouncillorBtn) {
  if (window.document.location.pathname == "/") {
    findCouncillorBtn.classList.add("hidden");
  }
}

const councillorWard = document.querySelector("#councillor-ward");
const councilNameEl = document.querySelectorAll(".ward-name");
const useLocationLoader = document.querySelector("#use-location-loader");
if (councillorWard && councilNameEl) {
  const councillorWardName = JSON.parse(councillorWard.textContent);
  let splitWardName = councillorWardName.split("Ward");
  let wardName = `Ward ${splitWardName[1]}, ${splitWardName[0]}`;
  useLocationLoader && useLocationLoader.classList.add("hidden");
  councilNameEl.forEach((el) => {
    el.textContent = wardName;
  });
}

const embedCard = document.querySelector("#embed-card");
const closeEmbed = document.querySelector("#close-embed");
const openEmbed = document.querySelector("#open-embed");

if (embedCard) {
  openEmbed.addEventListener("click", () => {
    embedCard.classList.remove("hidden");
  });

  closeEmbed.addEventListener("click", (e) => {
    embedCard.classList.add("hidden");
    e.stopPropagation();
  });
}

//Feedback form
const sendFeedbackBtn = document.querySelector("#send-feedback");
const feedbackDiv = document.querySelector("#feedback-div");
const feedbackForm = document.querySelector("#feedback-form");
const cancelFeedback = document.querySelector("#cancel-feedback");
sendFeedbackBtn &&
  sendFeedbackBtn.addEventListener("click", () => {
    feedbackDiv.classList.add("hidden");
    feedbackForm.classList.remove("hidden");
  });

cancelFeedback && cancelFeedback.addEventListener("click", () => {
  feedbackDiv.classList.remove("hidden");
  feedbackForm.classList.add("hidden");
})
