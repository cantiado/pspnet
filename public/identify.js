const MDCMenu = mdc.menu.MDCMenu;
const menu = new MDCMenu(document.querySelector(".mdc-menu"));
// menu.open = true;

const menuButton = document.querySelector("#menu-button");
menuButton.addEventListener("click", () => {
  menu.open = true;
});

menuButton.addEventListener("click", () => {
  console.log("login button pressed")
})

const uploadedImageList = document.querySelector("#uploaded-image-list");
for (let i = 0; i < 25; i++) {
  const listItem = document.createElement("li");
  listItem.classList.add("mdc-image-list__item");
  const div1 = document.createElement("div");
  div1.classList.add("mdc-image-list__image-aspect-container");
  const image = document.createElement("img")
  image.classList.add("mdc-image-list__image")
  image.setAttribute("src", "./pink-square.png")
  const div2 = document.createElement("div")
  div2.classList.add("mdc-image-list__supporting")
  const span = document.createElement("span")
  span.classList.add("mdc-image-list__label")
  span.innerText = "file name"

  div1.appendChild(image)
  div2.appendChild(span)
  listItem.appendChild(div1)
  listItem.appendChild(div2)
  uploadedImageList.appendChild(listItem)
}
