var municipality = {};
var baseUrl =
  window.document.location.href.split("/")[0] +
  "//" +
  window.document.location.href.split("/")[2];
var mapEl = document.querySelector("#map");

if (mapEl && baseUrl) {
  var map = L.map(mapEl);
  var latlng = [];
  var zoom = 8;
  var areas = [];
  var youAreHereLatlng = [];
  let muniAreaData = [];

  if (window.document.location.pathname == "/") {
    var municipalityId = "wc033";
    var wardId = "wc033-cape-agulhas-ward-1";
  } else {
    let path =
      window.document.location.href.split("/municipalities")[1] || "///";
    var municipalityId = path.split("/")[1];
    var wardId = path.split("/")[3];
  }

  fetch(`${baseUrl}/municipalities/${municipalityId}/wards/${wardId}.json`)
    .then((response) => response.json())
    .then((data) => {
      let { neighbours, map_geoJson, name, slug } = data;
      municipality["municipality_area_number"] =
        data["municipality"]["area_number"];
      let wardAreaData = JSON.parse(map_geoJson);
      wardAreaData["name"] = name;
      wardAreaData["slug"] = slug;
      muniAreaData.push(wardAreaData);

      neighbours.forEach((neighbour) => {
        let neighbourAreaData = JSON.parse(neighbour.map_geoJson);
        let name = neighbour["name"];
        let slug = neighbour["slug"];
        neighbourAreaData["name"] = name;
        neighbourAreaData["slug"] = slug;
        muniAreaData.push(neighbourAreaData);
      });
    })
    .then(() => {
      fetch(
        "https://mapit.code4sa.org/area/" +
          municipality["municipality_area_number"] +
          "/touches"
      )
        .then((response) => response.json())
        .then((data) => {
          municipality["neighbours"] = data;
          updateNeighbourMunicipalities();
        });

      fetch(
        "https://mapit.code4sa.org/area/" +
          municipality["municipality_area_number"] +
          "/geometry"
      )
        .then((response) => response.json())
        .then((data) => {
          municipality["geometry"] = data;
          latlng = [
            municipality["geometry"]["centre_lat"],
            municipality["geometry"]["centre_lon"],
          ];
          map.setView(latlng, zoom);

          var municipalOffice = L.divIcon({
            className: "text-pin is-filter-grayscale-bw is-pointer-events-none",
            iconAnchor: [52, 48],
            html: "<div>Municipal office</div>",
            interactive: false,
          });

          L.marker(latlng, {
            icon: municipalOffice,
            riseOnHover: true,
            bubblingMouseEvents: true,
          }).addTo(map);
        });
    })
    .then(() => {
      setTimeout(() => {
        loadMap();
      }, 1000);
    });

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

  function getBrowserLocation() {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition((position) => {
        youAreHereLatlng.push(position.coords.latitude);
        youAreHereLatlng.push(position.coords.longitude);
        setYouAreHere();
      });
    }
  }
  getBrowserLocation();

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

  // var inside = [-34.63778, 19.85581]
  // var outside = [-34.390567, 19.132697]

  // var insideDiv = L.divIcon({
  //   className: "text-pin is-filter-contrast-high is-pointer-events-none",
  //   iconAnchor: [42, 48],
  //   html: "<div>Inside</div>",
  //   interactive: false,
  // });

  // var insideMarker = L.marker(inside, {
  //   icon: insideDiv,
  //   riseOnHover: true,
  //   bubblingMouseEvents: true,
  // }).addTo(map);

  // var outsideDiv = L.divIcon({
  //   className: "text-pin is-filter-contrast-high is-pointer-events-none",
  //   iconAnchor: [42, 48],
  //   html: "<div>outside</div>",
  //   interactive: false,
  // });

  // var outsideMarker = L.marker(outside, {
  //   icon: outsideDiv,
  //   riseOnHover: true,
  //   bubblingMouseEvents: true,
  // }).addTo(map);

  // function getDistance(origin, destination) {
  //   // return distance in meters
  //   var lon1 = toRadian(origin[1]),
  //     lat1 = toRadian(origin[0]),
  //     lon2 = toRadian(destination[1]),
  //     lat2 = toRadian(destination[0]);

  //   var deltaLat = lat2 - lat1;
  //   var deltaLon = lon2 - lon1;

  //   var a =
  //     Math.pow(Math.sin(deltaLat / 2), 2) +
  //     Math.cos(lat1) * Math.cos(lat2) * Math.pow(Math.sin(deltaLon / 2), 2);
  //   var c = 2 * Math.asin(Math.sqrt(a));
  //   var EARTH_RADIUS = 6371;
  //   return c * EARTH_RADIUS * 1000;
  // }
  // function toRadian(degree) {
  //   return (degree * Math.PI) / 180;
  // }
  // var auchiDistance = getDistance([9.0765, 7.3986], [7.0669, 6.2748]);
  // var enuguDistance = getDistance([9.0765, 7.3986], [6.4483, 7.5139]);
    

  var loadMap = () => {
    if (muniAreaData.length > 0) {
      areas = L.geoJSON(muniAreaData, {
        style: {
          color: "#999",
          fillOpacity: 0.01,
          weight: 2,
        },
      }).addTo(map);

      //check if point is inside polygon
      // areas.eachLayer(function(memberLayer) {
      //   console.log("mem",memberLayer);
      //   if (memberLayer.getBounds().contains(insideMarker.getLatLng())) {
      //     console.log(memberLayer.feature.geometry.name);
      //   } 
      // });
      
      areas.getLayers().forEach((layer) => {
        var slug = layer.feature.geometry.slug;
        var name = layer.feature.geometry.name;
        var layerCenter = layer.getBounds().getCenter();
        var politicalParty = politicalParties[random(politicalParties.length)];
        var popup = L.popup({ className: "tooltip", closeButton: false });
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
          updateParentOrSelfLocationSearch(
            `municipalities/${municipalityId}/wards/${slug}/`
          );
        });

        iconMarker.bindTooltip(
          `${politicalParty["party"]["name"]} - ${politicalParty["wardCouncillor"]["name"]}`,
          {
            direction: "top",
            offset: [0, -16],
            className: "tooltip",
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
          //ward office is using randomPointsOnPolygon
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
          updateParentOrSelfLocationSearch(
            `municipalities/${municipalityId}/wards/${slug}/`
          );
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
      setTimeout(loadMap, 1000);
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
          iconSize: [32, 32],
          iconAnchor: [16, 16],
          className: "icon-marker",
          bubblingMouseEvents: true,
        }),
      },
      party: {
        name: "ANC",
        icon: L.icon({
          iconUrl: "../../../../static/assets/anc.png",
          iconSize: [32, 32],
          iconAnchor: [16, 16],
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
          iconSize: [32, 32],
          iconAnchor: [16, 16],
          className: "icon-marker",
          bubblingMouseEvents: true,
        }),
      },
      party: {
        name: "IFP",
        icon: L.icon({
          iconUrl: "../../../../static/assets/ifp.png",
          iconSize: [32, 32],
          iconAnchor: [16, 16],
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
          iconSize: [32, 32],
          iconAnchor: [16, 16],
          className: "icon-marker",
          bubblingMouseEvents: true,
        }),
      },
      party: {
        name: "DA",
        icon: L.icon({
          iconUrl: "../../../../static/assets/da.png",
          iconSize: [32, 32],
          iconAnchor: [16, 16],
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
              className: "tooltip",
              closeButton: false,
            });
            popup.setContent(neighbour["name"]);
            layer.bindPopup(popup);

            layer.on("mouseover", function (e) {
              var popup = e.target.getPopup();
              popup.setLatLng(latlng).openOn(map);
            });

            layer.on("mouseout", function (e) {
              e.target.closePopup();
            });

            layer.on("mousemove", function (e) {
              popup.setLatLng(e.latlng).openOn(map);
            });
            //distant neighbours are unclickable because no 'slug' for them from backend
            layer.on("click", (e) => {
              updateParentOrSelfLocationSearch(
                `municipalities/${parentAreaId}/wards/${slug}/`
              );
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
          });
      }
    });
  };
}