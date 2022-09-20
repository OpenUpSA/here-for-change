// for dropDowns
function dropDownHandler(e, btnId, isLang = false) {
  const link_text = e.target.innerHTML;
  const ward_btn = document.getElementById(btnId);
  if (isLang === false) {
    ward_btn.getElementsByTagName("span")[0].innerHTML = link_text;
  } else {
    lang_abbr = e.target.getAttribute("data-lang");
    ward_btn.getElementsByTagName("span")[0].innerHTML = lang_abbr;
  }
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
const surveyContainer1 =
  document.getElementsByClassName("survey-container-1")[0];
const surveyContainer2 =
  document.getElementsByClassName("survey-container-2")[0];
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

//Toc section
const toc_btns = document.getElementsByClassName("toc-btn");
const toc_sections = document.getElementsByClassName("toc");

if (toc_btns) {
  for (let i = 0; i < toc_btns.length; i++) {
    toc_btns[i].addEventListener("click", (e) => {
      for (let i = 0; i < toc_sections.length; i++) {
        toc_sections[i].style.display = "none";
      }
      let toc_name = e.currentTarget.children[1].textContent
        .trim()
        .toLowerCase();
      document.getElementById(toc_name).style.display = "block";

      for (j = 0; j < toc_btns.length; j++) {
        toc_btns[j].classList.remove("btn-active");
        toc_btns[j].classList.add("btn-inactive");
      }
      e.currentTarget.classList.remove("btn-inactive");
      e.currentTarget.classList.add("btn-active");
    });
  }
}

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

if (document) {
  var element = document.getElementById("toc");
  if (element) {
    var elementHeight = element.clientHeight;
  }
  document.addEventListener("scroll", animate);
  function inView() {
    var windowHeight = window.innerHeight;
    var scrollY = window.scrollY || window.pageYOffset;
    var scrollPosition = scrollY + windowHeight;
    var elementPosition =
      element.getBoundingClientRect().top + scrollY + elementHeight;
    if (scrollPosition > elementPosition) {
      return true;
    }
    return false;
  }

  function animate() {
    if (inView()) {
      const sideAnime = document.getElementById("side-anime");
      const sideAnimeBanner = document.getElementById("side-anime-banner");

      sideAnime.classList.add("side-anime");
      sideAnimeBanner.classList.add("side-anime-banner");
    }
  }
}

function Scrolldown() {
  const anchorId = window.location.href.split("#")[1];
  if(anchorId){
    window.location.hash = `#${anchorId}`
  }
}

window.onload = Scrolldown;
