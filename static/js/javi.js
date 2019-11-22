const imgurEndpoint = 'https://api.imgur.com/3/upload';
var file = null;

function handleFiles(e) {
    var ctx = document.getElementById('canvas').getContext('2d');
    var reader  = new FileReader();
    file = e.target.files[0];
    // load the image to get its width/height
    var img = new Image();
    img.onload = function() {
        // scale canvas to image
        ctx.canvas.width = img.width;
        ctx.canvas.height = img.height;
        // draw image
        ctx.drawImage(img, 0, 0, ctx.canvas.width, ctx.canvas.height );
    }
    // this is to load the image
    reader.onloadend = function () {
        img.src = reader.result;
    }
    // this is to read the file
   	reader.readAsDataURL(file);
}

function uploadImage() {

    var reader  = new FileReader();

    reader.onloadend = function() {
        
        var dataURI = reader.result;

        var encoded = dataURI.split(',')[1];
        
        var request = new XMLHttpRequest();
    
        request.open("POST", imgurEndpoint);
    
        request.setRequestHeader('content-type', 'multipart/form-data');
        request.setRequestHeader("Authorization", "Client-ID a4383f1dbba5971");
        
        request.onreadystatechange = function() {
            if (request.readyState == XMLHttpRequest.DONE) {
                console.log(request.response);
                JSON.parse(request.response);
            }
        }
        
        request.send('image=' + encoded);
    }
    
    reader.readAsDataURL(file);

}