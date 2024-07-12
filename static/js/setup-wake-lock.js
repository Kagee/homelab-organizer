
let wakeLockSupported = false;
let wakeLock = null;
const changeUI = (status = 'acquired') => {
    const acquired = status === 'acquired' ? true : false;
    console.log(`Wake lock status changed to ${status}`)
    if (acquired) {
        $("#wake-lock-btn").addClass("btn-danger")
        $("#wake-lock-btn").removeClass("btn-primary")
        $("#wake-lock-btn").html(`Wake lock (press to unlock)`)
    } else {
        $("#wake-lock-btn").addClass("btn-primary")
        $("#wake-lock-btn").removeClass("btn-danger")
        $("#wake-lock-btn").html(`Wake lock (press to lock)`)
    }
}

let wakeButton = 'off';
// create an async function to request a wake lock
const requestWakeLock = async () => {
    try {
        wakeLock = await navigator.wakeLock.request('screen');
        wakeButton = 'on';
        // change up our interface to reflect wake lock active
        changeUI();

        // listen for our release event
        //wakeLock.onrelease = function(ev) {
        //    console.log(ev);
        //}
        wakeLock.addEventListener('release', () => {
            // if wake lock is released alter the button accordingly
            changeUI('released');
        });

    } catch (err) {
        changeUI(`${err.name}, ${err.message}`)
    }
} // requestWakeLock()

function init_wakeLock() {
    if ('wakeLock' in navigator) {
        wakeLockSupported = true;
        $("wake-lock-div").show(0)
        console.log("Wake lock supported")
    } else {
        $("wake-lock-div").hide()
        console.log("Wake lock not supported")
    }
    if (wakeLockSupported) {
        $("#wake-lock-btn").on('click', function() {
            // if wakelock is off request it
            if (wakeButton === 'off') {
                requestWakeLock()
            } else { // if it's on release it
                wakeLock.release()
                .then(() => {
                    wakeLock = null;
                    wakeButton = 'off';
                })
            }
        }); // $("#wake-lock-btn").on('click', function() {
        const handleVisibilityChange = () => {
            if (wakeLock !== null && document.visibilityState === 'visible') {
                requestWakeLock();
            }
          }
        document.addEventListener('visibilitychange', handleVisibilityChange);
    } // if (wakeLockSupported)

}