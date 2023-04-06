function openCam(){
    let allMediaDevices = navigator.mediaDevices
    if (!allMediaDevices || !allMediaDevices.getUserMedia){
        console.log("getUserMedia() no supported");
        return;
    }
    allMediaDevices.getUserMedia({
        video:true
    })
    .then(function(vidStream) {
        var video = document.getElementById('videoCam');
        if ('srcObject' in video) {
            video.srcObject = vidStream;
        } else {
            video.src = window.URL.createObjectURL(vidStream);
        }
        video.onloadedmetadata = function(e) {
            video.play()
        };
    })
    .catch(function(e) {
        console.log(e.name + ':' + e.message);
    })
}
function onScanSuccess(decodedText, decodedResult){
    console.log('Code scanned = ${decodedText}', decodedResult);
    window.location.href = '/scanner/output/' + decodedText
}
function scanBarcode() {
    let scannerConfig = {
        fps: 10, 
        rqbox: 250,
        rememberLastUsedCamera: true,
        aspectRatio: 1.777778,
        rqbox: {
            width: 400, 
            height: 150 }
        };
    
    let scanner = new Html5QrcodeScanner(
        "qr-reader", scannerConfig );
    scanner.render(onScanSuccess);
}