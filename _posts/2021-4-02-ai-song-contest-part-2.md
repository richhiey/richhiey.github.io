---
layout: post
title:  "AI Song Contest 2021 Diaries - Part 2"
description: "Assembling musical data for learning musical tasks"
date:   2021-04-02 21:03:36 +0530
categories: Generative-Models Music AI-Song-Contest
---

Reflections on certain directions we are taking for the song contest this year.

Here, I write my thoughts about how we plan to us music data for learning models capable of creative tasks that often accompany the process of making music. 

The basic idea for our musical setup is that we first assemble for ourselves a set of useful AI tools. These AI tools must be able to create or transform musical information of different types. They must help us carry out tasks that are different from the functionality of normal music software. The tools must be  learnable i.e. their behavior must depend on the data fed into them. The tools must also have interfaces where we can interact with the learned model to test behavior. More complex models could have simpler interfaces. Simpler models could have more complex interfaces. Finally, we must be able to use the outputs from these interfaces within our DAW (Ableton Live).

So as is clear, our AI tools for music making are powered and shaped in terms of their functionality by the data that they are trained on. The AI models must learn knowledge representations from datasets, and must then be able to recreate new musical material using these learned representations. Therefore, each tool learns a different kind of representation, which can be used for simulating creative actions within a musical task.

It is important to make clear decisions about the types of musical data that is of interest, because there is so much data! For our purposes, since we are ultimately going to be working in Ableton Live, we wanted our AI tools to understand MIDI and audio data. They also help us achieve maximum amount of tasks and both these data formats are quite portable across software and hardware. It also helps us take a dual view at music, as being composed of a higher level structure of a MIDI track and a low level audio file which can be converted into sound. From this, it follows that our data will be in one of two formats - Audio or MIDI; MIDI for generative tasks of the creative process that require creativity on larger scales of time (composition) and audio for generative tasks over smaller scales of time (sound effects, singing, instrument sounds, etc).

Once the data formats have been decided, it is also important to ask what kinds of information do we want to capture in our datasets? What musical data is important to us and why? And where do we get this data from?

The characteristics of the data we collect will be centered around the tasks that we are training our AI models on. We have two types of AI models partially setup - Audio models and MIDI models. Audio models are a set of DL models which learn on audio data. MIDI models are a set of DL models that learn on MIDI data. 

Audio models consists of:
- **NSynth WaveNet autoencoder** (Pretrained)
	- NSynth can give us temporal embeddings of audio clips. These embeddings can then be used to resynthesize sound using a WaveNet decoder. The only drawback is that it is super slow. But it allows for interesting manipulations in the embedding space, and for a way to map these changes back to sound. Pretty cool! I see this as a tool to explore known spaces of sound.
- **SampleRNN**
	- Unconditional audio synthesis is the goal here. Feed in datasets of audio, and see what sampleRNN does with it! I see it as a way of exploring unknown spaces of sound.
- **DDSP**
	- This is something I just wanted to try out. The goal is to test DDSP on different kinds of vocal tasks. We will be testing out various variants of DDSP. First, we want to test unconditional generation of singing given f0 and amplitude features. Second, we want to learn a latent space of vocal techniques by using a VQ-VAE within the DDSP architecture. Slightly ambitious given the timeframe, but lets see how it goes!

MIDI models consists of:
- **MusicRNN models**
	- Collection of LSTM-based language models with different input representations which learn over MIDI datasets 
- **MusicVAE models**
	- Collection of Recurrent-VAE models which learn a latent space of single MIDI tracks or MIDI multitracks.

Finally, we want to know what types of musical data are important to us. Looking at the tasks above, we will be needing a few different types of datasets:
- Collections of subsets of sounds for unconditional generation (SampleRNN)
- Collections of clean singing voice datasets (DDSP)
- Collections of interesting sounds (NSynth Wavenet)
- Collections of subsets of MIDI tracks (MusicRNN and MusicVAE)

Each of the collections of data can have qualities slightly different from the others, hence allowing the AI model to learn something different. It is also important to have datasets that contain data which represent edge cases, to see where the model breaks and whether that is of any interest.

So thats a brief description about our decisions on what musical data is important in our musical process for the contest.