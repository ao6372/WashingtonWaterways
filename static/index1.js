
  submit = function(){
    lat = $("input#lat").val()
    lon = $("input#lon").val()
    startyr = $("input#startyr").val()
    endyr = $("input#endyr").val()
    thresh=$("input#thresh").val()

    values = {lat : lat,
      lon : lon,
      startyr : startyr,
      endyr: endyr}

    console.log(values)

    $.post({
      url: "/calculate",
    contentType: "application/json",
    data: JSON.stringify(values),
    success: function(result){
      $(".hidden").css("display","inline").html("Roots are ");
    }
    });
  }
