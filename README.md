Minimal Pairs Scraping Project
==============================

I am going to use forvo's api ($12 for six months, a little overpriced to use
once) in order to generate an anki deck of minimal pairs to be able to identify
French words.

The initial idea came from [fluent forever's minimal pairs anki
decks][0] (which I have not purchased). After I read [this incredibly
well-written][1] review of the product I decided it wasn't the right choice for
me.

Since I didn't want to spend the $12 on his deck, but I did want to explore the
concept, I found [this pretty good anki deck][2] for French pronunciation. It
has 349 notes, and is well put together, but I feel it's not enough,
specifically given this quote from that review I linked:

> Perhaps a better approach would have been to have only recorded people
> speaking their own language but to have a large enough pool of voices that it
> would be hard to recognise a particular voice. That would also help with the
> dialect problem because you could either have words pronounced in each major
> dialect or at least consistently hear the same dialect. I understand that
> having the extra speakers would have cost more but then much of the money
> raised was used for producing word lists, cartoons and free copies of the
> book, none of which contribute to the core purpose - improving pronunciation.

This is a brilliant idea, I thought, and it's a shame that Gabriel Wyner wasted
everyone's money on pretty pictures and word lists. But then I had a thought.

My Google Fu was feeling quite tingly, so I googled French minimal pairs and
found [this excellent linguistics Stack Exchange answer][3] which lead me to
[this blog post][4] where a brilliant man describes developing [this incredible
list][5] of every minimal pair in the French language. ([He also did it for
American English, Dutch, and Spanish if anyone is interested.][5]).

The problem with this, of course, is that (a) his list does not have audio like
I want it, and it's not even a machine readable format (it's html). Tant pis.
Instead of emailing him for it (which would be obnoxious), I figured I'd just
break out BeautifulSoup4 and parse it myself into 4 fields: 

1. The 1st word
2. The 1st word's IPA
3. The 2nd word
4. The 2nd word's IPA

This went off without a hitch.

The next step is to get all of the audio files. They are conveniently labelled
with esoteric id names, which will help in identifying them when I convert them
into anki, but for $12 (at six months) I have a 500 requests per day rate limit.
What's worse is that each audio file's time to be downloaded is limited to two
hours (they're one time links, I guess). And, finally, each audio file download
also counts toward my requests. There are 3792 pairs, which is 7584 words, and
for any word there may be 4-5 pronunciations. If we average at 3 that's 22,752
downloads, which does not include the requests to get the files (which will
require 7,584 requests), which ends up being 30,336 requests. That will take me
2 months to download.

I'm going to restart, and create a list of only the minimal pairs I care about
(since I know the difference between n and m).

It's starting to feel like I would have been better off just scraping like a
jerk than buying the api.

The Reckoning
-------------

Alright, so I recognized first that I don't really need to worry about
consonants. I saved like 2 pairs from that. The second thing I realized is that
there are an absurd amount of duplicates in this list, not just of pairs, but of
words.

First thing I did was go through the actual web page and my csv list and deleted
most of the consonant pairings. That brought me down to 1487 from 3792. Since
French vowels are the most difficult to hear, I'll just stick with those. And
since I don't feel like figuring out which vowels are problematic (obviously I
can differentiate opposition from imposition even in French) I'll just keep them
all. Because...

The second thing I did was deduplicate the list of pairs. That brought me from
1487 down to 745. This is starting to sound more doable.

In those 745 pairs are (obviously) `745 x 2 =` 1,490 words. But there an absurd
amount of duplicates. Bringing that down to unique we have a mere 497 unique
words.

497 words times an average of 3 files per word comes to 1,491 files to download.
That's almost 2,000 requests which I can do in (probably) a little over 4 days.

Now I just have to write a program that will do the following:

1. Take in the list of unique words
2. query forvo for the word
3. Limit the list to the pronunciations in French (the api doesn't seem to do
   that).
4. Download each of the French pronunciations of the given word.
5. Add the filenames to a json file to identify each word (and keep track of
   what has already been downloaded).
5. Repeat steps 3, 4, and 5 until I hit the 500 request rate limit.

Then, after that, I will use combinatronics to match every wordpair with every
file so that I have the maximum number of anki cards with the maximum number of
sounds for ultimate learning goodness.

Now to begin this hard part.

[0]: https://fluent-forever.com/product/fluent-forever-pronunciation-trainer/
[1]: https://www.reddit.com/r/German/comments/2przo1/a_review_of_fluent_forever_foreign_language/
[2]: https://ankiweb.net/shared/info/932662308
[3]: https://linguistics.stackexchange.com/a/11634
[4]: http://verbally.flimzy.com/list-of-french-minimal-pairs/
[5]: https://minimalpairs.net/en
