var municipality = {};
var closestMuni = [];
var muniLatlng = [];
var current_ward = [];
var areas = [];
var youAreHereLatlng = [];
var muniAreaData = [];
var muniCoords = [];
var municipalityId = "";
var wardId = "";
var neighbouring_wards = [];
var wardAreaData = [];
var neighbourAreaData = [];
var baseUrl =
  window.document.location.href.split("/")[0] +
  "//" +
  window.document.location.href.split("/")[2];
var mapEl = document.querySelector("#map");

const coords = document.querySelectorAll(".coords");
const currentWard = document.querySelector(".current_ward");
const neighbouringWards = document.querySelectorAll(".neighbouring_wards");

if (currentWard) {
  current_ward = JSON.parse(currentWard.textContent);
}

if (neighbouringWards) {
  neighbouringWards.forEach((el) => {
    neighbouring_wards.push(JSON.parse(el.textContent));
  });
}

if (coords) {
  coords.forEach((el) => {
    muniCoords.push(JSON.parse(el.textContent));
  });
}

if (mapEl && baseUrl) {
  var map = L.map(mapEl);

  function getDataFromBackend() {
    municipality["municipality_area_number"] = current_ward.muniAreaNum;
    wardAreaData = current_ward.geometry;
    wardAreaData["name"] = current_ward.name;
    wardAreaData["slug"] = current_ward.slug;
    muniAreaData.push(wardAreaData);

    neighbouring_wards.forEach((neighbour) => {
      neighbourAreaData = neighbour.geometry;
      neighbourAreaData["name"] = neighbour["name"];
      neighbourAreaData["slug"] = neighbour["slug"];
      muniAreaData.push(neighbourAreaData);
    });
  }

  function setBaseIds() {
    if (
      window.document.location.pathname == "/" ||
      window.document.location.pathname == "/find-my-ward-councillor"
    ) {
      if (closestMuni.length > 0) {
        municipalityId = closestMuni[0].muniCode;
        wardId = closestMuni[0].slug;
        muniLatlng = closestMuni[0].coords;
      } else {
        // IF NO LOCATION, TO Load MAP IN CAPE AGULHAS
        municipalityId = "wc033";
        wardId = "wc033-cape-agulhas-ward-1";
        muniLatlng = [-34.4781, 19.9798];
      }
    } else {
      municipalityId = current_ward.muniCode;
      wardId = current_ward.slug;
      muniLatlng = current_ward.coords;
    }
    getMapData();
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
          muniAreaData.push(wardAreaData);

          neighbours.forEach((neighbour) => {
            neighbourAreaData = JSON.parse(neighbour.map_geoJson);
            let name = neighbour["name"];
            let slug = neighbour["slug"];
            neighbourAreaData["name"] = name;
            neighbourAreaData["slug"] = slug;
            muniAreaData.push(neighbourAreaData);
          });
        })
        .catch((e) => console.log(e));
    } else {
      getDataFromBackend();
    }

    await fetch(
      "https://mapit.code4sa.org/area/" +
        municipality["municipality_area_number"] +
        "/touches"
    )
      .then((response) => response.json())
      .then((data) => {
        municipality["neighbours"] = data;
        updateNeighbourMunicipalities();
      })
      .catch((e) => console.log(e))
      .then(() => {
        var zoom = current_ward.defaultZoom || 8;
        map.setView(muniLatlng, zoom);

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
      })
      .then(() => {
        setTimeout(() => {
          loadMap();
        }, 1000);
      });
  }

  function successLocation(position) {
    youAreHereLatlng.push(position.coords.longitude);
    youAreHereLatlng.push(position.coords.latitude);
    setYouAreHere();
    createCookie("userIP", youAreHereLatlng, 2);
  }

  function failedLocation() {
    alert("Please enable location permission");
    setBaseIds();
  }

  function getBrowserLocation() {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(successLocation, failedLocation);
    } else {
      alert("Geolocation not available");
    }
  }

  if (
    window.document.location.pathname == "/" ||
    window.document.location.pathname == "/find-my-ward-councillor"
  ) {
    getBrowserLocation();
  } else {
    setBaseIds();
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

  function getDistance(origin, destination) {
    // return distance in meters
    var lon1 = toRadian(origin[1]),
      lat1 = toRadian(origin[0]),
      lon2 = toRadian(destination[1]),
      lat2 = toRadian(destination[0]);

    var deltaLat = lat2 - lat1;
    var deltaLon = lon2 - lon1;

    var a =
      Math.pow(Math.sin(deltaLat / 2), 2) +
      Math.cos(lat1) * Math.cos(lat2) * Math.pow(Math.sin(deltaLon / 2), 2);
    var c = 2 * Math.asin(Math.sqrt(a));
    var EARTH_RADIUS = 6371;
    return c * EARTH_RADIUS * 1000;
  }
  function toRadian(degree) {
    return (degree * Math.PI) / 180;
  }

  function setClosestMuni() {
    let muniDiff = [];
    muniCoords.forEach((item) => {
      let distanceDiff = getDistance(youAreHereLatlng, item.coords);
      muniDiff.push({
        name: item.name,
        distFromUser: distanceDiff,
        slug: item.slug,
        muniCode: item.muniCode,
        coords: item.coords,
      });
    });
    closestMuni = muniDiff.sort((a, b) => a.distFromUser - b.distFromUser);
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

    if (muniCoords && youAreHereLatlng.length > 0) {
      setClosestMuni();
    }

    setBaseIds();
  }

  const locationBtn = document.querySelector("#location-btn");
  if (locationBtn) {
    locationBtn.addEventListener("click", locationBtnHandler);
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
        }, 2000);
      } else {
        alert("Geolocation not available");
      }
    }
  }

  function successRedirect(position) {
    youAreHereLatlng.push(position.coords.longitude);
    youAreHereLatlng.push(position.coords.latitude);
    if (muniCoords && youAreHereLatlng.length > 0) {
      setClosestMuni();
    }
    if (closestMuni.length > 0) {
      updateParentOrSelfLocationSearch(
        `municipalities/${closestMuni[0].muniCode}/wards/${closestMuni[0].slug}/`
      );
    }
  }

  function failedRedirect() {
    alert("Please enable location permission");
  }

  //embed location button handler
  const embedLocationBtn = document.querySelector("#embed-location-btn");
  if (embedLocationBtn) {
    embedLocationBtn.addEventListener("click", embedLocBtnHandler);
  }

  function embedLocBtnHandler() {
    const useLocationLoader = document.querySelector("#use-location-loader");
    if (useLocationLoader) {
      useLocationLoader.classList.remove("hidden");
      if (navigator.geolocation) {
        setTimeout(() => {
          navigator.geolocation.getCurrentPosition(
            embedRedirect,
            failedEmbedRedirect
          );
        }, 2000);
      } else {
        alert("Geolocation not available");
      }
    }
  }

  function embedRedirect(position) {
    youAreHereLatlng.push(position.coords.longitude);
    youAreHereLatlng.push(position.coords.latitude);
    if (muniCoords && youAreHereLatlng.length > 0) {
      setClosestMuni();
    }
    if (closestMuni.length > 0) {
      updateParentOrSelfLocationSearch(
        `municipalities/${closestMuni[0].muniCode}/wards/${closestMuni[0].slug}/ward-councillor`
      );
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

  // Create the search box and link it to the UI element.
  const input = document.getElementById("address-search-input");
  if (input) {
    const searchBox = new google.maps.places.SearchBox(input);
    // Listen for the event fired when the user selects a prediction and retrieve
    // more details for that place.
    searchBox.addListener("places_changed", () => {
      const places = searchBox.getPlaces();

      if (places.length == 0) {
        return;
      }
      const form = document.getElementById("redirect-to-closest-ward-form");
      form.querySelector(
        'input[name="longitude"]'
      ).value = places[0].geometry.location.lng();
      form.querySelector(
        'input[name="latitude"]'
      ).value = places[0].geometry.location.lat();
      form.querySelector(
        'input[name="url"]'
      ).value = window.document.location.pathname
      form.submit();
    });
  }

  var loadMap = () => {
    if (muniAreaData.length > 0) {
      areas = L.geoJSON(muniAreaData, {
        style: {
          color: "#999",
          fillOpacity: 0.01,
          weight: 2,
        },
      }).addTo(map);

      //load homepage map in the users nearest ward
      if (
        youAreHereLatlng.length > 0 &&
        window.document.location.pathname == "/"
      ) {
        var posMarker = L.marker(youAreHereLatlng, {
          riseOnHover: true,
          bubblingMouseEvents: true,
        });

        var userClosestWard = [];
        //check if user position is inside polygon
        areas.eachLayer(function (memberLayer) {
          if (memberLayer.getBounds().contains(posMarker.getLatLng())) {
            userClosestWard.push(memberLayer.feature.geometry.slug);
          }
        });
        if (userClosestWard.length > 0) {
          wardId = userClosestWard[0];
        }
      }

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
          icon: politicalParty["party"]["icon"],
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
          `${politicalParty["party"]["name"]} - ${politicalParty["wardCouncillor"]["name"]}`,
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
          e.target.setIcon(politicalParty["party"]["icon"]);
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
    } else {
      //setTimeout(loadMap, 1000);
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
}
