var updateMapEmbed = function () {
  $(".data-src-wardid.data-src-municipalityid").attr(
    "src",
    "/map?municipalityid=" + municipalityId + "&wardid=" + wardId
  );
};
