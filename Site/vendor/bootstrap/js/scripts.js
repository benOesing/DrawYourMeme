  function execute(query) {
    console.log("Draw");
    $.ajax({
      type: 'POST',
      data: {},
      url: 'exec.php?' + query,
      success: function(response) {
        console.log(response);
        showGif();
        $("#linkP").removeAttr("style");
        $("#linkT").removeAttr("style");
        $("#linkT").attr("style", "width:500px");
        $("#linkT").val("https://www.drawyourmeme.com/Dankmemes/" + $("#newName").val() + ".gif")
      },
      error: function(response) {
        console.log(response);
      }
    });
  }


  function showGif() {
    document.getElementById("loading-pepe").style.display = "none"; //pepe
    console.log("Show");
    $("#result").attr("src", "Dankmemes/" + $('#newName').val() + ".gif");
    $("#result").removeAttr("style");
  }


  $(function() {
    $('#dataForm').on("submit", function(e) {
        document.getElementById("loading-pepe").style.display = "block";
      e.preventDefault();
      if (!$('#newName').val()) {
        console.log("Submit");
		if(!$('#border-size').val()){
			$('#border-size').val(0);
		}
        var file_data = $('#uploadFile').prop('files')[0];
        var form_data = new FormData();
        form_data.append('file', file_data);
        upload(form_data);
      } else {
        console.log("Already submitted");
        var newName = $('#newName').val();
        var parts = newName.split("_");
        newName = parts[0] + "_" + document.getElementById('mode').value;
        $('#newName').val(newName);
        var query = $('input').serialize() + "&" + $('select').serialize();
        execute(query);
      }
    });
  });


  function upload(form_data) {
    resizeImg(form_data);
    $.get("https://www.random.org/strings/?num=1&len=20&digits=on&upperalpha=on&loweralpha=on&unique=on&format=plain&rnd=new", function(response) {
      response = response.replace(/(\r\n|\n|\r)/gm, "");
      var style = document.getElementById('mode').value;
      $('#newName').val(response + "_" + style);
      $.ajax({
        url: "upload.php?a1=" + $('#newName').val(),
        data: form_data,
        dataType: 'text',
        cache: false,
        contentType: false,
        processData: false,
        type: 'post',
        success: function(response) {
          console.log(response);
          var newName = $('#newName').val();
          var query = $('input').serialize() + "&" + $('select').serialize();
          execute(query);
          console.log(query);
        },
        error: function(response) {
          console.log(response);
        }
      });
    });
  }


  function resizeImg(img_data) {
    console.log("Resize");

    var sizes = [];
    var ratio = 16 / 9;
    for (var i = 360; i <= 1980; i += 90) {
      var j = i * ratio;
      sizes.push([j, i]);
    }

    var img = new Image;
    var reader = new FileReader();
    reader.onload = function(e) {
      img.src = e.target.result;
      var oldw = img.width;
      var oldh = img.height;
      var w = 1024;
      var h = 768;
      var distance = w * h;
      var orientation = w > h;

      for (var i = 0; i < sizes.length; i++) {
        var d = w * h;
        if (orientation) {
          d = Math.abs(sizes[i][0] - oldw) + Math.abs(sizes[i][1] - oldh);
        } else {
          d = Math.abs(sizes[i][1] - oldw) + Math.abs(sizes[i][0] - oldh);
        }
        if (d < distance) {
          distance = d;
          if (orientation) {
            w = sizes[i][0];
            h = sizes[i][1];
          } else {
            w = sizes[i][1];
            h = sizes[i][0];
          }

        } else {
          break;
        }
      }

      var canvas = document.createElement('canvas');
      var ctx = canvas.getContext('2d');
      canvas.width = w;
      canvas.height = h;
      ctx.drawImage(img, 0, 0, w, h);
      var data = canvas.toDataURL();
      var blobBin = atob(data.split(',')[1]);
      var array = [];
      for (var i = 0; i < blobBin.length; i++) {
        array.push(blobBin.charCodeAt(i));
      }
      var file = new Blob([new Uint8Array(array)], {
        type: 'image/png'
      });
      img_data.set('file', file, 'blob.png');
    }
    reader.readAsDataURL(img_data.get("file"));
  }


  function showImage(input) {
    if (input.files && input.files[0]) {
      var reader = new FileReader();
      reader.onload = function(e) {
        $('#preview')
          .attr('src', e.target.result)
          .show();
          //.removeAttr("style");
        $('#preview').load(function() {
          $('#binarized')
            .show()
            //.removeAttr("style")
            .attr('src', binarize(128));
        });
        $('#slider').show();
      };
      reader.readAsDataURL(input.files[0]);
    }
  }


  function binarize(threshhold) {
    var imgObj = document.getElementById("preview");
    var canvas = document.createElement('canvas');
    var canvasContext = canvas.getContext('2d');

    var imgW = imgObj.width;
    var imgH = imgObj.height;
    canvas.width = imgW;
    canvas.height = imgH;

    canvasContext.drawImage(imgObj, 0, 0, imgW, imgH);
    var imgPixels = canvasContext.getImageData(0, 0, imgW, imgH);
    /*for (var y = 0; y < imgPixels.height; y++) {
      for (var x = 0; x < imgPixels.width; x++) {
        var i = (y * 4) * imgPixels.width + x * 4;
        var avg = (imgPixels.data[i] + imgPixels.data[i + 1] + imgPixels.data[i + 2]) / 3;
        if (avg < threshhold) {
          avg = 0;
        } else {
          avg = 255;
        }
        imgPixels.data[i] = avg;
        imgPixels.data[i + 1] = avg;
        imgPixels.data[i + 2] = avg;
      }
    }*/
	for (var y = 0; y < imgPixels.height; y++) {
                for (var x = 0; x < imgPixels.width; x++) {
                    var i = (y * 4) * imgPixels.width + x * 4;
                    var avg = (imgPixels.data[i] + imgPixels.data[i + 1] + imgPixels.data[i + 2]) / 3;
                    var oldAvg = avg;
                    if (avg <= threshhold) {
                        avg = 0;
                    } else {
                        avg = 255;
                    }
                    imgPixels.data[i] = avg;
                    imgPixels.data[i + 1] = avg;
                    imgPixels.data[i + 2] = avg;

                    var quant_error = oldAvg - avg;
                    imgPixels.data[i + 4] += quant_error * 7 / 16;
                    imgPixels.data[i - 4 + imgPixels.width * 4] += quant_error * 3 / 16;
                    imgPixels.data[i + imgPixels.width * 4] += quant_error * 5 / 16;
                    imgPixels.data[i + imgPixels.width * 4 + 4] += quant_error * 1 / 16;
                }
            }
    canvasContext.putImageData(imgPixels, 0, 0, 0, 0, imgPixels.width, imgPixels.height);
    return canvas.toDataURL();
  }