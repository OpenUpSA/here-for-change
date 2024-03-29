var mapEl = document.querySelector("#map");
var centerPosition = [];
var current_ward = current_ward; //global
var areas = [];
var youAreHereLatlng = [];
var mapBoundary = [];
var municipalityId = "";
var wardId = "";
var neighbouring_wards = neighbouring_wards; //global
var wardAreaData = [];
var neighbourAreaData = [];

var provinces = [];
var municipalities = [];
var wards = [];
var baseUrl =
  window.document.location.href.split("/")[0] +
  "//" +
  window.document.location.href.split("/")[2];
var hasMunis = false;
var hasWards = false;

if (mapEl) {
  var tiles = L.gridLayer.googleMutant({
    type: "roadmap",
  });

  var map = L.map(mapEl, {
    layers: [tiles],
    center: [-28.7966, 24.5949],
    zoom: 4,
  });
  async function getWardDataFromBackend() {
    wardAreaData = current_ward.geometry;
    wardAreaData["name"] = current_ward.name;
    wardAreaData["slug"] = current_ward.slug;
    wardAreaData["details"] = current_ward.ward_detail;
    mapBoundary.push(wardAreaData);

    neighbouring_wards.forEach((neighbour) => {
      neighbourAreaData = neighbour.geometry;
      neighbourAreaData["name"] = neighbour["name"];
      neighbourAreaData["slug"] = neighbour["slug"];
      neighbourAreaData["details"] = neighbour["ward_detail"];
      mapBoundary.push(neighbourAreaData);
    });
  }

  async function setBaseIds() {
    if (current_ward) {
      municipalityId = current_ward.muniCode;
      wardId = current_ward.slug;
      centerPosition = current_ward.coords;
    }
  }

  async function getHomeMapData() {
    await fetch(`${baseUrl}/provinces/list/`)
      .then((response) => response.json())
      .then((data) => {
        data.provinces.forEach((province) => {
          provinces = JSON.parse(province.map_geoJson);
          provinces["name"] = province["name"];
          provinces["province_code"] = province["province_code"];
          provinces["area_number"] = province["area_number"];
          mapBoundary.push(provinces);
        });
        mapLoader && mapLoader.classList.add("hidden");
        loadMap();
        let zoom = 4;
        centerPosition = [-28.7966, 24.5949];
        map.setView(centerPosition, zoom);
      })
      .catch((e) => console.log(e));
  }

  function provinceClickHandler(province_code, coords) {
    mapLoader && mapLoader.classList.remove("hidden");
    fetch(`${baseUrl}/provinces/${province_code}/municipalities/list/`)
      .then((response) => response.json())
      .then((munis) => {
        map.removeLayer(areas);
        hasMunis = true;
        mapBoundary = [];

        munis.municipalities.forEach((muni) => {
          municipalities = JSON.parse(muni.map_geoJson);
          municipalities["name"] = muni["name"];
          municipalities["municipality_code"] = muni["municipality_code"];
          municipalities["municipality_type"] = muni["municipality_type"];
          municipalities["area_number"] = muni["area_number"];
          mapBoundary.push(municipalities);
        });
        mapLoader && mapLoader.classList.add("hidden");

        loadMap();
        let zoom = 6;
        centerPosition = [coords.lat, coords.lng];
        map.setView(centerPosition, zoom);
      })
      .catch((e) => {
        mapLoader && mapLoader.classList.add("hidden");
        console.log(e);
      });
  }

  function muniClickHandler(municipality_code, coords) {
    mapLoader && mapLoader.classList.remove("hidden");
    fetch(`${baseUrl}/municipalities/${municipality_code}/wards/list/`)
      .then((response) => response.json())
      .then((wardData) => {
        map.removeLayer(areas);
        hasMunis = false;
        hasWards = true;
        mapBoundary = [];

        wardData.wards.forEach((ward) => {
          wards = JSON.parse(ward.map_geoJson);
          wards["name"] = ward["name"];
          wards["slug"] = ward["slug"];
          wards["absolute_url"] = ward["absolute_url"];
          wards["municipality"] = ward["municipality"];
          mapBoundary.push(wards);
        });
        mapLoader && mapLoader.classList.add("hidden");

        loadMap();
        let zoom = 8;
        centerPosition = [coords.lat, coords.lng];
        map.setView(centerPosition, zoom);
      })
      .catch((e) => {
        console.log(e);
        mapLoader && mapLoader.classList.add("hidden");
      });
  }

  function wardClickHandler(ward_url) {
    mapLoader && mapLoader.classList.remove("hidden");
    updateParentOrSelfLocationSearch(ward_url);
  }

  function getBrowserLocation() {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(successLocation, failedLocation);
    } else {
      alert("Geolocation not available");
    }
  }

  function successLocation(position) {
    youAreHereLatlng.push(position.coords.longitude);
    youAreHereLatlng.push(position.coords.latitude);
    createCookie("userLoc", youAreHereLatlng, 2);
    setYouAreHere();
  }

  function failedLocation() {
    console.log("Please enable location permission");
  }

  function createCookie(name, value, days) {
    var expires;
    if (days) {
      var date = new Date();
      date.setTime(date.getTime() + days * 24 * 60 * 60 * 1000);
      expires = "; expires=" + date.toGMTString();
    } else {
      expires = "";
    }
    document.cookie = name + "=" + value + expires + "; path=/";
  }

  function getCookie(c_name) {
    if (document.cookie.length > 0) {
      c_start = document.cookie.indexOf(c_name + "=");
      if (c_start != -1) {
        c_start = c_start + c_name.length + 1;
        c_end = document.cookie.indexOf(";", c_start);
        if (c_end == -1) {
          c_end = document.cookie.length;
        }
        return unescape(document.cookie.substring(c_start, c_end));
      }
    }
    return "";
  }

  function setYouAreHere() {
    var youAreHere = L.divIcon({
      className: "text-pin is-filter-contrast-high is-pointer-events-none",
      iconAnchor: [42, 48],
      html: "<div>You are here</div>",
      interactive: false,
    });

    if (youAreHereLatlng.length > 0) {
      L.marker(youAreHereLatlng, {
        icon: youAreHere,
        riseOnHover: true,
        bubblingMouseEvents: true,
      }).addTo(map);
    }
  }

  function locationBtnHandler() {
    const locationModal = document.querySelector("#location-modal");
    if (locationModal) {
      openModal();
      if (navigator.geolocation) {
        setTimeout(() => {
          navigator.geolocation.getCurrentPosition(
            successRedirect,
            failedRedirect
          );
        }, 1000);
      } else {
        alert("Geolocation not available");
      }
    }
  }

  function successRedirect(position) {
    youAreHereLatlng.push(position.coords.longitude);
    youAreHereLatlng.push(position.coords.latitude);

    let userLocation = getCookie("userLoc");
    if (!userLocation) {
      createCookie("userLoc", youAreHereLatlng, 2);
    }
    const form = document.getElementById("redirect-to-closest-ward-form");
    form.querySelector('input[name="latitude"]').value =
      position.coords.latitude;
    form.querySelector('input[name="longitude"]').value =
      position.coords.longitude;
    form.querySelector('input[name="url"]').value =
      window.document.location.pathname;
    form.submit();
  }

  function failedRedirect() {
    alert("Please enable location permission");
  }

  function embedLocBtnHandler() {
    const useLocationLoader = document.querySelector("#use-location-loader");
    if (useLocationLoader) {
      useLocationLoader.classList.remove("hidden");
      if (navigator.geolocation) {
        setTimeout(() => {
          navigator.geolocation.getCurrentPosition(
            successRedirect,
            failedEmbedRedirect
          );
        }, 1000);
      } else {
        alert("Geolocation not available");
      }
    }
  }

  function failedEmbedRedirect() {
    alert("Please enable location permission");
    const useLocationLoader = document.querySelector("#use-location-loader");
    if (useLocationLoader) {
      useLocationLoader.classList.add("hidden");
    }
  }

  var canAccessParent = function () {
    try {
      return !!parent.document.location.pathname;
    } catch (err) {
      return false;
    }
  };

  var updateParentOrSelfLocationSearch = function (path) {
    if (canAccessParent()) {
      parent.document.location.pathname = path;
    } else {
      document.location.pathname = path;
    }
  };

  async function mapInit() {
    if (current_ward) {
      await setBaseIds();
      await getWardDataFromBackend();
      setTimeout(() => {
        mapLoader && mapLoader.classList.add("hidden");
        loadMap();
      }, 1000);
      let zoom = current_ward.defaultZoom;
      map.setView(centerPosition, zoom);

      let userLocation = getCookie("userLoc");
      if (userLocation) {
        youAreHereLatlng = userLocation.split(",");
        setYouAreHere();
      } else {
        getBrowserLocation();
      }
    } else {
      await getHomeMapData();
    }
  }
  mapInit();

  const mapLoader = document.querySelector("#map-loader");

  const locationBtn = document.querySelector("#location-btn");
  if (locationBtn) {
    locationBtn.addEventListener("click", locationBtnHandler);
  }

  const openModalBtn = document.querySelector("#open-modal");
  if (openModalBtn) {
    openModalBtn.addEventListener("click", locationBtnHandler);
  }

  //embed location button handler
  const embedLocationBtn = document.querySelector("#embed-location-btn");
  if (embedLocationBtn) {
    embedLocationBtn.addEventListener("click", embedLocBtnHandler);
  }

  // Google places Autocomplete
  function googlePlacesAutocomplete(inputId) {
    const input = document.getElementById(inputId);
    var options = {
      types: [
        "street_address",
        "sublocality",
        "route",
        "point_of_interest",
        "postal_code",
      ],
      componentRestrictions: { country: "ZA" },
    };
    if (input) {
      const searchBox = new google.maps.places.Autocomplete(input, options);
      searchBox.addListener("place_changed", () => {
        mapLoader && mapLoader.classList.remove("hidden");
        const place = searchBox.getPlace();
        if (place.length == 0) {
          return;
        }
        const form = document.getElementById("redirect-to-closest-ward-form");
        form.querySelector('input[name="longitude"]').value =
          place.geometry.location.lng();
        form.querySelector('input[name="latitude"]').value =
          place.geometry.location.lat();
        form.querySelector('input[name="url"]').value =
          window.document.location.pathname;
        form.submit();
      });
    }
  }
  //Home and embed page search
  googlePlacesAutocomplete("address-search-input");
  //ward page search
  googlePlacesAutocomplete("nav-search-input");

  var loadMap = () => {
    if (mapBoundary.length > 0) {
      areas = L.geoJSON(mapBoundary, {
        style: {
          color: "#999",
          fillOpacity: 0.01,
          weight: 2,
        },
      }).addTo(map);

      areas.getLayers().forEach((layer) => {
        var slug = layer.feature.geometry.slug;
        var name = layer.feature.geometry.name;
        var layerCenter = layer.getBounds().getCenter();
        var popup = L.popup({ className: "mapTooltip", closeButton: false });
        popup.setContent(`${name}`);
        layer.bindPopup(popup);
        layer.on("mouseover", function (e) {
          var popup = e.target.getPopup();
          popup.setLatLng(e.latlng).openOn(map);
        });

        layer.on("mouseout", function (e) {
          e.target.closePopup();
        });

        layer.on("mousemove", function (e) {
          popup.setLatLng(e.latlng).openOn(map);
        });

        var partyLogoUrl;
        if (
          layer.feature.geometry.details &&
          layer.feature.geometry.details.councillor_political_party_logo_url
        ) {
          partyLogoUrl =
            layer.feature.geometry.details.councillor_political_party_logo_url
              .value;
        }

        if (current_ward && partyLogoUrl) {
          var iconMarker = L.marker(layerCenter, {
            icon: L.icon({
              iconUrl: partyLogoUrl,
              iconSize: [40, 40],
              iconAnchor: [20, 20],
              className: "icon-marker",
              bubblingMouseEvents: true,
            }),
            riseOnHover: true,
            bubblingMouseEvents: true,
          }).addTo(map);

          iconMarker.on("click", (e) => {
            if (window.document.location.pathname.endsWith("ward-councillor")) {
              updateParentOrSelfLocationSearch(
                `municipalities/${municipalityId}/wards/${slug}/ward-councillor`
              );
            } else {
              updateParentOrSelfLocationSearch(
                `municipalities/${municipalityId}/wards/${slug}/`
              );
            }
          });
          iconMarker.bindTooltip(
            `${layer.feature.geometry.details.councillor_political_party.value} - ${layer.feature.geometry.details.councillor_name.value}`,
            {
              direction: "top",
              offset: [0, -20],
              className: "mapTooltip",
              permanent: false,
              opacity: 1,
            }
          );

          iconMarker.on("mouseover", (e) => {
            e.target.setIcon(
              L.icon({
                iconUrl: "../../../../static/assets/placeholder-image-1.svg",
                iconSize: [40, 40],
                iconAnchor: [20, 20],
                className: "icon-marker",
                bubblingMouseEvents: true,
              })
            );
          });

          iconMarker.on("mouseout", (e) => {
            e.target.setIcon(
              L.icon({
                iconUrl:
                  layer.feature.geometry.details
                    .councillor_political_party_logo_url.value,
                iconSize: [40, 40],
                iconAnchor: [20, 20],
                className: "icon-marker",
                bubblingMouseEvents: true,
              })
            );
          });
        }

        if (wardId == slug) {
          layer.setStyle({
            weight: 3,
            fillOpacity: 0.05,
            color: "#8334f7",
          });
          layer.bringToFront();
          map.fitBounds(layer.getBounds());
        }

        //Map layer click handler
        layer.on("click", (e) => {
          if (current_ward) {
            var slug = e.target.feature.geometry.slug;

            if (window.document.location.pathname.endsWith("ward-councillor")) {
              updateParentOrSelfLocationSearch(
                `municipalities/${municipalityId}/wards/${slug}/ward-councillor`
              );
            } else {
              updateParentOrSelfLocationSearch(
                `municipalities/${municipalityId}/wards/${slug}/`
              );
            }
          } else {
            if (municipalities.length === 0) {
              provinceClickHandler(
                e.target.feature.geometry.province_code,
                e.latlng
              );
            }
            if (municipalities.length !== 0 && hasMunis) {
              muniClickHandler(
                e.target.feature.geometry.municipality_code,
                e.latlng
              );
            }
            if (municipalities.length !== 0 && !hasMunis && hasWards) {
              wardClickHandler(e.target.feature.geometry.absolute_url);
            }
          }
        });

        layer.on("mouseover", (e) => {
          e.target.setStyle({
            weight: 3,
            fillOpacity: 0.05,
            color: "#8334f7",
          });
          e.target.bringToFront();
        });

        layer.on("mouseout", (e) => {
          if (e.target.feature.geometry.slug != wardId) {
            areas.resetStyle(e.target);
          }
        });
      });
    }
  };

  //resize embed map on feedback form open
  const sendFeedbackBtn = document.querySelector("#send-feedback");
  sendFeedbackBtn &&
    sendFeedbackBtn.addEventListener("click", () => {
      setTimeout(function () {
        map.invalidateSize();
      }, 200);
    });
}
