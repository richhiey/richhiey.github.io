---
layout: post
title:  "Sequential Chains with Memory using LangChain"
description: "Learning about sequential chains with LangChain, integrating memory and it's internals"
date:   2024-11-05 21:03:36 +0530
tag: Langchain
---

The latest LLM's provide much better performance than previous approaches at the language modelling task when approached as a one-shot task. Many a times, we want to chain together sequences of such LLM's, prompting each other to create more complicated pipelines compared to simple one-shot prompts. We might also want to process the LLM outputs in order to return structured objects like JSON or XML for tasks like classification or text summarization.

[LangChain][langchain] is one such framework for developing pipelines using LLM's. It has libraries for [Python][langchain-py] and [Typescript][langchain-js]. It can be used in all phases of setting up an AI application. In development, LangChain provides open-source building blocks and integrations for working with most of the major open-source and closed-source model providers such as OpenAI, Anthropic, Mistral, HugggingFace, etc. [LangSmith][langsmith], [LangServe][langserve] and [LangGraph][langgraph] can be used by applications in production to monitor and evaluate deployed chains, providing a ready to use CI/CD pipeline to optimize deployments.

[langchain]: https://python.langchain.com/docs/introduction/
[langchain-py]: https://github.com/langchain-ai/langchain
[langchain-js]: https://github.com/langchain-ai/langchainjs

[langsmith]: https://www.langchain.com/langsmith
[langserve]: https://python.langchain.com/docs/langserve/
[langgraph]: https://www.langchain.com/langgraph


The LangChain framework consists of the following components, namely:
- [langchain-core][langchain-core]: Base abstractions and LangChain Expression Language.
- Integration packages (e.g. [langchain-openai][langchain-openai], [langchain-huggingface][langchain-hf], etc.): These integrations have been split into lightweight packages that are co-maintained by the LangChain team and the integration developers.
- [langchain][langchain]: Chains, agents, and retrieval strategies that make up an application's cognitive architecture.
- [langchain-community][langchain-community]: Third-party integrations that are community maintained.

[langchain-hf]: https://python.langchain.com/docs/integrations/providers/huggingface/
[langchain-openai]: https://python.langchain.com/docs/integrations/providers/openai/
[langchain-core]: https://pypi.org/project/langchain-core/
[langchain]: https://pypi.org/project/langchain/
[langchain-community]: https://pypi.org/project/langchain-community/


### LLMChain:

LLMChain represents a simple chain consisting of an input parser, an LLM model and an output parser. This was previously created with the LLMChain class that is now deprecated, and is now done using the LangChain Expression Language.

```python
from langchain.prompts import PromptTemplate
from langchain_google_genai.llms import GoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser

template_str = """
Act like a Captain Obvious and list 5 funny things to not do at {prompt}?
"""
output_parser = StrOutputParser()
prompt = PromptTemplate(input_variables=["prompt"], template=template_str)
question = "Mumbai"
gemini_llm = GoogleGenerativeAI(model="gemini-1.5-flash")
llm_chain = prompt | gemini_llm | output_parser
output_str = llm_chain.invoke({"prompt": question})
print(output_str)

"""
1. **Don't try to hail a taxi with your bare hands.**  They're called "taxis" for a reason! You need to wave your hand like you're trying to signal a passing ship. 
2. **Don't wear your best silk scarf while riding a local train.**  It's a whirlwind of humanity in there, your scarf will end up as a souvenir for someone else. 
3. **Don't order a "chai" and then ask for it "with milk."**  It's basically a law of the universe that chai is made with milk.  
4. **Don't try to bargain with a street vendor for a 10 rupee item.**  Just pay the price and enjoy your vada pav.  
5. **Don't forget to bring your own umbrella.**  It's Mumbai, it rains like it's trying to wash away the entire city. 

Remember, folks, Mumbai is a city of contrasts, but one thing's for sure: you'll have a great time if you just relax and go with the flow.  Now, go forth and explore! 
"""
```

The above LLM chain can also be created with a LangChain ChatModel. The difference between a ChatModel and an LLM model in LangChain boils down to the difference in parameters that are passed to the model. The LLM is closer to the model whereby the input passed in is a string and the output is a string. Chat models are more readily setup for creating conversational interfaces and hence take input as a list of messages of the type SystemMessage, AIMessage, HumanMessage. PromptTemplate is used for formatting prompts for LLM's whereas ChatPromptTemplate is used to for prompt formatting with ChatModels. Below is an example code snippet to run a simple LLM Chain with Chat models.

```python
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a travel assistant bot. Given the name of a place, you must provide the best points to visit around that area."),
    ("human", "The name of the place is - {prompt_str}")
])
gemini = ChatGoogleGenerativeAI(model="gemini-1.5-flash", max_tokens=None, timeout=None, max_retries=2)
llm_chain = prompt | gemini | output_parser
output_str = llm_chain.invoke({"prompt_str": question})
print(output_str)
```
This produces the same result as the code cell above! Just a different way of achieving the same output.

