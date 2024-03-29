// check compatability
var video = document.querySelector("#barcode-scanner");
var cameraOptions = document.querySelector("#camera-options");
var playButton = document.querySelector("#scan-button");
var barcodeResult = document.querySelector("#isbn");
let streamStarted = false;

const constraints = {
    video: {
        width: {
            min: 1280,
            ideal: 1920,
            max: 2560
        },
        height: {
            min: 720,
            ideal: 1080,
            max: 1440
        },
        facingMode: 'environment'
    }
}

const getCameraSelection = async () => {
    const devices = await navigator.mediaDevices.enumerateDevices();
    const videoDevices = devices.filter(device => device.kind === 'videoinput');
    const options = videoDevices.map(videoDevice => {
        var label = videoDevice.label;
        if (label === "") {
            label = `Camera ${videoDevice.kind}`;
        }
        return `<option value="${videoDevice.deviceId}">${label}</option>`;
    });
    cameraOptions.innerHTML = options.join('');
}

playButton.onclick = () => {
    if (streamStarted) {
        video.play();
        return
    }
    if ('mediaDevices' in navigator && navigator.mediaDevices.getUserMedia) {
        const updatedConstraints = {
            ...constraints,
            deviceId: {
                exact: cameraOptions.value
            }
        };
        startStream(updatedConstraints);
    }
}

const startStream = async (constraints) => {
    const stream = await navigator.mediaDevices.getUserMedia(constraints);
    handleStream(stream);
}

const handleStream = (stream) => {
    video.srcObject = stream;
    streamStarted = true;
}

Quagga.init({
    name: "Live",
    type: "LiveStream",
    constraints: {
        width: 640,
        height: 480,
        facingMode: "environment",
    },
    decoder: {
        readers: ["ean_reader"]
    },
    multiple: false,
}, function (err) {
    if (err) {
        console.log(err);
        return
    }
    console.log("Initialization finished. Ready to start.");
    Quagga.start();
    Quagga.onDetected(function (data) {
        console.log(data);
        barcodeResult.value = data.codeResult.code;
        video.autoplay = false
        streamStarted = false
    })
});

getCameraSelection();