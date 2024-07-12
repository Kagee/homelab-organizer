scanner = null
scanned_code_1 = null
scanned_code_2 = null
scan_action = null

function onScanSuccess(decodedText, _decodedResult) {
    // Handle on success condition with the decoded text or result.
    if (scanned_code_1 == null) {
        scanned_code_1 = decodedText
        console.log(`scanned code 1 = ${decodedText}`)
        $('#waiting-btn').html(scanner_data[scan_action]["second_msg"])
        $('#waiting-btn').addClass("btn-success")
        $('#waiting-btn').removeClass("btn-outline-success")
    }
    if (scanned_code_1 == decodedText) {
        return
    }
    if (scanned_code_2 == null) {
        scanned_code_2 = decodedText
        $('#waiting-btn').html("&nbsp;<br />...<br />&nbsp;")
        console.log(`scanned code 2 = ${decodedText}`)
    }
    console.log('Scan result: \nCode 1: ' + scanned_code_1 + '\nCode 2:' + scanned_code_2)
    scanner_data[scan_action]["result_func"](scanned_code_1, scanned_code_2)
    scanned_code_1 = null
    scanned_code_2 = null
    cancelScan()
}

function scan_ajax_result(post_url, scanned_code_1, scanned_code_2) {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    $.ajax
        ({
            url: post_url,
            data: { code1: scanned_code_1, code2: scanned_code_2 },
            type: 'post',
            headers: { 'X-CSRFToken': csrftoken },
            success: function (_data, _textStatus, jqXHR) {
                if (Object.hasOwn(jqXHR, 'responseJSON')) {
                    j = jqXHR.responseJSON
                    if (j["ok"]) {
                        $('#result-btn').removeClass("btn-outline-danger")
                        $('#result-btn').addClass("btn-outline-success")
                        $('#result-btn').html(j["result"]["msg"])
                        $('#result-div').show(0)
                    } else {
                        $('#result-btn').removeClass("btn-outline-success")
                        $('#result-btn').addClass("btn-outline-danger")
                        $('#result-btn').html(j["result"]["msg"])
                        $('#result-div').show(0)
                    }
                } else {
                    alert("Unknown response from backend")
                }
            },
            error: function (jqXHR, _textStatus, errorThrown) {
                if (Object.hasOwn(jqXHR, 'responseJSON')) {
                    alert(jqXHR.responseJSON)
                } else {
                    alert("Serverside error: \nHTTP " + jqXHR.status + " " + errorThrown)
                }
            }
        });
}

function move_item_to_storage(scanned_code_1, scanned_code_2)  {
    console.log("in function move_item_to_storage")
    scan_ajax_result(move_item_to_storage_url,scanned_code_1, scanned_code_2)
}

function move_storage_into_storage(scanned_code_1, scanned_code_2) {
    console.log("in function move_storage_into_storage")
    scan_ajax_result(move_storage_into_storage_url,scanned_code_1, scanned_code_2)
}

var scanner_data = {
    item_to_storage: {
        result_func: move_item_to_storage,
        first_msg: "&nbsp;<br />Please scan item to move...<br />&nbsp;",
        second_msg: "&nbsp;<br />Please scan target storage...<br />&nbsp;"
    },
    storage_into_storage: {
        result_func: move_storage_into_storage,
        first_msg: "&nbsp;<br />Please scan child storage...<br />&nbsp;",
        second_msg: "&nbsp;<br />Please parent child storage...<br />&nbsp;"
    }
}

function start_scan() {
    const config = { fps: 10, qrbox: { width: 200, height: 200 } };
    scanner.start({ facingMode: "environment" }, config, onScanSuccess);
    $("#cancel-btn").prop('disabled', false);
    $('#scan-div').hide()
    $('#result-div').hide()
    $('#waiting-btn').html(scanner_data[scan_action]["first_msg"])
    $('#waiting-div').show(0)
}

function cancelScan() {
    if (scanner) {
        scanner.stop();
    }
    scanned_code_1 = null
    scanned_code_2 = null
    scan_action = null
    $("#cancel-btn").prop('disabled', true);
    $('#waiting-div').hide(0)
    $('#scan-div').show(0)
    $('#waiting-btn').removeClass("btn-success")
    $('#waiting-btn').addClass("btn-outline-success")
    $('#waiting-btn').html("&nbsp;<br />Waiting for match...<br />&nbsp;")
}

function init_scanner() {
    // Set reader width to 95%
    z = Math.min(window.innerWidth, window.innerHeight) * 0.9;
    $("#reader").width(z)
    // setup a scanner
    scanner = new Html5Qrcode(
        "reader", {
        fps: 10,
        qrbox: 250,
        formatsToSupport: [
            Html5QrcodeSupportedFormats.QR_CODE
        ]
    });

    // Setup listeners for DOMs that may not have been created yet
    $("#scan-is-btn").on('click', function () {
        scan_action = "item_to_storage"
        start_scan()
    });
    $("#scan-ss-btn").on('click', function () {
        scan_action = "storage_into_storage"
        start_scan()
    });
    $("#cancel-btn").on('click', cancelScan);
}