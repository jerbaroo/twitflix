//@ sourceURL=twitflix.js

// Whether to print out new media names when discovered.
const PRINT_MEDIA_NAMES = false;

// Whether to show the histogram.
const SHOW_HISTOGRAM = false;

// The current active tile as: (ID, media name, boxart element).
var activeTile = null;

// All media names we know of so far.
const mediaNames = new Set();

const canvasContainerID = (tileID) =>
  `twitflix-canvas-container-${tileID}`;


// An identifier to uniquely identify a Twitflix tile.
function newTileID() {
  _tileID++;
  return `twitflix-${_tileID - 1}`;
}
var _tileID = 1;


// Return the film data from the large data object.
function filmData(name) {
  return _filmData[name];
}
const _filmData = null;


// Attach a graph of given data to a canvas element.
function attachGraph(canvasContext, sentiments) {
  new Chart(canvasContext, {
    type: 'line',
    data: {
      datasets: [{
        data: sentiments.map(x => x[0]),
        label: "Sentiment",
        borderColor: "#3e95cd",
        fill: false
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false
    }
  });
}


function mean(numbers) {
  var total = 0, i;
  for (i = 0; i < numbers.length; i += 1) {
    total += numbers[i];
  }
  return total / numbers.length;
}


// Right side of twitflix box, a histogram.
function showHistogram(tileID, height, width, right, data) {
  var canvas = document.createElement('canvas');
  canvas.id = canvasContainerID(tileID);
  right.style.position = 'relative';
  right.style.height = `${height}px`;
  right.style.width = `${width * 0.66}px`;
  right.appendChild(canvas);

  attachGraph(canvas.getContext('2d'), data["sentiments"]);
}

// Convert a value from one range to another range.
// e.g. convertRange(5, [0, 10], [0, 100]) = 50.
function convertRange( value, r1, r2 ) {
  return ( value - r1[ 0 ] ) * ( r2[ 1 ] - r2[ 0 ] ) / ( r1[ 1 ] - r1[ 0 ] ) + r2[ 0 ];
}

// Inner contents of some tile, for some media title.
function newInnerTile(tileID, name, height, width) {
  var main = document.createElement('div');
  main.className = 'twitflix-tile-main';
  var left = document.createElement('div');
  left.className = 'twitflix-tile-scores';
  var right = document.createElement('div');
  right.className = 'twitflix-tile-graph';
  main.appendChild(left);
  main.appendChild(right);

  const data = filmData(name);
  const criticScore = data["critic_score"];
  const userDescription = data["agreement"];
  const userCompound = data["scores"]["mean_scores"]["compound"];
  const userScore = convertRange(userCompound, [-1, 1], [0, 10]);

  // Left side, critic and user score.
  var criticScoreEl = document.createElement('div');
  criticScore.className = 'twitlix-tile-score';
  criticScoreEl.innerHTML = `${userScore}<br>Critic`;
  var userScoreEl = document.createElement('div');
  userScore.className = 'twitlix-tile-score';
  userScoreEl.innerHTML = `${criticScore}<br>Twitter`;
  left.appendChild(criticScoreEl);
  left.appendChild(userScoreEl);

  if (SHOW_HISTOGRAM)
    showHistogram(tileID, height, width, right, data);

  return main;
}


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
  tile.appendChild(newInnerTile(tileID, name, height, width));
  return tile;
}


// A new Twitflix tile is added to the DOM, above the given boxart element.
//
// Removes the current active tile if it exists. Also registers a function to
// resize the tile if the media box resizes or the page resizes.
function showNewTile(boxart, name) {
  if (activeTile == null || activeTile[1] != name) {
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

  const right = document.getElementById(canvasContainerID(tileID));
  right.style.height = `${height}px`;
  right.style.width = `${width * 0.66}px`;
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
window.setInterval(registerTilesOnPage, 100);
window.requestAnimationFrame(repositionTile);
