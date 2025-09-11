$(document).ready(function () {
  carregarPagina("dash");
  $(".logoutbutton").click(function () {
    window.location.href = "logout";
  });
  $(".panel li").click(function () {
    $(".panel li").removeClass("panelclicked");
    $(this).addClass("panelclicked");

    let url = $(this).attr("id");
    carregarPagina(url);
  });
});

function carregarPagina(url) {
  $("#main").attr("src", url);
}
