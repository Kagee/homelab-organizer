let wakeLockSupported = false;
let wakeLock = null;
let wakeLockStatus = 'off';
let wakeLockBtn = null;

const changeUI = (status = 'acquired') => {
    const acquired = status === 'acquired';
    console.log(`Wake lock status changed to ${status}`);
    if (!wakeLockBtn) return;
    if (acquired) {
        wakeLockBtn.classList.add("btn-danger");
        wakeLockBtn.classList.remove("btn-primary");
    } else {
        wakeLockBtn.classList.add("btn-primary");
        wakeLockBtn.classList.remove("btn-danger");
    }
};

// async function to request a wake lock
const requestWakeLock = async () => {
    try {
        wakeLock = await navigator.wakeLock.request('screen');
        wakeLockStatus = 'on';
        // change up our interface to reflect wake lock active
        changeUI();

        wakeLock.addEventListener('release', () => {
            // if wake lock is released alter the button accordingly
            changeUI('released');
        });

    } catch (err) {
        changeUI(`${err.name}, ${err.message}`);
    }
} // requestWakeLock()

function init_wakeLock() {
    // check if the browser supports wake lock API
    if ('wakeLock' in navigator) {
        wakeLockSupported = true;
        console.log("Wake lock supported");
    } else {
        console.log("Wake lock not supported");
        wakeLockBtn.style.display = 'none';
        return; // exit if not supported
    }

    wakeLockBtn = document.getElementById("wake-lock-btn");
   
    if (wakeLockSupported && wakeLockBtn) {
        wakeLockBtn.addEventListener('click', function() {
            
            // if wakelock is off request it
            console.log("Wake lock button pressed...");
            if (wakeLockStatus === 'off') {
                console.log("Requesting wake lock...");
                requestWakeLock();
            } else { // if it's on release it
                console.log("Releasing wake lock...");
                wakeLock.release()
                .then(() => {
                    wakeLock = null;
                    wakeLockStatus = 'off';
                });
            }
        });
        // re-request wake lock on visibility change
        // this is useful if the user switches tabs or minimizes the browser
        // and then returns to the page
        const handleVisibilityChange = () => {
            if (wakeLock !== null && document.visibilityState === 'visible') {
                requestWakeLock();
            }
          }
        document.addEventListener('visibilitychange', handleVisibilityChange);
    }
}