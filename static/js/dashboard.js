$(document).ready(function () {
  // INFO: load default page
  carregarPagina("dash");

  $(".logoutbutton").click(function () {
    window.location.href = "logout";
  });

  // INFO: handle sidebar navigation
  $("aside ul li a").click(function (e) {
    e.preventDefault(); // INFO: prevent default anchor behavior

    $("aside ul li").removeClass("panelclicked");
    $(this).parent().addClass("panelclicked");

    let url = $(this).parent().attr("id");
    carregarPagina(url);
  });
});

function carregarPagina(url) {
  // INFO: load partial HTML into main container
  $("#main").load("/" + url);
}