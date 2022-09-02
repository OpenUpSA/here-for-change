    // for dropDowns
      function dropDownHandler(e, btnId, isLang=false){
          const link_text = e.target.innerHTML;
          const ward_btn = document.getElementById(btnId);
          if(isLang===false){
            ward_btn.getElementsByTagName("span")[0].innerHTML = link_text;
          }
          else{
            lang_abbr = e.target.getAttribute('data-lang');
            ward_btn.getElementsByTagName("span")[0].innerHTML = lang_abbr;
          }
      }

      const trayTabs = document.getElementsByClassName("tray-tabs");
      const tray = document.getElementsByClassName("nav-tray")[0];
      tray.addEventListener("mouseover", ()=>{
        tray.classList.remove("top-[-50%]")
        tray.classList.add("toggle-tray")
      })

      tray.addEventListener("mouseout", ()=>{
        tray.classList.remove("toggle-tray")
        tray.classList.add("top-[-50%]")
      })

      for(let i=0; i<trayTabs.length; i++){
        trayTabs[i].addEventListener("mouseover", ()=>{
          const tray = document.getElementsByClassName("nav-tray")[0];
          tray.classList.remove("top-[-50%]")
          tray.classList.add("toggle-tray")
          
        
        })
        trayTabs[i].addEventListener("mouseout", ()=>{
          const trayMenu = document.getElementsByClassName("nav-tray")[0];
          trayMenu.classList.remove("toggle-tray")
          trayMenu.classList.add("top-[-50%]")
        })
      }

    //for accordions
      const btns = document.getElementsByClassName("tab-button");
      const panels = document.getElementsByClassName("panel");
      const icons = document.getElementsByClassName("tab-caret")
      for(let i=0; i<btns.length; i++){
            btns[i].addEventListener("click", ()=>{
            if(panels[i].style.maxHeight){
                panels[i].style.maxHeight = null;
                icons[i].classList.toggle("rotate-icon")
            }
            else{
                panels[i].style.display = "block";
                icons[i].classList.toggle("rotate-icon")
                panels[i].style.maxHeight = panels[i].scrollHeight + "px";
            }
        })
      }

    
    //Survey container toggle
    const showResultBtn = document.getElementsByClassName("show-results")[0];
    const surveyContainer1 = document.getElementsByClassName("survey-container-1")[0];
    const surveyContainer2 = document.getElementsByClassName("survey-container-2")[0];
    const hideResultBtn = document.getElementsByClassName("hide-results")[0];

    showResultBtn.addEventListener("click", ()=>{
        surveyContainer1.style.display = "none";
        surveyContainer2.style.display = "block";
    })

    hideResultBtn.addEventListener("click", ()=>{
        surveyContainer1.style.display = "block";
        surveyContainer2.style.display = "none";
    })


//other survey answer toggle
const otherBtn = document.getElementsByClassName("other-button")[0];
const otherInput = document.getElementsByClassName("other-input")[0];

otherBtn.addEventListener("click", ()=>{
    if(otherInput.style.maxWidth){
        otherInput.style.maxWidth = null;
        otherInput.style.padding = null;
    }
    else{
        otherInput.style.display = "block";
        otherInput.style.padding = "12px";
        otherInput.style.maxWidth = otherInput.scrollWidth + "px";
    }
})


//Toc section
function openToc(event, toc_name) {
  const toc_btns = document.getElementsByClassName("toc-btn");
  const toc_sections = document.getElementsByClassName("toc");

  for(let i=0; i<toc_sections.length; i++){
    toc_sections[i].style.display = "none";
  }
  document.getElementById(toc_name).style.display = "block";

  for (i = 0; i < toc_btns.length; i++) {
   toc_btns[i].classList.remove("btn-active");
   toc_btns[i].classList.add("btn-inactive");
  }
  event.currentTarget.classList.remove("btn-inactive");
  event.currentTarget.classList.add("btn-active");
}





    