### LLMChain with Memory
Many a times, we want our Chat models to remember previous conversations and use them as context when creating responses to latest queries fired by the user. For e.g. if a user tells the chat-bot his name, it is important that this name is remembered and referenced throughout the conversation to personalize the chat experience. Similarly, we want to capture other aspects of user preferences expressed as part of the conversation while tailoring responses for user queries. This is where the concept of Memory comes into play in LangChain.

We can add memory capabilities to our LLMChain by wrapping it around a class named RunnableWithMessageHistory. This provides various options for storing previous messages for the chat model to access it easily when crafting responses. Below is a code snippet showing how this is put into action!

```python
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.runnables import ConfigurableFieldSpec
from langchain_community.chat_message_histories import ChatMessageHistory, \
                                                        RedisChatMessageHistory
```
```python
store = {}
question = "suggest good places to eat in Mumbai. Also, my name is Richhiey, let's see if you can remember this ;)"
```
```python
def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

def get_user_session_history(user_id: str, conversation_id: str) -> BaseChatMessageHistory:
    if (user_id, conversation_id) not in store:
        store[(user_id, conversation_id)] = ChatMessageHistory()
    return store[(user_id, conversation_id)]
```
```python
gemini = ChatGoogleGenerativeAI(model="gemini-1.5-flash")
prompt_template = ChatPromptTemplate([
    ("system", "You are a friendly travel assistant known for suggesting the best places to visit in a given location. You not only provide names of places but also answer queries regarding details about the place"),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}")
])
output_parser = StrOutputParser()
runnable = prompt_template | gemini | output_parser
with_message_history = RunnableWithMessageHistory(
    runnable, get_user_session_history, input_messages_key="input", history_messages_key="history",
    history_factory_config=[
        ConfigurableFieldSpec(
            id="user_id",
            annotation=str,
            name="User ID",
            description="Unique identifier for the user.",
            default="",
            is_shared=True,
        ),
        ConfigurableFieldSpec(
            id="conversation_id",
            annotation=str,
            name="Conversation ID",
            description="Unique identifier for the conversation.",
            default="",
            is_shared=True,
        ),
    ],
)
```

Now, we have wrapped our runnable within the RunnableWithMessageHistory object and we are utilizing an instance of the ChatMessageHistory class to store message histories related to this chat. An easy test of whether this works will be to tell the model our name and then check whether it remembers it or not. If it can remember the name, it means it is able to access the chat history! 

```python
question = "suggest good places to eat in Mumbai. Also, my name is Richhiey, let's see if you can remember this ;)"
print(with_message_history.invoke({"input": question}, config={"configurable": {"user_id": "1", "conversation_id": "1"}}))
# ---------------------
"""
Hey Richhiey!  I'll try my best to remember your name. 😊  

Now, let's talk food!  Mumbai has so many amazing places to eat.  To give you the best recommendations, tell me a little bit more about what you're looking for:

* **What kind of food are you craving?**  (Indian, street food, fine dining, international, etc.)
* **What's your budget?** (Budget-friendly, mid-range, high-end)
* **What area of Mumbai are you in?** (South Mumbai, Bandra, Juhu, etc.) 

Once I know what you're looking for, I can give you some personalized recommendations! 
"""
```

```python
print(with_message_history.invoke({"input": "Btw, what's my name?"}, config={"configurable": {"user_id": "1", "conversation_id": "1"}}))
# ----------------------------
"""
Hey Richhiey! 😊  I'm doing my best to remember your name.  

Now, let's talk food!  Mumbai has so many amazing places to eat.  To give you the best recommendations, tell me a little bit more about ...
"""
```

And just like this, we were able to create a Runnable that is able to store message histories! The current history is stored within a variable named store. However, in a real-world scenario, we might want to save these messages into a more persistent storage like a local file or an online Redis store. The [memory integrations][mem-integrations] page shows various options for how persistence of messages can be configured beyond a simple in-memory store.   

[mem-integrations]: https://integrations.langchain.com/memory

### SimpleSequentialChain

This is the simplest type of sequential chain which takes only a single input, and the output of each step is the input of the next step. Here is an example of how this works in LangChain. The chain passes inputs through the variable "input".

