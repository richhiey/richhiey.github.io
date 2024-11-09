---
layout: post
title:  "Experiments on writing music with AI"
description: Looking back at my journey participating in the AI Song Contest
date:   2020-05-09 21:03:36 +0530
---

*AI Song Contest Entry - [Contest Page][contest], [Traveller in Time][song-link]*

- Team name - OVGNeUrovision

- *[Music Maker App][demo-app]*

- *Github [repository][github-repo]*

- *Live Stream [Link][live-stream-link]*

- *Official [Results][official-results]*

- *[Blog][magenta-post] about learnings from AI Song Contest by Magenta Team*

- *AI Song Contest [wikipedia][contest-wiki]*

Both Music and AI have been a part of my life for a long time.

My mother encouraged me to learn music as a kid and coming from a Christian family, I loved singing with my church choir. I even learnt to play the guitar and the piano while in college, just because it was cool. Even after moving out of home, I found a few Indian friends who love playing the tunes we used to listen to back at home. So we enjoy performing for our friends here. But all in all, music always made me feel a sense of social harmony with the people around me. It is always a good feeling.

Artificial Intelligence on the other hand is a field I have been pursuing since a few years now. It started out by implementing a simple K-Means algorithm for Xapian, until now, where I am starting to make sense of the immense progress that really smart people in computer science are making around the world. My most recent fascinations are the fields of Deep Learning and Reinforcement Learning, specifically with scenarios where we teach AI models how to generate data. In my context, I'm interested in generative models for musical applications. :D

While I had been planning to experiment with generative models for music, I had never taken time out to answer all the questions that needed to be answered for the experiment to be developed. So when the idea of an AI Song Contest landed on my consciousness, I was pumped. We had three months to develop an AI-driven-system for making a Eurovision like song. Seemed like the perfect way to test a system for generative music! But when I started brainstorming for ideas, I found myself asking some really fundamental questions. 

- What is music?
- What does music mean to me?
- Why AI in music?
- What can AI do in music?
- How do I interact with this AI?
- Can I play with a band of AI musicians?

The answers to these questions shaped my perspective on how I think about AI in music.

As I started to think about the first question, I started to wonder why music exists at all. But as I looked back at my own experiences, I saw that music is nourishment for the soul. Music has the power of metaphor, just like language, and can thus be used to tell stories. And stories make us feel emotions, all kinds of them. Hence, it is to fill in this emotional void within ourselves that we've been musical creatures, from the stone age to present times. We can see that music of each generation represents what human civilization sounded like in that period. As we had more tools, the music we cherished became increasingly complex. Hence most importantly, I realized that music is basically what we sound like as humans! 

Consequently, a thought really resonated with me. I thought, 'the music I consume or create is what I sound like'. This was a really motivating thought. I started looking beyond my physical limitations as a musician. It seemed to me that there must always be a way to explore what I sound like. And I started wondering whether AI could help me find what I'm looking for.

The Google Magenta Project was a very effective demonstration of why AI in music. Simply because of the creative possibilities if offers. Music is composed of multiple layers of concepts, such as song structures, chord progressions, rhythm, tempo, instrument sounds etc. The Magenta Project proves that it is possible to build creative tools for musical expression in completely novel ways by learning the patterns underlying such concepts. I find that particularly interesting. We can build machines to learn from our musical knowledge?! What would they learn? What would their music sound like? If I train the machines with music that I like, will they sound like me then? Such questions really started stretching my ideas about what it meant to be creative.

After my first few tries of generating sequences of notes with the Magenta models, I felt like I lost track of what I was doing. Because nothing sounded great. It was all okay. And thats when it struck me, that music cannot happen without some kind of interaction. There always has to be a back-and-forth of ideas for a musical moment to come. So I investigated whether I could interact with the AI models in better ways. And I realized that there is infinite room for creativity with the kinds of tools that we can be build. So I followed a simple process, where I gave the model a sequence of notes, and it would give me something back. Then I would listen, and give something back. Or else, I'd give the model a start sequence and an end sequence, and I'd tell the model to figure out melodies in between those two sequences. I am pleasantly surprised by how a back-and-forth between me and my computer helped me create a song.

The way I see it, the AI helped me fill in the gaps in my musical knowledge, but still let me use my musical ear for allowing my composition to sound like me. I truly believe in the power of AI to democratize the power of music making to people who might not be formally trained, but might be passionate enough to explore. A simple webapp can help anyone become a musician using their keyboard and a bunch of deep learning models. And the challenge of creativity lies in what new things we can discover in such a paradigm. Experienced musicians will be able to use such tools in much more advanced ways, thus expanding our collective consciousness about the possibilities of music making.

I interacted with multiple Magenta models within my browser playing different instruments, so in some sense, I did feel like I was playing with my band of AI Musicians. However, I still need to equip these 'AI Musicians' with more functionality so that it is easier to interact with them going ahead. But I happily admit that I could not have written a song without AI and that it expanded my ideas about what is possible.

Going ahead, I want to move from the design aspect of this system into more technical aspects such as building custom pipelines for training models and interacting with them on the interface, experimenting with the latest advances such as DDSP and other powerful models for symbolic and raw audio music and moving these models to the web.

Creating a song has been a deeply enriching experience for me, since it taught me the creative process. Starting off with an idea and moulding it into musical expression by being patient and being deeply involved in the act. I will cherish this as a time of learning, and I'm looking forward to all the cool things that I will be able to do with my 'Music Maker' in the future! :D


[github-repo]: https://github.com/richhiey1996/music-maker
[demo-app]:   https://ai-music-maker.herokuapp.com
[song-link]: https://www.youtube.com/watch?v=BNRd4eo-ePk
[contest]: https://www.vprobroadcast.com/titles/ai-songcontest/teams/germany-2.html
[live-stream-link]: https://www.youtube.com/watch?v=-yIu5VLZj5g
[official-results]: https://github.com/AI-Song-Contest/ai-song-contest-data
[magenta-post]: https://magenta.tensorflow.org/aisongcontest
[contest-wiki]: https://en.wikipedia.org/wiki/AI_Song_Contest