document.getElementById("submitButton").addEventListener("click", callCalcRoute)

function callCalcRoute(event) {
  event.preventDefault()

  console.log("hello")

  latitude = $("input#lat").val()
  longitude = $("input#lon").val()
  startyear = $("input#startyr").val()
  endyear = $("input#endyr").val()
  // thresh=$("input#thresh").val()

  values = {
    lat: latitude,
    lon: longitude,
    startyr: startyear,
    endyr: endyear
    thresh:thresh
        }

  console.log(values)

  $.post({
    url: "/calculate",
    contentType: "application/json",
    data: JSON.stringify(values),
    success: function(result) {
      $(".hidden").css("display", "inline").html("");
    }
  });
}
