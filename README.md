# hololive_collabs
[Link to the final product.](https://thennal10.github.io/hololive-collabs/)

So I was bored out of my mind and decided to do a little data visualization. In particular, I wanted to see a network graph of collabs, and I liked all my plots interactive and jiggly. Two issues: there is no one as far as I can find whose hobby is to just collect collab information between vtubers, and jiggly plots means (to an extent) I'd have to work outside python. 

There is no real solution to issue 1: only a bad approximation. See, most vtubers, when doing a planned collab, link each other in the description. Unlike titles, hashtags, and whatever else, these links are far easier to parse and a fair bit more reliable

Two problems with this approach:

A) A lot of collabs are streamed on both channels of the given vtubers. Due to the way this works, it counts this as 2 collabs. Since I just generally want an overarching idea of who collabs with who more than completely accurate data, this was more or less fine with me, but be warned that this is heavily biased towards vtubers who do more multistream collabs.

B) Some vtubers link their genmates on the descriptions of *all* their videos. With respect to Hololive, all other livers in all other branches (ID, EN, Holostars) do this. This, in particular, is why I didn't extend the data collection to Nijisanji or other independant vtubers: I didn't want to spend hours looking through every single liver's description to confirm that they don't spam other vtuber links on every video.

As for issue 2, considering this vue project also has an ipynb file, you can probably guess how that shook out. Python *did* have a library that acts as a wrapper for visjs, and it even outputs as an html file and displays inside ipynb. Only one, personally breaking issue: a minimum collab filter - something that just yeets all the collab links that are less than a certain amount - is the only way to to make the network look semi-comprehensible, and not letting the viewer have control of that just seemed wrong. Didn't find a way to do that without directly using visjs. Hence, this vue project!

## Data Collection
All data collection is done in `collabs.ipynb`, with the resulting json object in `src/assets/collabs.json`, which vue accesses. Pretty straightforward. I used the [vtuber wiki](https://virtualyoutuber.fandom.com/wiki/Virtual_YouTuber_Wiki) to get a list of everyone in the Hololive JP branch and their channel links, and then used the [Youtube Data API](https://developers.google.com/youtube/v3/getting-started) to get video description data. You can look through the ipynb file to see the specifics, and change it up a bit if you want to, for example, do another set of vtubers.

## The Vue Project
The vue part itself isn't exactly special. It just uses visjs to create the network, and then adds a simple box with a slider to change the minimum collab filter.

### Project setup
The data collection will require everything needed to run an ipynb file, and a couple misc python libraries. Just use pip and download based on imports.

As for the vue part, that's pretty easy:

```
npm install
```

### Compiles and hot-reloads for development
```
npm run serve
```

### Compiles and minifies for production
```
npm run build
```

### Lints and fixes files
```
npm run lint
```

### Customize configuration
See [Configuration Reference](https://cli.vuejs.org/config/).
