===============================================================================
### HELLO AND WELCOME TO MY LITTLE DOCUMENT ABOUT AI USAGE IN THIS PROJECT ###
===============================================================================

#### 01 General Opinion
AI exists. While we certainly can completely avoid using it, there really isnt a point.
Generative AI doesnt neccessarily makes you a worse coder. It's a tool and if you use it properly,
it can benefit you / us greatly and speed things up.
AI can help. It can't magically build your app.
Use it to assist and learn, dont use it to vibe code

===============================================================================
#### 02 IMPORTANT THINGS TO REMEMBER
IF you work with AI and you copy past shit into it, especially code
--> Anonimyze what you feed the model
In my work, i never use Bellis EV. Because i dont want that connection to exist.
I shortened it to B_EV
When working with keys and other senstive data and what not, you can simply put in X's

That way the model knows something is there. But it doesnt have the link. Or the key. Or anything of interest beyond the code, really.
committing private secrets like .env files to GitHub is bad. If you feed it to AI, i will find you in your sleep.
DONT.

==================================================================================
#### Tools I use (And maybe you can too)

#### CodeRabbit 
CodeRabbit is a neat little tool that helps you with code reviews. Thats what happens if you push a branch and then do
a pull request to merge it with main. Instead of working in main directly. Like we currently do. Dont do that.
It integrates via extension into VSCode. Which is pretty neat.
You can look at your branch, and where you would merge, and generate reviews. Useful for when we actually are deep into writing code.
The base version is actually free, you can log in using your github account. You also get a free 14 day trial when you do.
So maybe create the account after the holidays so you can use the features for actualy coding work

#### Perplexity
I mainly do any and all work with generative AI in Perplexity,
What is Perplexity?
Imagine an actualy organised workspace out of LLM Chat instances. That are fully customizable if it comes to models and functions used (Premium models are locked behind paid plans, but my Revolut offers a free subscription). 
You can define sets of instructions that carry over chat within workspaces, ensuring consistent answering styles.

#### What Models to use
Don't use ChatGPT. I find that DeepSeek/DeepThink performs better in terms of code.
However, if you can, use Claude. It performs best for IT related questions, finding issues, explaining concepts and so on.
CoPilot in VSCode has Claude Haiku 4.5, which is alright, especially for chatting / smaller simple tasks. However, Claude Sonnet 4.5 is vastly superior if it comes to anything more complex, or indepth analysis.

#### MasterPrompts, Tokens & Context
Different LLMs process Context differently, but whats consistent is that the initial Prompt has the most influence accross the whole chat. Anything after that is seen as additional context, and its efficiency quickly falls off.
Even so, there are limits to the amount of tokens a model can process as initial context before additional information leads to diminished returns overall.
I try to use 2k, 2.5k max, as a guideline.
Theres also a maximum of context within a chat, so eventually your model will start to hallucinate.
Another reason why good initial instructions, short concise answers and consistency when transferring chats is important.
For that reason I use Master-Prompts for all my Projects. They contain Style Guidelines, as well as key System, User and Project context that may be important to give you the answers that actually fit your SetUp. I will provide a part of my Master Prompt in this repo.

#### So should we write this project with AI?
No. You can, however, use it for simple sections, generate examples to see how implementation works. You can use it to find and explain bugs you dont see yourself.
As with work by others, you should always double check the shit you get.
From my experience, good generative AI models can be used to write decent, working code - i do it all the time.
The issue is that you still need to understand how to create software.
You need to know what you want, what you dont want, how to prompt, and how to control that the results you get actually match what you need.

#### Risks
AI is, for example, notoriously bad with safety protocols unless you actively ensure that they are implemented.
AI, especially GPT, also tends to loose context and hallucinate quickly
AI also tends to overengineer things, or do things terribly inefficiently (tbf i do that too.)
This includes starting to add "enhancements" that are well beyond whats neccessary or just doing inefficient or redundant stuff.
It might cure your imposter syndrome tho
# NOTE: Honestly, a great example was me starting to implement managers while sprinting through the whole implementation, just to realise halfway through that Django actually offers all these things, and i knew this.