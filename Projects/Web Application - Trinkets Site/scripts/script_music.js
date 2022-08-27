const kits = ["we_did_it_kid"];

const containerEl = document.querySelector(".button start");

kits.for((kit) => {
  const audioEl = document.createElement("audio");
  audioEl.src = "sounds/" + kit + ".mp3";
  containerEl.appendChild(audioEl);
  btnEl.addEventListener("click", () => {
    audioEl.play();
  });
  
});