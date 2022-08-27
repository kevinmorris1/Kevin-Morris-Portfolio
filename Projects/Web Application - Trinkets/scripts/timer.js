const time_el = document.querySelector('.timer-container .timer-time');
const start_btn = document.getElementById('start');
const pause_btn = document.getElementById('pause');
const reset_btn = document.getElementById('reset');

let time = 0;
let interval = null;


start_btn.addEventListener('click', start);
pause_btn.addEventListener('click', pause);
reset_btn.addEventListener('click', reset);


function timer () {
    time++;
    let hsecs = time % 100;
    let secs = Math.floor(time / 100);
    let mins = Math.floor(secs / 60);
    let hrs = Math.floor(mins / 60);

    secs = secs % 60;
    mins = mins % 60;
    hrs = hrs % 24;

    if (hsecs < 10) hsecs = '0' + hsecs;
    if (secs < 10) secs = '0' + secs;
    if (mins < 10) mins = '0' + mins;
    if (hrs < 10) hrs = '0' + hrs;

    time_el.innerText = `${hrs}:${mins}:${secs}.${hsecs}`;
}

function start () {
    if (interval) {
        return
    }
    interval = setInterval(timer, 10);
}

function pause () {
    clearInterval(interval);
    interval = null;
}

function reset () {
    stop();
    time=0;
    time_el.innerText = '00:00:00.00';
}