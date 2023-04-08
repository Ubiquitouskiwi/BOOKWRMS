function openCam() {
    let allMediaDevices = navigator.mediaDevices;
    if (!allMediaDevices || !allMediaDevices.getUserMedia) {
        console.log("getUserMedia() not supported.");
        return;
    }
    allMediaDevices.getUserMedia({
        video: true
    })
    .then(function(vidStream) {
        var video = document.getElementById('videoCam');
        if ("srcObject" in video) {
            video.srcObject = vidStream;
        } else {
            video.src = window.URL.createObjectURL(vidStream);
        }
        video.onloadedmetadata = function(e) {
            video.play();
        };
    })
    .catch(function(e) {
        console.log(e.name + ": " + e.message);
    });
}

function dercodeOnce(codeReader, selectedDeviceId) {
    codeReader.decodeFromInputVideoDevice(selectedDeviceId, 'video').then((result) => {
        console.log(result);
        document.getElementById('result').textContent = result.text;
        window.location.href = '/scanner/output/' + result.text;
    }).catch((err) => {
        console.log(err);
        document.getElementById('result').textContent = err;
    })
}

function decodeContinuously(codeReader, selectedDeviceId) {
    codeReader.decodeFromInputVideoDeviceContinuously(selectedDeviceId, 'video', (result, err) => {
        if (result) {
            // Properly decoded qr code
            console.log('Found code: ', result);
            document.getElementById('result').textContent = result.text;
            window.location.href = '/scanner/output/' + result.text;
            return;
        }

        if (err) {
            if (err instanceof ZXing.NotFoundException) {
                console.log('No code found.');
            }

            if (err instanceof ZXing.ChecksumException) {
                console.log('A code was found, but it\'s read value was not valid.');
            }

            if (err instanceof ZXing.FormatException) {
                console.log('A code was found, but it was in an invalid format.');
            }
        }
    })
}

window.addEventListener('load', function() {
    let selectedDeviceId;
    const codeReader = new ZXing.BrowserMultiFormatReader();
    console.log('ZXing code reader initialized');

    codeReader.getVideoInputDevices()
        .then((videoInputDevices) => {
            const sourceSelect = document.getElementById('sourceSelect');
            selectedDeviceId = videoInputDevices[0].deviceId;
            if (videoInputDevices.length >= 1) {
                videoInputDevices.forEach((element) => {
                    const sourceOption = document.createElement('option');                        
                    sourceOption.text = element.label;
                    sourceOption.value = element.deviceId;
                    sourceSelect.appendChild(sourceOption);
                })

                sourceSelect.onchange = () => {
                    selectedDeviceId = sourceSelect.value;
                };

                const sourceSelectPanel = document.getElementById('sourceSelectPanel');
                sourceSelectPanel.style.display = 'block';
            }

            document.getElementById('startButton').addEventListener('click', () => {
                const decodingStyle = document.getElementById('decoding-style').value;

                if (decodingStyle == 'once') {
                    dercodeOnce(codeReader, selectedDeviceId);
                } else {
                    decodeContinuously(codeReader, selectedDeviceId);
                }

                console.log('Started decode from camera with id ${selectedDeviceId}');
            })

            document.getElementById('resetButton').addEventListener('click', () => {
                codeReader.reset();
                document.getElementById('result').textContent = '';
                console.log('Reset.');
            })
        })
        .catch((err) => {
            console.err(err);
        })
})