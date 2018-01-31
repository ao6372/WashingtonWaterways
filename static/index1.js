document.getElementById("submitButton").addEventListener("click", callCalcRoute)

function callCalcRoute(event) {
  event.preventDefault()

  console.log("hello")

  Lattitude = $("input#lat").val()
  Longitude = $("input#lon").val()
  Startyear = $("input#startyr").val()
  Endyear = $("input#endyr").val()

  values = {
    Lattitude: Lattitude,
    Longitude: Longitude,
    Startyear: Startyear,
    Endyear: Endyear
  }

  console.log(values)

  $.post({
    url: "/calculate",
    contentType: "application/json",
    data: JSON.stringify(values),
    success: function(result) {
      $(".hidden").css("display", "inline").html("Roots are ");
    }
  });
}
