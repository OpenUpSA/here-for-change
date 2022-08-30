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
        tray.classList.add("top-[68px]")
      })

      tray.addEventListener("mouseout", ()=>{
        tray.classList.remove("top-[68px]")
      })

      for(let i=0; i<trayTabs.length; i++){
        trayTabs[i].addEventListener("mouseover", ()=>{
          const tray = document.getElementsByClassName("nav-tray")[0];
          tray.classList.add("top-[68px]")
          
        
        })
        trayTabs[i].addEventListener("mouseout", ()=>{
          const trayMenu = document.getElementsByClassName("nav-tray")[0];
          trayMenu.classList.remove("top-[68px]")
          trayMenu.classList.add("top-[-50%]")
        })
      }

    //for accordions
      const btns = document.getElementsByClassName("menu-buttons");
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
    