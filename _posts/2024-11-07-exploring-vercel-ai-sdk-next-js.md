---
layout: post
title:  "Exploring Vercel AI SDK and next.JS"
description: "Exploration of the capabilities of the Vercel AI SDK-Core and SDK-UI"
date:   2024-11-04 21:03:36 +0530
---

2024 has been the year of LLM's and other AI models with powerful generative capabilities across the domains of language, image, video and audio. While foundation models provide the essential building block for creating intelligent features in our applications, building AI-native user experiences on our devices requires a new way of thinking about how we integrate these AI models into our everyday software applications. [Vercel][vercel], the creators of [Next.JS][nextjs] are one such player in this market, easing up the deployment process for the next generation of applications creating native AI experiences on the web.

[vercel]: https://vercel.com/
[nextjs]: https://nextjs.org/

---

## Quick info about Next.JS

[Next.JS][nextjs] is a React based full-stack web framework used to create dynamic web based applications. React components and Typescript are used to create the front-end UI components for the user interfaces, whereas Next.JS provides an additional layer of optimizations and functionality over this.
The main features of Next.JS are noted down well in their supporting documentation.  [https://nextjs.org/docs#main-features](https://nextjs.org/docs#main-features). Some important concepts relevant to the Vercel AI SDK include:

#### [Routing](https://nextjs.org/docs/app/building-your-application/routing):
Next.JS supports a file-system based routing whereby a route is a single path of nested folders following the file heirarchy from the root-level until a final leaf-folder containing a page.tsx file. UI-files are used to create the UI shown for a particular route segment.

#### [Rendering](https://nextjs.org/docs/app/building-your-application/rendering):
Next.JS supports both [Client](https://nextjs.org/docs/app/building-your-application/rendering/client-components) and [Server](https://nextjs.org/docs/app/building-your-application/rendering/server-components) side rendered components. Server side components have a number of advantages, namely:
- Data fetching is easier since the components are rendered closer to the data sources. Sensitive data and logic can be kept more secure on the server side. Caching of server side rendered components, performance optimization by moving non-interactive code to the server to reduce client side Javascript, and improving of page load times by loading a page before it is requested can be done with Server components.
- Server components allow to split the rendering work across multiple chunks and stream them to the client as they are ready. This allows to the user to see the page without waiting for the whole page to be rendered.

## [Vercel AI SDK](https://sdk.vercel.ai/docs/introduction)

The Vercel AI SDK is a Typescript toolkit helping developers build AI applications using React and Next.JS amongst other frameworks. React Server Components and streaming turn out to be important concepts when dealing with the Vercel AI SDK.
The SDK consists of two separate parts, the SDK Core and the SDK UI.

#### [SDK Core](https://sdk.vercel.ai/docs/ai-sdk-core)
Vercel AI SDK Core solves this issue by offering a single way of interfacing with the LLMs from the supported providers through a Language Model Specification. The Language Model Specification is a set of specifications published by Vercel as an open-source package that can be used to create custom providers. The SDK exposes various functions that take a standardized approach to working with multiple LLM providers to setup prompts and settings.

- [generateText][generateText]: Generates text and calls tools for a given prompt 

Example using the OpenAI API:
```typescript
import { generateText } from "ai"
import { openai } from "@ai-sdk/openai"
const { text } = await generateText({
    model: openai("gpt-4-turbo"),
    prompt: "What is love?"
})
```

Similarly, [streamText][streamText]: Streams text from a given language model. We can also generate structured objects, as required by certain tasks like classification and synthetic data generation using the [generateObject][generateObject] and [streamObject][streamObject] functions. It can return or stream a typed, structured object for a given prompt and schema using a language model.

[generateText]: https://sdk.vercel.ai/docs/reference/ai-sdk-core/generate-text
[streamText]: https://sdk.vercel.ai/docs/reference/ai-sdk-core/stream-text
[generateObject]: https://sdk.vercel.ai/docs/reference/ai-sdk-core/generate-object
[streamObject]: https://sdk.vercel.ai/docs/reference/ai-sdk-core/stream-object

#### [SDK UI](https://sdk.vercel.ai/docs/ai-sdk-ui)

The AI SDK UI simplifies the process of building interactive applications like chat applications, handling complex tasks like state management, parsing and streaming data, data persistence and more.

It offers three main hooks, each serving a distinct purpose:

- [useChat][usechat]: Provides real-time chat streaming and manages input, message, loading and error state, making it easy to integrate into any UI design.

[usechat]: https://sdk.vercel.ai/docs/reference/ai-sdk-ui/use-chat

- [useCompletion][usecompletion]: Enables text completions, chat input state management and automatic UI updates as new completions are streamed from an AI provider.

[usecompletion]: https://sdk.vercel.ai/docs/reference/ai-sdk-ui/use-completion

- [useAssistant][useAssistant]: Facilitates interaction with OpenAI-compatible assistant APIs, 
managing UI state and updating it automatically as responses are streamed.

[useAssistant]: https://sdk.vercel.ai/docs/reference/ai-sdk-ui/use-assistant

## [AI SDK RSC](https://sdk.vercel.ai/docs/ai-sdk-rsc)
The AI SDK RSC extends the SDK’s power beyond plain text, providing LLMs with rich, component-based interfaces using the React Server components approach employed in Next.js.

It enables streaming user interfaces directly from the server during model generation, eliminating the need to conditionally render them on the client based on the data returned by the language model.

---

Hence, Next.JS coupled with the Vercel AI SDK and the various LLM model providers shows a path towards creating generative AI/UI application with powerful integrations between various components, while retaining customizability over each indvidual part of the stack as required!