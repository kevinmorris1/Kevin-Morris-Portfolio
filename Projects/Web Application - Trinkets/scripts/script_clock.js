const hourEl = document.querySelector(".hour");
const minuteEl = document.querySelector(".minute");
const secondEl = document.querySelector(".second");
const dateEl = document.querySelector(".date p");

function updateClock() {
    const currentDate = new Date();
    setTimeout(updateClock, 1000)
    const hour = currentDate.getHours(); 
    const minute = currentDate.getMinutes(); 
    const second = currentDate.getSeconds();
    const date = currentDate.getDate();
    
    const hourDeg = (hour/12)*360;
    const minDeg = (minute/60)*360;
    const secDeg = (second/60)*360;

    hourEl.style.transform = `rotate(${hourDeg}deg)`;
    minuteEl.style.transform = `rotate(${minDeg}deg)`;
    secondEl.style.transform = `rotate(${secDeg}deg)`;
    dateEl.innerText = date;
}

setInterval(updateClock, 1000);