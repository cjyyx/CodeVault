
function draw(rgb_array) {
    /* 将RGB数组表示的图片绘制到Canvas上 */
    var c = document.getElementById("myCanvas");
    var ctx = c.getContext("2d");

    width=rgb_array[0].length;
    height=rgb_array.length;


    var imgData = ctx.createImageData(width,height);

    for(var i=0;i<height;i++){
        for(var j=0;j<width;j++){
            imgData.data[i*4*width+j*4]=rgb_array[i][j][0];
            imgData.data[i*4*width+j*4+1]=rgb_array[i][j][1];
            imgData.data[i*4*width+j*4+2]=rgb_array[i][j][2];
            imgData.data[i*4*width+j*4+3]=255;
        }
    }
    ctx.putImageData(imgData, 10, 10);
    console.log("ok");
}