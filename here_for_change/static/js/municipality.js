var urlSearch = new URLSearchParams(window.location.search);
var municipalityId = urlSearch.get("municipalityid");
var wardId = urlSearch.get("wardid");

var municipality = {};

var updateMunicipalInfo = function () {
  $(".data-municipality-name").text(municipality["info"]["name"]);
  $(".data-href-municipality-id").attr(
    "href",
    "?municipalityid=" + municipalityId
  );
};

var updateMunicipalChildren = function () {
  Object.keys(municipality["children"]).forEach((key) => {
    var child = $(".data-template.data-municipal-child").clone();
    var childLink = child.find("a");
    childLink.attr(
      "href",
      "?municipalityid=" + municipalityId + "&wardid=" + key
    );
    childLink.text(municipality["children"][key]["name"]);
    child.removeClass("is-hidden");
    child.removeClass("data-template");
    child.appendTo(".data-has-children");
  });
};
