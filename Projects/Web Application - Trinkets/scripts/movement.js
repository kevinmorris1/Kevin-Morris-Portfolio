let circle = document.querySelector('.circle');
let move = 10;

window.addEventListener('load', () => {
    circle.style.position = 'absolute';
    circle.style.left = 150 + 'px';
    circle.style.top = 150 + 'px';
});

window.addEventListener('keyup', (e) => {
    switch (e.key) {
        case 'ArrowLeft':
            circle.style.left = parseInt(circle.style.left) - move + 'px';
            break;
        case 'ArrowRight':
            circle.style.left = parseInt(circle.style.left) + move + 'px';
            break;
        case 'ArrowUp':
            circle.style.top = parseInt(circle.style.top) - move + 'px';
            break;
        case 'ArrowDown':
            circle.style.top = parseInt(circle.style.top) + move + 'px';
            break;
    }
});