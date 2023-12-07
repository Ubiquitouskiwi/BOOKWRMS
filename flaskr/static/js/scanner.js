// check compatability
var video = document.querySelector("#barcode-scanner");

if (navigator.mediaDevices.getUserMedia) {
    navigator.mediaDevices.getUserMedia({ video: true }).then(function (stream) {
        video.srcObject = stream;
    }).catch(function (err) {
        console.log(err);
    });
}


Quagga.init({
    inputStream: {
        name: "Live",
        type: "LiveStream",
        target: document.querySelector("#barcode-scanner")
    },
    decoder: {
        readers: ["code_128_reader", "ean_reader"]
    },
    multiple: false,
    halfSample: false,
}, function (err) {
    if (err) {
        console.log(err);
        return
    }
    console.log("Initialization finished. Ready to start.");
    Quagga.start();
    Quagga.onDetected(function (data) {
        console.log(data);
    })
})