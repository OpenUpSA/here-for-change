var municipality = {};
var muniLatlng = [];
var current_ward = current_ward; //global
var areas = [];
var youAreHereLatlng = [];
var muniAreaData = [];
var municipalityId = "";
var wardId = "";
var neighbouring_wards = neighbouring_wards; //global
var wardAreaData = [];
var neighbourAreaData = [];
var mapEl = document.querySelector("#map");

if (mapEl) {
  var map = L.map(mapEl);

  async function getDataFromBackend() {
    municipality["municipality_area_number"] = current_ward.muniAreaNum;
    wardAreaData = current_ward.geometry;
    wardAreaData["name"] = current_ward.name;
    wardAreaData["slug"] = current_ward.slug;
    wardAreaData["details"] = current_ward.ward_detail;
    muniAreaData.push(wardAreaData);

    neighbouring_wards.forEach((neighbour) => {
      neighbourAreaData = neighbour.geometry;
      neighbourAreaData["name"] = neighbour["name"];
      neighbourAreaData["slug"] = neighbour["slug"];
      neighbourAreaData["details"] = neighbour["ward_detail"]
      muniAreaData.push(neighbourAreaData);
    });
  }

  async function setBaseIds() {
    if (current_ward) {
      municipalityId = current_ward.muniCode;
      wardId = current_ward.slug;
      //muniLatlng = [-34.4781, 19.9798];
      muniLatlng = current_ward.coords;
    }
  }

  async function getMapData() {
    if (
      window.document.location.pathname == "/" ||
      window.document.location.pathname == "/find-my-ward-councillor"
    ) {
      //get data from json for home map
      await fetch(
        `${baseUrl}/municipalities/${municipalityId}/wards/${wardId}.json`
      )
        .then((response) => response.json())
        .then((data) => {
          let { neighbours, map_geoJson, name, slug } = data;
          municipality["municipality_area_number"] =
            data["municipality"]["area_number"];
          wardAreaData = JSON.parse(map_geoJson);
          wardAreaData["name"] = name;
          wardAreaData["slug"] = slug;
          wardAreaData["details"] = data["ward_detail"];
          
          muniAreaData.push(wardAreaData);

          neighbours.forEach((neighbour) => {
            neighbourAreaData = JSON.parse(neighbour.map_geoJson);
            let name = neighbour["name"];
            let slug = neighbour["slug"];
            neighbourAreaData["name"] = name;
            neighbourAreaData["slug"] = slug;
            neighbourAreaData["details"] = neighbour["ward_detail"]
            muniAreaData.push(neighbourAreaData);
          });
        });
    } else {
      getDataFromBackend();
    }

    // await fetch(
    //   "https://mapit.code4sa.org/area/" +
    //     municipality["municipality_area_number"] +
    //     "/touches"
    // )
    //   .then((response) => response.json())
    //   .then((data) => {
    //     municipality["neighbours"] = data;
    //     updateNeighbourMunicipalities();
    //   })
    //   .catch((e) => console.log(e));

  }

  async function setMuniOfficePin() {
    var municipalOffice = L.divIcon({
      className: "text-pin is-filter-grayscale-bw is-pointer-events-none",
      iconAnchor: [52, 48],
      html: "<div>Municipal office</div>",
      interactive: false,
    });

    L.marker(muniLatlng, {
      icon: municipalOffice,
      riseOnHover: true,
      bubblingMouseEvents: true,
    }).addTo(map);
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

  var random = function (top = 6) {
    return Math.floor(Math.random() * top);
  };

  async function mapInit() {
    if (current_ward) {
      await setBaseIds();
      await getDataFromBackend();
      await setMuniOfficePin();
      setTimeout(() => {
        loadMap();
      }, 1000);
      let zoom = current_ward.defaultZoom;
      map.setView(muniLatlng, zoom);

      let userLocation = getCookie("userLoc");
      if (userLocation) {
        youAreHereLatlng = userLocation.split(",");
        setYouAreHere();
      } else {
        getBrowserLocation();
      }
      await getMapData();
    } else {
      //Load SA Map in Homepage
      let zoom = 6;
      map.setView([-29.68351, 24.70076], zoom);
    }
  }
  mapInit();

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
        "neighborhood",
        "colloquial_area",
      ],
      componentRestrictions: { country: "ZA" },
    };
    if (input) {
      const searchBox = new google.maps.places.Autocomplete(input, options);
      searchBox.addListener("place_changed", () => {
        const place = searchBox.getPlace();
        if (place.length == 0) {
          return;
        }
        const form = document.getElementById("redirect-to-closest-ward-form");
        form.querySelector(
          'input[name="longitude"]'
        ).value = place.geometry.location.lng();
        form.querySelector(
          'input[name="latitude"]'
        ).value = place.geometry.location.lat();
        form.querySelector('input[name="url"]').value =
          window.document.location.pathname;
        form.submit();
      });
    }
  }
  //Home and embed page search
  googlePlacesAutocomplete("address-search-input")
  //ward page search
  googlePlacesAutocomplete("nav-search-input")


  var loadMap = () => {
    if (muniAreaData.length > 0) {
      areas = L.geoJSON(muniAreaData, {
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
        var politicalParty = politicalParties[random(politicalParties.length)];
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
        var iconMarker = L.marker(layerCenter, {
          icon:L.icon({
            iconUrl: layer.feature.geometry.details.councillor_political_party_logo_url.value,
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
          e.target.setIcon(politicalParty["wardCouncillor"]["icon"]);
        });

        iconMarker.on("mouseout", (e) => {
          e.target.setIcon(L.icon({
            iconUrl: layer.feature.geometry.details.councillor_political_party_logo_url.value,
            iconSize: [40, 40],
            iconAnchor: [20, 20],
            className: "icon-marker",
            bubblingMouseEvents: true,
          }));
        });

        if (wardId == slug) {
          //ward office gotten using randomPointsOnPolygon
          var wardLatlng = randomPointsOnPolygon(
            1,
            layer.feature
          )[0].geometry.coordinates.reverse();

          var wardOffice = L.divIcon({
            className: "text-pin",
            iconAnchor: [40, 48],
            html: `<div>Ward office</div>`,
          });
          layer.setStyle({
            weight: 3,
            fillOpacity: 0.05,
            color: "#8334f7",
          });
          layer.bringToFront();
          map.fitBounds(layer.getBounds());

          L.marker(wardLatlng, {
            icon: wardOffice,
            riseOnHover: true,
            bubblingMouseEvents: true,
          }).addTo(map);
        }

        layer.on("click", (e) => {
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

  L.gridLayer
    .googleMutant({
      type: "roadmap",
    })
    .addTo(map);

  var politicalParties = [
    {
      wardCouncillor: {
        name: "Daniel Kapungwe",
        icon: L.icon({
          iconUrl: "../../../../static/assets/danielkapungwe.png",
          iconSize: [40, 40],
          iconAnchor: [20, 20],
          className: "icon-marker",
          bubblingMouseEvents: true,
        }),
      },
      party: {
        name: "ANC",
        icon: L.icon({
          iconUrl: "../../../../static/assets/anc.png",
          iconSize: [40, 40],
          iconAnchor: [20, 20],
          className: "icon-marker",
          bubblingMouseEvents: true,
        }),
      },
    },
    {
      wardCouncillor: {
        name: "Bukelani Zuma",
        icon: L.icon({
          iconUrl: "../../../../static/assets/bukelanizuma.png",
          iconSize: [40, 40],
          iconAnchor: [20, 20],
          className: "icon-marker",
          bubblingMouseEvents: true,
        }),
      },
      party: {
        name: "IFP",
        icon: L.icon({
          iconUrl: "../../../../static/assets/ifp.png",
          iconSize: [40, 40],
          iconAnchor: [20, 20],
          className: "icon-marker",
          bubblingMouseEvents: true,
        }),
      },
    },
    {
      wardCouncillor: {
        name: "Stuart Pringle",
        icon: L.icon({
          iconUrl: "../../../../static/assets/stuartpringle.png",
          iconSize: [40, 40],
          iconAnchor: [20, 20],
          className: "icon-marker",
          bubblingMouseEvents: true,
        }),
      },
      party: {
        name: "DA",
        icon: L.icon({
          iconUrl: "../../../../static/assets/da.png",
          iconSize: [40, 40],
          iconAnchor: [20, 20],
          className: "icon-marker",
          bubblingMouseEvents: true,
        }),
      },
    },
  ];

  var updateNeighbourMunicipalities = function () {
    var neighbourIds = Object.keys(municipality["neighbours"]);
    neighbourIds.forEach(function (neighbourId) {
      var neighbour = municipality["neighbours"][neighbourId];
      var parentAreaId = neighbour["parent_area"];

      if (neighbour["type"] === "WD") {
        fetch("https://mapit.code4sa.org/area/" + neighbourId + ".geojson")
          .then((response) => response.json())
          .then((data) => {
            var layer = L.geoJSON(data, {
              style: {
                color: "#ccc",
                fillOpacity: 0.01,
                weight: 2,
              },
            }).addTo(map);
            var popup = L.popup({
              className: "mapTooltip",
              closeButton: false,
            });
            popup.setContent(neighbour["name"]);
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
            //distant neighbours are unclickable because no 'slug' for them from backend
            layer.on("click", (e) => {
              if (
                window.document.location.pathname.endsWith("ward-councillor")
              ) {
                updateParentOrSelfLocationSearch(
                  `municipalities/${municipalityId}/wards/${slug}/ward-councillor`
                );
              } else {
                updateParentOrSelfLocationSearch(
                  `municipalities/${municipalityId}/wards/${slug}/`
                );
              }
            });

            layer.on("mouseover", (e) => {
              e.target.setStyle({
                color: "#999",
                fillOpacity: 0.05,
              });
              e.target.bringToFront();
            });

            layer.on("mouseout", (e) => {
              e.target.setStyle({
                color: "#ccc",
                fillOpacity: 0.01,
              });
              e.target.bringToBack();
            });
          })
          .catch((e) => console.log(e));
      }
    });
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
