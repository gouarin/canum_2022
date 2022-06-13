import 'reveal.js/dist/reveal.css'
// see available themes in the
// node_modules/reveal.js/dist/theme
//  beige, black, blood, league, moon, night, serif, simple, ...
// import 'reveal.js/dist/theme/black.css'
import 'highlight.js/styles/github.css'
// import 'reveal.js/plugin/highlight/monokai.css'
import 'reveal.js-menu/menu.css'

import Reveal from 'reveal.js'
import Markdown from 'reveal.js/plugin/markdown/markdown.esm.js'
import RevealHighlight from 'reveal.js/plugin/highlight/highlight.js'
import RevealMath from 'reveal.js/plugin/math/math.js'
// import RevealMenu from 'reveal.js-menu/menu.js'
import RevealMenu from './plugin.js'

function get_theme_ext(href)
{
  if (href == "/theme/dark.css")
  {
    return "dark";
  }
  else {
    return "light";
  }
}

function update_img() {
  var theme = document.getElementById("theme");
  var href = theme.getAttribute("href");
  var theme_ext = get_theme_ext(href);
  var el = document.querySelectorAll("#adapt");
  for (var i = 0; i < el.length; i++) {
    var data = el[i].getAttribute("src").split(".");
    console.log(data);
    var ext = "_" + theme_ext + "." + data[1];
    var filename = data[0].split("_");
    if (filename.length == 1) {
      el[i].setAttribute("src", filename[0] + ext);
    }
    else {
      el[i].setAttribute("src", filename.slice(0,-1).join('_') + ext);
    }

  }
}

var observer = new MutationObserver(function(mutation){
  console.log("coucou")
  update_img();
});

var theme = document.querySelector("#theme");

observer.observe(theme, {
  attributes: true,
  attributeFilter: ["href"],
});


const deck = new Reveal({
  plugins: [Markdown, RevealHighlight, RevealMath.KaTeX, RevealMenu]
})

deck.initialize({
  // width: 960,
  // height: 700,
  center: true,
  hash: true,
  menu: {
    themes: true,
    // themesPath: 'public/theme',
    themes: [
        // {name: 'dark', theme: 'public/styles.css'},
        // {name: 'light', theme: 'public/styles_light.css'},
        {name: 'black', theme: '/theme/black.css'},
        {name: 'dark', theme: '/theme/dark.css'},
        {name: 'light', theme: '/theme/light.css'}
    ],
    path: 'node_modules/reveal.js-menu/',
  },
  // markdown: {
  //   smartypants: true
  // }
})


// function select_img()
// {

//     theme.setAttribute("href", "/theme/light.css")
// }

// select_img()