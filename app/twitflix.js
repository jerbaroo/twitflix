//@ sourceURL=twitflix.js

// Whether to print out new media names when discovered.
const PRINT_MEDIA_NAMES = false;

// The current active tile as: (ID, media name, boxart element).
var activeTile = null;

// All media names we know of so far.
const mediaNames = new Set();


// An identifier to uniquely identify a Twitflix tile.
function newTileID() {
  _tileID++;
  return `twitflix-${_tileID - 1}`;
}
var _tileID = 1;


// Return a new Twitflix tile of given size, position and media data.
//
// The tile is not yet attached to the DOM.
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

  if (activeTile != null) {
    const [activeTileID, activeTileName, activeTileBoxart] = activeTile;
    const activeTileElem = document.getElementById(activeTileID);
    activeTileElem.parentNode.removeChild(activeTileElem);
  }

  document.body.insertBefore(tile, document.body.firstChild);
  activeTile = [tileID, name, boxart];
}


// Register handlers to show Twitflix tiles above media boxes on mouse enter.
//
// The handler will not run if a Twitflix tile already exists for that media.
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


// Reposition and resize the currently displaying Twitflix tiles.
//
// This is needed since the media boxes change size on hover.
function repositionTile() {
  var tileID, name, boxart;
  const namesAndBobPlays = getNamesAndBobPlays();
  // Position the active tile on a box art / bob card.
  if (activeTile) {
    [tileID, name, boxart] = activeTile;
    if (name in namesAndBobPlays)
        positionAbove(tileID, namesAndBobPlays[name]);
    else
        positionAbove(tileID, boxart);
  }
  window.requestAnimationFrame(repositionTile);
}


// Position a tile above a HTMLElement.
function positionAbove(tileID, targetElem) {
  var tile = document.getElementById(tileID);
  if (tile == null) {
    console.log('Previous tile removed');
    return;
  }
  const height = targetElem.clientHeight;
  const width = targetElem.clientWidth;
  const targetPosition = targetElem.getBoundingClientRect();
  tile.style.height = `${height}px`;
  tile.style.width = `${width}px`;
  tile.style.left = `${targetPosition.left}px`;
  tile.style.top =
    `${targetPosition.top - document.body.getBoundingClientRect().top - height}px`;
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


// Return a set of {String: HtmlElement}, media names and bob card elements.
function getNamesAndBobPlays() {
  const namesAndBobs = {};
  const bobCards = document.getElementsByClassName('bob-card');
  const bobTitles = document.getElementsByClassName('bob-title');
  for (var i = 0; i < bobCards.length; i++) {
    // Find the title of this bob card.
    var title = null;
    for (var j = 0; j < bobTitles.length; j ++) {
      if (bobCards[i].contains(bobTitles[j])) {
        title = bobTitles[j].innerHTML;
        break;
      }
    }
    if (title != null)
        namesAndBobs[title] = bobCards[i];
    else
      console.log(`Could not find title for ${bobCards[i]}`);
  }
  return namesAndBobs;
}

console.log('Twitflix running...');
registerTilesOnPage();
document.onscroll = registerTilesOnPage;
window.requestAnimationFrame(repositionTile);
