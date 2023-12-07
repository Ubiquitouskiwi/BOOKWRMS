// check compatability
var video = document.querySelector("#barcode-scanner");
var cameraOptions = document.querySelector("#camera-options");
var playButton = document.querySelector("#play-button");
let streamStarted = false;

const constraints = {
    video: {
        width: {
            min: 480,
            ideal: 1920,
            max: 2560
        },
        height: {
            min: 480,
            ideal: 1080,
            max: 1440
        }
    }
}

const getCameraSelection = async () => {
    const devices = await navigator.mediaDevices.enumerateDevices();
    const videoDevices = devices.filter(device => device.kind === 'videoinput');
    const options = videoDevices.map(videoDevice => {
        return `<option value="${videoDevice.deviceId}">${videoDevice.label}</option>`;
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
    streamStarted = ture;
}

getCameraSelection();


// getCameraSelection();

// if (navigator.mediaDevices.getUserMedia) {
//     navigator.mediaDevices.getUserMedia({ video: true }).then(function (stream) {
//         video.srcObject = stream;
//     }).catch(function (err) {
//         console.log(err);
//     });
// }


// Quagga.init({
//     inputStream: {
//         name: "Live",
//         type: "LiveStream",
//         target: document.querySelector("#barcode-scanner")
//     },
//     decoder: {
//         readers: ["code_128_reader", "ean_reader"]
//     },
//     multiple: false,
//     halfSample: false,
// }, function (err) {
//     if (err) {
//         console.log(err);
//         return
//     }
//     console.log("Initialization finished. Ready to start.");
//     Quagga.start();
//     Quagga.onDetected(function (data) {
//         console.log(data);
//     })
// })