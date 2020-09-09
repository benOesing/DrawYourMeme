for (var y = 0; y < imgPixels.height; y++) {
                for (var x = 0; x < imgPixels.width; x++) {
                    var i = (y * 4) * imgPixels.width + x * 4;
                    var avg = (imgPixels.data[i] + imgPixels.data[i + 1] + imgPixels.data[i + 2]) / 3;
                    var oldAvg = avg;
                    if (avg < threshhold) {
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