```python
from langchain.chains import SimpleSequentialChain
```
```python
singer_prompt_template = """
You are singer and song writer. Your job is to come up with the best possible lyrics with an interesting rhyme scheme given some input such as a topic, an event or a story. Here is the input for which you create a song: {input}
"""
singer_prompt_template: PromptTemplate = PromptTemplate(input_variables=["input"], template=singer_prompt_template)
singer_runnable = LLMChain(llm=gemini_llm, prompt=singer_prompt_template)
genre_prompt_template = """
You are tasked with identifying the genre of a song given its lyrics. You must also specify keywords describing the main ideas and concepts being used in the given lyrics. The required output will contain the genre of the song and the required keywords.
The lyrics of the song are: {input}.
"""
verified_prompt_template: PromptTemplate = PromptTemplate(input_variables=["input"], template=genre_prompt_template)
verify_runnable = LLMChain(prompt=verified_prompt_template, llm=gemini_llm, output_parser=output_parser)
```
```python
ss_chain = SimpleSequentialChain(chains=[singer_runnable, verify_runnable])
review: str = ss_chain.invoke("Climate change")
print(review)
# ------------------------------------------
"""
## Genre: **Environmental Anthem/Protest Song**

## Keywords:

* **Climate Change:**  The central theme of the song, focusing on its effects and consequences.
* **Environmental Destruction:**  Lyrics depict the devastating impacts of climate change on the planet (melting ice caps, rising oceans, forest destruction).
* **Greed:**  Blames human greed and disregard for warnings as the root cause of the crisis.
* **Urgency:**  Emphasizes the immediacy of the situation and the need for action.
* **Hope:**  Despite the bleakness, the song ends on a note of hope, urging listeners to act and change their ways.
* **Nature's Fury:**  Highlights the powerful and destructive forces unleashed by climate change.
* **Survival:**  The song emphasizes the importance of collective action for the survival of humanity and the planet. 
"""
```

### SequentialChain
The limitations of the SimpleSequentialChain are overcome with the SequentialChain whereby we can pass multiple inputs to the prompts at different stages!

```python
from datetime import datetime
from langchain.chains import SequentialChain
from langchain.memory import SimpleMemory
```
```python
singer_prompt_template = """
You are singer and song writer. Your job is to come up with the best possible lyrics with an interesting rhyme scheme given some input such as a topic, an event or a story. Here is the input for which you create a song: {input}
"""
singer_prompt: PromptTemplate = PromptTemplate(input_variables=["input"], template=singer_prompt_template)
genre_prompt_template = """
You are tasked with identifying the genre of a song given its lyrics. You must also specify keywords describing the main ideas and concepts being used in the given lyrics. The required output will contain the genre of the song and the required keywords.
The lyrics of the song are: {ai_lyrics}.
"""
genre_prompt: PromptTemplate = PromptTemplate(input_variables=["ai_lyrics"], template=genre_prompt_template)
final_prompt_template = """
You are tasked with creating the final output for verification of generated song lyrics.
The output string must contain the following details:
1. Genre: Musical genre the song belongs to
2. Keywords: specific words that represent the themes running through the song
3. Date of human verification: {time_created_and_verified}
4. Full lyrics of the generated song!

Here are the generated lyrics!
{AI_verified}
"""
final_prompt: PromptTemplate = PromptTemplate(
    input_variables=["AI_verified", "time_created_and_verified", "verified_by_human"], template=final_prompt_template
)
```
```python
# creating the rapper chain
singer_chain: LLMChain = LLMChain(llm=llm, output_key="ai_lyrics", prompt=singer_prompt)
# creating the verifier chain
genre_chain: LLMChain = LLMChain(llm=llm, output_key="AI_verified", prompt=genre_prompt)
# creating the verifier chain
final_chain: LLMChain = LLMChain(llm=llm, output_key="final_output", prompt=final_prompt)
# creating the simple sequential chain
ss_chain: SequentialChain = SequentialChain(
    memory=SimpleMemory(
        memories={"time_created_and_verified": str(datetime.utcnow()), "verified_by_human": "False"}),
    chains=[singer_chain, genre_chain, final_chain],
    # multiple variables
    input_variables=["input"],
    output_variables=["final_output"],
    verbose=True
)
# running chain
review = ss_chain.run(input="Social media")
print(review)
# ----------------------------------------------
"""
> Entering new SequentialChain chain...

> Finished chain.
## Genre: Pop/Indie Pop

## Keywords: 
* Social Media
* Addiction
* Comparison
* Authenticity
* Disconnection
* Digital World
* Self-Reflection

## Date of Human Verification: 2024-11-09 19:08:26.735703

## Lyrics:

**(Verse 1)**
Scrolling through the feeds, another perfect day
Smiling faces, filtered lives, it's all a facade they say
Everyone's a star, a highlight reel, a perfect life they portray
But behind the screens, the truth is hidden, a different story to convey

**(Pre-Chorus)**
The dopamine rush, the endless scroll, a constant chase for more
Lost in the digital world, forgetting what we're living for
Comparing ourselves, chasing dreams, that we've made up in our heads
Ignoring the beauty of reality, the moments we've left unsaid .....
"""
```

Code used in this post can be found at - [langchain/sequential.ipynb](https://github.com/richhiey/ai-model-playground/blob/develop/models/langchain/sequential.ipynb)

The above examples using the basic LLMChain, SimpleSequentialChain and the SequentialChain with memory gives us an idea for how to build basic pipelines where models are chained together with multiple inputs. It also shows how the chains integrate with memory to craft outputs as if they remember details of previous conversations in chat models. Memory can also be used outside of the chat messages, to retrieve values like the dates from external stores based on identifiers. There is much more to chains in LangChain and I'm excited to explore this topic further!
