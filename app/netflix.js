//@ sourceURL=twitflix.js

const PRINT_MEDIA_NAMES = false;

// The current active tile as: (tile ID, associated boxart node).
var activeTile = null;

// All media names we know of so far.
const mediaNames = new Set();


// A unique tile ID.
function newTileID() {
  _tileID++;
  return `twitflix-${_tileID - 1}`;
}
var _tileID = 1;


// Return a new tile of given size and position.
function newTile(tileID, height, width, left, top, name) {
  var tile = document.createElement('div');
  tile.id = tileID;
  tile.className = 'twitflix-tile';
  tile.style.height = `${height}px`;
  tile.style.width = `${width}px`;
  tile.style.position = 'absolute';
  tile.style.left = `${left}px`;
  tile.style.top =
    `${top - document.body.getBoundingClientRect().top - height}px`;
  tile.innerHTML = 'Hi...';
  return tile;
}


// Reposition the currently active tile.
// Need this since the boxart may change size on hover.
function repositionTiles() {
  // const bobplays = document.getElementsByClassName('bobplay-hitzone');
  // if (bobplays.length == 1) {
  //   document.getElementById(activeTile[0])
  // }
}


// Show a new tile above the given boxart element.
// Removes the previous tile if it exists.
function showNewTile(link, boxart, name) {
  const height = boxart.clientHeight;
  const width = boxart.clientWidth;
  const boxPosition = boxart.getBoundingClientRect();
  const tileID = newTileID();
  const tile = newTile(
    tileID, height, width, boxPosition.left, boxPosition.top, name);
  if (activeTile) {
    const activeTileNode = document.getElementById(activeTile[0]);
    activeTileNode.parentElement.removeChild(activeTileNode);
  }
  document.body.insertBefore(tile, document.body.firstChild);
  activeTile = [tileID, boxart];
}


// Register handlers to show tiles on media on hover.
function registerTiles() {
  var links = document.links;
  for (var i = 0; i < links.length; i++) {
    const name = links[i].getAttribute("aria-label");
    if (name && name != "Play" && links[i].href.includes("watch")) {
      if (!mediaNames.has(name)) {
        mediaNames.add(name);
        if (PRINT_MEDIA_NAMES)
          console.log(Array.from(mediaNames));
      }
      const boxart = links[i].firstChild;
      boxart.onmouseenter = () => showNewTile(links[i], boxart, name);
    }
  }
}


console.log('Twitflix running...');
registerTiles();
document.onscroll = registerTiles;
