A quick refactor of an older project, because I wanted to try out [Streamlit](). Verdict: a largely immature tool, but occasionally useful if you need to be *fast* fast.

## Hololive Collabs
If you drill it down, it's actually just a network graph counting many times a hololive vtuber has linked another hololive vtuber in
any of their video descriptions. I just make the assumption that this indicates a collab. Liver data is taken from the [Holofans wiki](https://hololive.wiki/wiki/Main_Page).

Caveats:
1. If two livers collab with eachother, and they both make video linking the other liver in their respective livestreams, the collab
is double-counted, so to speak.
2. Instead of linking the channel, some livers directly link the other livestream for a collab. Rare to also not just throw a channel
link in there too, but something to keep in mind.
3. Only the JP branch. Other branches have the tendency to link literally all their genmates/branchmates on every single video description.


All three of those could be countered by some cross-checking (video owner checks and timing checks) but that's for someone else to code up. I just
wanted a jiggly graph that approximates collabs.