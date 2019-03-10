//@ sourceURL=twitflix.js

// Whether to print out new media names when discovered.
const PRINT_MEDIA_NAMES = false;

// The current active tile as: (tile ID, associated boxart node).
var activeTile = null;

// All media names we know of so far.
const mediaNames = new Set();


// An identifier to uniquely identify a Twitflix tile.
function newTileID() {
  _tileID++;
  return `twitflix-${_tileID - 1}`;
}
var _tileID = 1;


// Return a new Twitflix tile node of given size, position and media data.
//
// The node is not yet attached to the DOM.
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


// A new Twitflix tile is added to the DOM, above the given boxart element.
//
// Removes the current active tile if it exists. Also registers a function to
// resize the tile if the media box resizes or the page resizes.
function showNewTile(boxart, name) {
  const height = boxart.clientHeight;
  const width = boxart.clientWidth;
  const boxPosition = boxart.getBoundingClientRect();
  const tileID = newTileID();
  const tile = newTile(
    tileID, height, width, boxPosition.left, boxPosition.top, name);
  if (activeTile) {
    const activeTileNode = document.getElementById(activeTile[0]);
    activeTileNode.className += " twitflix-tile-fade-out";
    setTimeout(() => {
      activeTileNode.parentElement.removeChild(activeTileNode);
    }, 600);
  }
  document.body.insertBefore(tile, document.body.firstChild);
  activeTile = [tileID, boxart];
}


// Register handlers to show Twitflix tiles above media boxes on mouse enter.
//
// The handler will not run if a Twitflix tile already exists for that media.
//
// Only media shown on the page is affected, so this function should be run
// again on page scroll.
function registerTilesOnPage() {
  const namesAndBoxarts = getNamesAndBoxarts();
  for (var i = 0; i < namesAndBoxarts.length; i ++) {
    const name = namesAndBoxarts[i][0];
    const boxart = namesAndBoxarts[i][1];
    if (!mediaNames.has(name)) {
      mediaNames.add(name);
      if (PRINT_MEDIA_NAMES)
        console.log(Array.from(mediaNames));
    }
    boxart.onmouseenter = () => {
      if (!activeTile || activeTile[1] != boxart)
        showNewTile(boxart, name);
    };
  }
}


// Reposition and resize the currently active Twitflix tile.
//
// This is needed since the media boxes change size on hover.
function resetActiveTile() {
    const bobplays = document.getElementsByClassName('bobplay-hitzone');
    if (bobplays.length > 0) {
        document.getElementById(activeTile[0]);
        console.log(`bobplays.length = ${bobplays.length}`);
        console.log(bobplays);
    }
}


////////////////////////////////////////////////////////////////////////////////
// Functions to find data in the Netflix page. /////////////////////////////////
////////////////////////////////////////////////////////////////////////////////


// Return a list of (String, HtmlElement), film names and box art element.
//
// There may be multiple HtmlElements for the same film name.
function getNamesAndBoxarts() {
  const tuples = [];
  const links = document.links;
  for (var i = 0; i < links.length; i++) {
    const name = links[i].getAttribute("aria-label");
    const boxart = links[i].firstChild;
    if (name && name != "Play" && links[i].href.includes("watch"))
      tuples.push([name, boxart]);
  }
  return tuples;
}


console.log('Twitflix running...');
registerTilesOnPage();
document.onscroll = registerTilesOnPage;
