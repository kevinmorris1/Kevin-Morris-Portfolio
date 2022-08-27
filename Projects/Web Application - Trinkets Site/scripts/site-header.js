class siteHeader extends HTMLElement {
    connectedCallback() {
        this.innerHTML = `
            <div class="topnav">
                <a class="active" href="home.html">Home</a>
                <a href="counter.html">Counter</a>
                <a href="stopwatch.html">Stopwatch</a>
                <a href="clock.html">Clock</a>
            </div>
        `
    }
}

customElements.define('site-header', siteHeader)