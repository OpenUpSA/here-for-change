var urlSearch = new URLSearchParams(window.location.search);
//var municipalityId = urlSearch.get("municipalityid");
//var wardId = urlSearch.get("wardid");
var municipalityId = 9152;
var wardId = 6775;

var municipality = {};

var updateMapEmbed = function () {
  $(".data-src-wardid.data-src-municipalityid").attr(
    "src",
    "/map?municipalityid=" + municipalityId + "&wardid=" + wardId
  );
};

if (municipalityId) {
  $.getJSON(
    "https://mapit.code4sa.org/area/" + municipalityId + ".json",
    (data) => {
      municipality["info"] = data;
    }
  );

  $.getJSON(
    "https://mapit.code4sa.org/area/" + municipalityId + "/children.json",
    (data) => {
      municipality["children"] = data;
    }
  );
}

updateMapEmbed();
