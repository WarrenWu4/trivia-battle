// chip logic
const categories = ["General Knowledge", "Books", "Films & TV", "Music", "Video Games", "Science & Nature", "Math", "Mythology", "Sports", "Geography", "History", "Politics", "Art", "Celebrities", "Animals", "Vehicles", "Anime & Manga"]
const categoryIds = ["9", "10", "11,14", "12", "15", "17", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "31"]

const categoryContainer = document.getElementById("category-container")
const categoryEl = document.getElementById("category");
categoryEl.style.display = "none";
categoryEl.value = "9";
let active = 0;

categories.forEach((category, _idx) => {
  const chip = document.createElement("p")
  chip.classList = "chip neobrutalist"
  chip.textContent = category
  if (category === "General Knowledge") {
    chip.style.backgroundColor = "lightgreen";
  }
  categoryContainer.appendChild(chip)
})

for (let i = 0; i < categoryContainer.children.length; i++) {
    categoryContainer.children[i].addEventListener("click", function() {
    // 2 states: 1. active 2. inactive
    // if active, don't do anything
    // if inactive, set to active, set previous active to inactive
    if (categoryContainer.children[i].style.backgroundColor !== "lightgreen") {
      // set previous active to inactive
      categoryContainer.children[active].style.backgroundColor = "white";
      // set current to active
      categoryContainer.children[i].style.backgroundColor = "lightgreen";
      categoryEl.value = categoryIds[i];
      active = i;
    }
  })
}

const difficultyContainer = document.getElementById("difficulty-container")
const difficultyEl = document.getElementById("difficulty");
let difficultyActive = 0;

for (let i = 0; i < difficultyContainer.children.length; i++) {
    difficultyContainer.children[i].addEventListener("click", function() {
        if (difficultyContainer.children[i].style.backgroundColor !== "lightgreen") {
            difficultyContainer.children[difficultyActive].style.backgroundColor = "white";
            difficultyContainer.children[i].style.backgroundColor = "lightgreen";
            difficultyEl.value = difficultyContainer.children[i].textContent.toLowerCase()
            difficultyActive = i;
        }
  })
}

const gamemodeContainer = document.getElementById("gamemode-container")
const gamemodeEl = document.getElementById("gamemode");
let gamemodeActive = 0;

for (let i = 0; i < gamemodeContainer.children.length; i++) {
  gamemodeContainer.children[i].addEventListener("click", function() {
      if (gamemodeContainer.children[i].style.backgroundColor !== "lightgreen") {
          gamemodeContainer.children[gamemodeActive].style.backgroundColor = "white";
          gamemodeContainer.children[i].style.backgroundColor = "lightgreen";
          gamemodeEl.value = gamemodeContainer.children[i].textContent.toLowerCase()
          gamemodeActive = i;
      }
})
}

const funny = ["Toasty McButterpants", "Pickles Von Crunch", "Waffleton Sizzlebottom", "Nacho Cheeseholic", "Olive Q. Martini", "Jellybean Snickerdoodle", "Cornelius Popcornicus", "Pancake Fluffington", "Fluffy McSnoutface", "Bark Twain", "Meow Zedong", "Snappy Turtlepants", "Pawsitively Clawrence", "Quackers McDuckface", "Wiggly Wigglesworth", "Hootie Featherbottom", "Sprinkle Stardustington", "Glorbnax the Wobbly", "Zany Moonwhisker", "Bloop Fizzlewink", "Twinkle McFroggle", "Professor Quirkadoo", "Sir Bananington III", "Lady Zoodleflop", "Bytey McGiggles", "Wi-Fido Snarkington", "Clickety Clackerson", "Captain Debuggeroo", "Cache Memorykins", "Pixel Doodlebug", "Glitchy Von Zap", "Algo Rhythmicus", "Soggy Pants McGee", "Doodle McSquiggleface", "Bloopity Blorpington", "Chauncey Wobblebottom", "Snorkel Dingledoodle", "Lumpy Sporklebean", "Fizzlebop Zanytoes", "Wobblewoo Noodlebrain"]
const username = document.getElementById("username")
username.value = funny[Math.floor(Math.random() * funny.length)]

localStorage.setItem("domain_username", username.value)
username.addEventListener("input", () => {
  if (username.value === "") {
    username.value = funny[Math.floor(Math.random() * funny.length)]
  }
  localStorage.setItem("domain_username", username.value)
})