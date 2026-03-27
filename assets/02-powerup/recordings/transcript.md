BiT: KB (Power-Up)

[00:00:00]

**Shawn Clybor:** Hello everyone and welcome to Innovating with AI's,
build It Together, knowledge Base Lesson for the Power Up Workflow. This
is Shawn and I am excited to dig in. So let's begin. So as a quick
reminder, the Build It Together framework is designed so that you can
provide valuable client deliverables at pretty much every level of your
tech skill.

And at every level of tech complexity. The second lesson, which is the
current lesson in the series, the Power up lesson is a great way for
Bootstrappers creators and strategists to enhance.

The core workflow lesson. And then the third lesson, the advanced
lesson. Will be the more techie approach to the same client solution.

What is a knowledge base? Knowledge bases [00:01:00] are sources of
truth for organizational memory.

They are like an encyclopedia to, an organization. It's processes,
it's protocols, it's operating procedures, institutional memory. But
instead of humans manually searching through these files or searching
through the knowledge base, AI is going to help us organize the
documents, process the queries, and then deliver the precise answers.

Every step of that process is AI augmented. It. The knowledge base
process involves first document processing, taking the documents and,
putting them into a form or transforming them in such a way that they
are,  tuned, specifically for ai,
document retrieval.

As a quick reminder, our fictional client, true Point. HR Solutions is a
regional HR consulting and outsourced HR services firm that is based in
Charlotte, North Carolina.

Quick recap of their pain points. They have a tribal knowledge
bottleneck. They're co-founder Elisa Fields, pretty much all of the
internal [00:02:00] questions and loses, an estimated 10 plus billable
hours a week to just answering these basic questions.

It takes a long time to get new consultants up to speed because of this,
fragmented knowledge structure. And the fact that it all flows through
the single person. There's template chaos, there's compliance risk.
They've got files all over the place. They're not version controlled.

It's all inconsistently labeled. The consultants who work for True
Point HR solutions are often playing detectives if they have to cover
for someone else. They, have a lot of time finding files and getting up
to speed on what their colleagues are doing. And there are very
repetitive, client q and as.

Consultants are just spending a ton of time answering the same questions
over and over and over again, and then having to go to Lisa, the
co-founder to answer them. So these are the problems that we are facing
and for which we are developing our solutions. So the tech stack today,
we'll be pretty simple.

We are working with Claude Cowork [00:03:00] and, really excited to
show that off a bit more. I like thinking of it as cloud code for the
rest of us. It has a lot of the features and functionality of Cloud
code. But, it's not designed for coding. I mean, it does code, but
it's really more about, operating, and automating your day-to-day
workflows.

To filter and tag all of my email or, to go through a folder on Google
Drive and process all of the data and create a spreadsheet out of it.
These types of tasks. But instead of using Claude's regular AI
functionality, it, powers it up with, functionality that is borrowed
from Claude Code.

So the technical scope then is Claude Cowork. There are custom system
prompts that we will also, use that are pre-generated and there are MCP
connectors. Just one really, for this lesson, we're gonna be using the
MCP connector for Supabase, really easy to set up, if everything works
correctly, as long as you already have a Supabase account, and as long
as you're logged into your Supabase account on your browser. The setup
for today's lesson [00:04:00] should involve, I think, two clicks to
get Supabase, run it.

Why are we using Claude Cowork and not Claude Desktop ai? Cloud Cowork
has a couple of things that really work in its favor. First, it runs
locally, which means that a lot of the work that you're doing is
happening on your computer rather than on the cloud. It has its own
virtual environment , which means that it just creates a safe spaces
that are, cut off or, isolated from the rest of your running, run,
running environment on your computer to execute code. And if anything
happens with the code or if there are any errors, it's contained to
that environment. And, the environment is also controlled. So, external
factors are less likely to cause bugs or to, to mess up the running of
the coat.

So it has its own virtual environment that it spins up, it has terminal
access. Command line interface, which just means that it can, execute,
functions on your computer. The terminal is, that little, app that you
pull up that you actually have to manually type text into, and that
[00:05:00] will then execute, different commands on your computer.

And, cloud Cowork has access to it. It operates mostly within a folder
that you'll select. But it does have some pretty powerful
functionality,

so this intermediate level power up build is going to be, ultimately
we're going to build a knowledge base. It's going to be connected up
via Supabase and it will be able to handle knowledge queries, and it
will work with our existing documents. It will support a template based
workflow.

I would say in terms of, market validation, the types of projects that
you can do could be anywhere between eight to $25,000, depending on
how, how much work goes into it, how many documents are involved, how
long the discovery is to put those documents together.

So I think the one thing today that's really important is this, this
lesson's really about building the knowledge base. And certainly we can
connect the knowledge base directly to Claude itself,

but there are a lot of other ways that you can connect a knowledge base
to a chat bot, as long as you have it set up in Supabase. You
[00:06:00] really just need to add that Supabase connection to, Zapier
or n Aden or Flowise or Vapi or any other tool that you happen to be
using that requires a knowledge base, .

You just have to go through that standard Supabase connection. So wanted
to point that out that this is really portable in terms of, um, what you
would do with it. But, assuming that you just set it up on something
like clawed directly, like we'll do today, probably more in the $8,000
to $10,000 range, depending on how much work you had to put into it.

Okay. So, what we're really doing today is building what is called a
rag pipeline or retrieval, augmented generation.

What's really exciting about the lesson today is that it's an all in
one package that walks you through the process of building a rag
knowledge base and is mostly automatic. It can be modified and adjusted
in many different ways, but the core functionality of it is all, already
included [00:07:00] as a part of the lesson.

So here's a quick overview of how RAG works. So if we start over on the
left here,

the user inputs this query and presses enter into, let's assume some
sort of chat bot or agent, or even claw itself. What the LLM then does
is it, converts this query to vectors. It uses a special, fine tuned LLM
that is available through OpenAI, regular.

API. But it's a particular model that is used to convert natural
language into sets of coordinates or vectors. And these vectors are
quite long, but they map out onto a three dimensional plane, that
organizes different words and language, by their similarity in terms of
their meaning and their concepts.

I use this example later in the lesson, but the idea of cat. Cat, kitty,
kitten, meow, meow, kitty, cat, whatever slang you can think of, or
cutesy term you can think of for cat, on a vector map would [00:08:00]
all be relatively close together because they all sort of mean the same
thing. But if we were searching for keywords on your computer and you
have a file on your desktop that's called kittycat, and you run a
search for, kitten.

It may pop up because KIT are the same, but if you keep typing beyond
the KIT, it won't show up anymore because it's a different word. So
that's the difference between a keyword search and, a semantic search?
a keyword search is looking for the exact letters and the exact words.

And a semantic search is looking for, similarity and meaning and
adjacency in language. So here's the retrieval phase then. The query
has now been, converted into vectors, and then these vectors are , run
through a search, in a knowledge base. And it is looking to match or
find 

 on the vector map, right? So it is querying,
it's looking at the vector database, which we will build on Supabase.
And it's trying to find, okay, if I use these coordinates, what's
nearby?

And once it pulls [00:09:00] those and returns those, it might return
five or 10 or even two, of the top hits in terms of what's closest to
that position on the 3D map. This retrieved context, is just given raw
back to the agent, as is like, here's chunk one, here's chunk 57,
here's chunk 256, and passes it back.

It takes everything you've put together. Here's the original query.
Here is the context that I've found, passes that to an LLM and says.
Here's the user's prompt.

Here are the chunks that I found. Use whichever chunk seems most
helpful, synthesize them and then generate an answer based upon this
context . And that's how it generates the answer. Photosynthesis is the
process used by plants, blah, blah, blah, blah, blah, blah.

I think things got a little AI over here. I love that.

 okay. So,
overall, hopefully that gives you a sense of how retrieval [00:10:00]
augmented generation works.

And of course that's obviously going to be a lot more accurate than,
here's 150 documents, a thousand pages total.

That pollutes the LLM with thousands and thousands, if not millions of
tokens, that are, not helpful and it is just gonna make it way more
likely that it will hallucinate and not be able to find the correct
answer.

Okay, so how are we gonna build this today? We are going to use Quad co
work to design a seamless, efficient rag pipeline that will transform
unstructured data into actionable knowledge. And we provide as a part of
a lesson, I think 12 different, generated files that are, generated by
ai. They look like real documents. They, relate to various HR functions
that True Point provides, but they're not actually real. We're gonna
take those documents and we're gonna convert 'em into this, rag
knowledge base. So the steps that we're going to use will be first
file, intake and hashing.

We're gonna intake the files and we're gonna hash the [00:11:00]
files. Meaning we're gonna generate unique, codes for them. Multiple
formats, so Doc X markdown, PDF, and CSV, and just get them all prepped
for processing and version control. We're then gonna convert them.

It says docking here. Docking is a, tool that, downloads libraries that
help you convert and extract data from different document formats into
structured markdown documents.

The libraries it uses are quite sizable and I found that they very
quickly overwhelmed the virtual, memory so I, instead I wrote scripts
that, cover similar functions that are much more lightweight. So it's
less robust than docking.

But for the purposes of this lesson, it works for basic file types and
it's, not going to overwhelm the system. Okay, so it intakes the files.
It converts the files.

It is then going to break the files up into smaller chunks or bits that
can be generated into embeddings and added into the database. And it's
going to [00:12:00] analyze the document and the type and how the
document is structured, and then it has one of several different
chunking strategies that it will use to extract that data.

From these chunks, it generates the embeddings. And it uses the OpenAI
API to do this. It then puts everything into a database that it's going
to create in Supabase.

And then it will connect it together. It says MCP integration. What
we're really doing is we're integrating it via the Supabase connector,
which could, in theory be used for other projects, or databases on
Supabase.

It's a start and there are a lot of different ways to connect this up,
and that's something that I'm gonna be exploring more in the advanced
lesson. What are some of the ways that you can take this and link it
into other systems, for clients. Okay. So let's talk a little bit about
operational costs.

Claude will require, I think, at in the minimal a, a pro account, which
is $20 per user, per [00:13:00] month. I do not believe that Claude
Cowork operates if you do not have a pro account. I don't think you can
use it on a free account. You can also use a team account, which allows
different users to access the same things that you're working on.

It's much more collaborative. There are higher usage, usage limits, and
you get priority access to new models and features. I think just for
you, if you're working on your own, quad Pro will be enough. And if you
wanna just set it up for this course, get everything built and then
revert back to the free account, you know, by all means, the MCP
connectors that we're using themselves are free.

So we're, this lesson, we're only using the Supabase connector, but
any MCP connector that you use that's free, on its own, you don't have
to pay anyone or anything to use those Supabase. Supabase has a cost.
You have to pay for it as, a platform and when you set it up, it could
be anywhere from free to $25 a month.

The free tier gives you 500 [00:14:00] megabytes of storage on a
database. And, you can store files in the database up to one gigabyte,
and it allows for 50,000 monthly active users to access that database,
which I think for our purposes is pretty, sufficient, to be honest. So
you may not need more than the free tier here.

However, be aware that when you create a project, there is also a charge
for individual projects. So the project we're creating today will cost
$10 a month. But again, it's a type of thing that you can set up, use
it for a couple of weeks and then get rid of it if you need to, and you
will not get charged for it.

So keep that in mind. And then finally, the OpenAI API for embeddings.
You need to have an OpenAI account. I believe that also needs to be a
pro account, so you will need to pay. To get access to that. And once
you, have it, then when you create the API, obviously you get charged
for the, the usage.

And the usage varies [00:15:00] depending on the models that you're
using. Using the, embeddings fine tuned model through the API is a
little more expensive than using the regular API LLMs. Like four oh or
four oh mini. But again, it's really not that expensive. It could be
around $5 total to do the work that we're doing today.

I actually think that's, I think that's pretty high because this is,
that's $5 for a hundred to 500 pages. I think we're maybe doing 40 or
50 pages total, so it's probably gonna be more like 50 cents for the
work that we're doing today.

It would be about five bucks to generate all the embeddings. So if we
add all up all of that up together, we're looking at, you know, less
than a hundred dollars a month for this whole thing to run and be used,
on an ongoing basis. So it's, pretty affordable as these types of
solutions, go.

Certainly enterprise solutions can be thousands of dollars per month.
And this is a fraction of, of that. Okay. So, as a quick [00:16:00]
note, the architecture is ultimately flexible. This project will work
in, other ways. I, I will point out that when it comes to the LLMs that
you can use, these other tools do not offer, as far as I know currently.

Anything similar to what Claude Cowork is, this sort of interesting
blend of a traditional desktop LLM and an AI coding app. So, at least a
time of recording. I'm not aware of any of the other major providers
that offer something quite like that. There are some new things popping
up, like open cloud, which I don't recommend you use, that are similar.

But for the major providers, this is still, I would say, pretty open
frontier. So keep that in mind. I think that for today, you're probably
gonna want to use Claude Cowork no matter what you do in terms of the
embeddings API, you definitely have some options. You don't have to use
OpenAI today if you don't want to.

I would really recommend you just stick with OpenAI for today to keep it
simple and straightforward and to [00:17:00] minimize the amount of,
variables that you're creating. So if there are any errors, you can
kind of, narrow that down and say, well, hey, I'm doing the video.

Exactly. So there, you know, I know exactly what's wrong. If you're
doing something differently, you're creating all these extra variables
and then if something goes wrong, it's a lot harder to troubleshoot it.
Okay, so the Vector database itself, I'm using Supabase. It's, we
really recommend it as a backend, as a service.

We have a whole lesson on Supabase that, I encourage you to check out.
But there are other vector databases that you can use that are a little
more lightweight and fine tuned to, the specific use case that we're
doing today. In, in all honesty, using Supabase for the project today,
some might argue is, overkill.

Because we really just need a simple vector store, not this like whole
robust row based access platform with authentication and the ability to
link up payments and all this other stuff, right? We just really need a
basic knowledge base. And so for that you could use Pine Cone or
Quadrant and there are other, solutions as well.

Pine Cone and Quadrant are sort of the two, most [00:18:00] popular
alternatives out there. So you could try those if you wanted. If you're
familiar with those, you can sub that in here instead. But again,
you're gonna have to figure out then how you get that connection
between, Claude Cowork and whichever knowledge base it is that you use,
you would be responsible for figuring out how to set that up on your own
and that.

Pretty necessary for running this, this lesson. And then finally
document processing. There are a lot of options out there.  but what I ended up doing is
just going with my own custom parsers that I wrote as scripts that are a
part of this lesson .

I did that because some of these libraries, are very, large and can be a
bit, resource intensive. So to keep things slim and lean and mean, I
wrote my own simple scripts that can be used. But again, if you were
looking to build this out and make it more robust, you may look into,
expanding and, integrating one of these other document processing
services, into, the knowledge base that we're building.

We are gonna be working today in Claude on the desktop app [00:19:00]
right here. This is how, it will look for you. View. Have three options
up here. Claude Cowork right here is what we'll be using today.

Cowork allows you to spin up, a virtual environment, where it can run,
and execute script. It can run code, in sort of a contained space that
will not, impact or, or damage or, corrupt anything on your operating
system.

And, it's a lot like Claude Code, in terms of its tooling, so it has
access to, skills and connectors.

I'm sure it will be adding agents soon. At the time of recording this,
it didn't have them. And it operates with, the core instructions that,
 in Claude Projects. We, they just call them
instructions. But of course, by the time you get to Claude Code, they
refer to it as a Claude MD file.

And so, again, this is an intermediary space where it operates with
Claude, Claude Tooling files like the Claude md. Not in this more, the
more simple, structure of, Claude Chat. So yeah, it's a midpoint
between Claude Chat and Cloud Code. [00:20:00] So we're gonna be
working on this, and when you spin up Claude Cowork, the first thing
that you need to do is to select a project or a folder, where all the
files are that, that this virtual environment will be using, as it
executes your projects.

We are going to pretend we don't have that yet. And we're going to go
get it from my, GitHub account here that is posted, with the lesson on
the Innovating with AI course platform. You are gonna wanna download
this even if you've already downloaded it once. I would download it
again. Updates happen.

You can see right here. I made some what are called commits. I committed
some updates to files just about a half an hour ago. And as we know,
GitHub, the Git system tracks all of these changes over time. It has
really rigid version controlling and you can branch off from these
different versions, which is, really great for development work and,
multiple people working on, projects, at the same time.

But again, it allows me to do things like update the code base, make
sure things are [00:21:00] running, and then when I feel good about
it, I can merge it into this main branch here where you would, where you
would download it. So it has a lot of great functionality like that.

Okay. Now if you had, a more direct connection to this knowledge base,
if you had forked your own copy of it locally, if you had, if you were
following it, if you were connected to, GitHub, through, the command
line interface or an MCP, you could certainly just tell Claude to go to
this project and grab the files.

I'm gonna operate by the strict organizational structure of Claude
Cowork. It looks for folders, and so I'm going to give it a folder. So,
to do that, either if you're operating in Claude code already, you
could say, Hey. You fork a branch of this repo and, download it locally
to, and then give it the directory you want it in presumably documents.

 instead just stick to the downloading
method. Click code right here, click download, zip. And again, just make
sure that you're doing that between lessons because, updates will
happen. So I've already done that. It will download a [00:22:00] zip
file and when you click on it, it will just, unzip it.

Alright, so let's go back to Claude now and, choose a different folder.
I'll actually just choose the one that I just downloaded. Okay. And
then I'm gonna click on assets. Really important, do not just link this
main folder. You want to click on assets and then click on Power Up.

And you want to add just this power up lesson. Okay, allow Claude to
change files in O2 Power Up. Yes, we want Cloud Claude to be able to
operate within, this file structure and make changes to these files. So
I'm going to blanket allow it. If you wanna play cautious, you could
just allow, obviously you can redownload these files at any time.

So it's really just operating here. The worst that happens is you
corrupt everything and you download it over again. So I would say take
the risk. Always allow live dangerously for once in your life. That's
what I say. So we're in. Okay. It's set [00:23:00] up. And the first
thing that we're going to do is a type run, and that's it.

So this is going to take a moment to spin up and connect things together
and to begin thinking through processes. You can see here it says
thinking. You can click on this too, and you'll see it's thought
processes. I would note also, i, as a general rule have, doesn't look
like, oh, here. Yeah. I'm using Opus 4.6.

This is a very token heavy, LLM and if you're not using, a more
expensive plan like I do, if you're using like, maybe just the $20 a
month plan, you may wanna try running this on sonnet instead. It should
be fine. I have run portions of this in sonnet and, it didn't cause any
problems, but you may want to switch over for parts of this, and test it
out just in case anything is happening.

This could be a variable that you wanna check. Okay. So it's running,
let me. Talk about a couple things that are happening and then we can
get back when we have some free time to this interface. So it's looking
around [00:24:00] and it checked its available skills list and it
looked through the prompts that were available and it saw that the
prompts that it need, are not their currently.

And so it now is digging into its core instructions and it is, setting
up, the skills, that it needs to function. So, it then went on to build
its own, what Claude, what Anthropic is calling a plugin and a plugin is
an attachment or a connection that you can use in Claude Cowork, that,
packages together, scripts and skills, MCP, rules and, setup.

And it's all together. And so you just have it in one single package
and everything runs together. This is a really key part of the
architecture, for this build. And so what it did was there is no plugin.
It, it created its own from the instructions that we included, in the,
in the repo.

So if we go to assets and we go to power Up, and we [00:25:00] look
here, we can see that there are a bunch of, files here that are now all
added to Claude that, include builder tools, MC P set up, connections,
instructions, migrations, migrations mean. These are the, right, these
are the, sql, documents that, execute, the creation of tables in, a
project database in Supabase.

So these are all pre-developed for you, and ready to go and tested. So
you will execute these and it will set up that database, those tables in
Supabase, automatically. It has its own pipeline, and this pipeline is
kind of the core of what it does, right? It's ingesting documents,
ultimately into a rag database.

And it's converting source documents that we give it from, true point,
and it's converting them into first markdown. Then it's embedding
them, at creating chunks that are stored in [00:26:00] Supabase. And
then finally it will be able to access those and retrieve those by
running searches, directly in clawed.

So it creates, its, its own, rag, rag knowledge base directly from the
knowledge that you provided. So, it has all the templates here to do
those various things, right? So you have, like, for example, the
embedding, this is. How the embeddings are generated and it has all the
steps already mapped out and how the LLM should, undertake this process.

What it means is, is it will know when you say, I need you to embed this
document, it will have a pre-developed set of scripts and templates that
will execute that. At most, if it needs to make some sort of intelligent
modification, based upon a weird file type or some sort of, exception,
Claude will be able to adjust its own tooling, to function and operate
with these edge cases that you throw at it.

And of course, if anything ever goes wrong and it all blows up, if
you're version controlling your version on GitHub, you can go back to
it. And if you're not, you can always [00:27:00] reset from my
template and just start over, right? So it gives you a lot of room to
experiment and play around and, mess up if you have to.

Okay, so that's all in here. Also in here is this dot Claude folder.
And this dot claude folder is the, the tooling of Claude itself. This is
how Claude operates. These are sort of like the core instructions that
Claude co-work needs to, function correctly. And so you can see there's
a read me here that just sort of lays this out very generally, both for
you and for the ai, like how it operates.

 it has also,
agents involved, so it's all set up and ready to go. We can click
agents. You can see there is one agent here, the rag reviewer. So this
agent is actually specifically, built, to run, this particular process,
reviews the rag pipeline output for quality issues, checks, chunk sizes,
embedding coverage, metadata completeness and retrieval quality.

And as a part of this larger pipeline as it's running. [00:28:00]
Claude will run that subagent and ask it to review the pipeline output,
and make sure that, the documents are being chunked correctly, that
there's not a bunch of, you know, empty chunks and, and wasted tokens
and weird random characters and, and whatnot.

And a part of these, these workflows, also includes here the source
files folder is very important. The source file folder is where we are
keeping copies of, well, let's see, documents to ingest through the rag
pipeline. So these represent the kinds of files a client's knowledge
base would contain, HR policies, compliance checklist, templates, and
reference data.

And so what we've done is created, all of these fake generated true
point documents with data in it. And these will be the documents then
that we will be, processing, pre-processing, and then, embedding into
our [00:29:00] knowledge base and ultimately testing to make sure
that, that the operates properly, or at least that's what, the testing
piece will be.

I think a lot more heavily covered in the, the advanced lesson, which I
would recommend checking out even if advanced might be a bit, above and
beyond your skill level. If you make it through this lesson, you sh I
think I really encourage you to just, try the advanced lesson and see
how it goes.

A lot of it will be self-explanatory, in the same way as this lesson,
just with slightly more complex skills and, expectations for you to be
able to set things up, at the beginning. So here we are. We have all of
these source files, and you certainly can pause here and click through
some more of those if you want to familiarize yourself with them.

I think now would be a good time, for me to go back to the tooling that
we just built. And you can see right here, these are the actual
instructions of what we're doing right now. Confirm you have a Supabase
project. Confirm you have an OpenAI, API [00:30:00] key, confirm you
have Claude code or Cowork with the Supabase MCP connector enabled, and
you have the source files in this lesson.

Okay, let's go back then to Claude and see how it's doing with that
task. Well, it's set up the initial skills, so let's click save
plugin. All right, we'll click manage over here. I want to see it. And
here it is. I have another pipeline, plugin, here that I downloaded.
Anthropic has, you can click this plus and then click Browse Plugins.

They have a bunch of plugins that are already built for you. But of
course, mine, ours is custom built, for Innovating with AI students. So,
that one's right here, rag Pipeline tool. So we click on that and we
can see that it's got skills and connectors. 

 for now, I found this project to work pretty well. So the
connectors, this is the one that we really need, is Supabase. And we
know from the lesson that that's going to be one of the first things
that the, the LLM is going to ask us. And then we have these three
skills here that, have been built.

[00:31:00] And these will then run, specific processes in a specific
way. So, it's saying this is what you do, you test the quality of your
embedded knowledge base arguments. This is just a variable that means
that like, somebody may, include with the execution of the skill. They
may say, execute the skill and here's some things that I want you to do
along with it, right?

Or it, they may also flag it with something like, dash, dash all. So you
could say like, you know, forward slash calibrate and then dash dash
all, and you're kind of modifying sometimes these, commands have
modifications that you can, that you can add to them. So that's a part
of what's called arguments.

And if there are no arguments, run the full test suite. So yeah,
arguments. Another way to look at them is they, they're sort of like
bookmarks that allow you to say, I don't want you to do all of this. I
want you to do like, you know, dash, dash, do this in a modified way,
right? Okay. So that's one skill.

Ingest is another skill, and that's for actually, you know, ingesting
the data into the pipeline. [00:32:00] And then we have the setting up
the rag pipeline itself. And again, you know, feel free to stop and
pause and check out these instructions, read them a little more closely.
And we're gonna be seeing all of this in action, right?

So don't feel like, ah, I have to stop this video and read every single
one of these files. I don't know what's going on. They will all happen
in real time. This is more your backend introduction, so don't get
overwhelmed yet.

Remember, so far the only thing you've had to do. Is type, run and
click save plugin. So that's, we're, we're now. Okay. That's it.
Alright. But let's continue. We've saved the plugin. So let's say
again, let's say run. You could really say anything you wanted, of
course. And I'm gonna exit out of this 'cause we've already saved
that plugin.

And while that's running, I'm gonna talk a little bit now about, what
you can see over here. So, the progress, that's pretty straightforward.
This is where it tracks tasks and you'll [00:33:00] see some tasks
populating here relatively soon. Next you can see, documents, that it
is, that it is accessing and adding to its memory and context as it
goes.

And then here are the tools and the referenced files that it uses for
the specific tasks. Okay, let it's, let's see what it says. It says,
welcome to the Reg Pipeline Builder. We'll be setting up a retrieval
augmented generation pipeline that ingests knowledge based documents
into Supabase PG Vector.

This is just the extension that's used to do vector searches using,
Supabase. You're starting fresh, so it'll begin with step one
environment setup. Before we dive in, you'll need to do three things.
You'll need a Supabase project, your Supabase service rule key, and an
OpenAI key. Do you have these ready or do you need help getting any of
them set up?

I need help. What are you asking me to do right now, man? Are you
kidding? I don't know what that means. Come on. Sure. What do you need
help with? Are you looking for guidance on one of these? Like, help me
set it all up. [00:34:00] Don't be coy. Okay, let's do it. I'll
kick off the set up skill and walk us through everything one step at a
time so you can see now, it's now running this.

It has now entered that into its context that is now a skill that it is
executing. And this is that setup rag skill we were looking at earlier.
Everything's blank. We need all three API keys. Let me start with the
first question. Do you already have a Supabase project? Do you need me
to create one for you?

Once we sort that out, I'll need you to paste me these three values.
Create a project for me. I will say,

thinking about that one, I'd love to create from you, but it looks like
Supabase MCP connector isn't connected yet. You'll need to
authenticate it first. Aha. We gotta go to settings. [00:35:00] Well,
there is no gear connector, my friend. Oh, there is managed connectors.
There it is. All right, take that. Okay. You should see Supabase listed.

There it is. Another way to get it would be just to go to the connectors
and then you could go to, hmm. I think maybe just here in type Supabase.
Well, here it is. Cool. So let's click connect. So that takes us
automatically over to our browser, where it will do an OAuth, API,
authentication.

So, I've already logged into my Supabase account. You do need to create
a Supabase account before you start this project or. Pause now and,
create a Supabase account. It's very easy to set up. I think you would
just need to make sure that you have, you know, a credit card on file
and a basic understanding of how it runs.

We have a lesson on Supabase that, can help you give a bigger picture
overview of how Supabase runs. Otherwise, a quick [00:36:00] tutorial
online, literally just to log in and do the basic setup that you need to
do, which is to create yourself an organization. You don't even need to
create any specific projects.

If you have your, credit card already entered, for charges, be aware
there will be a $10 charge per month to set this project up. Claude
itself will also warn you about that. So we are now here and let's
click select an organization. We're gonna go with Cly Work Consulting,
and we're gonna authorize Claude.

Okay, so Claude now should have API access, once this verifies, and that
will then, allow us to access Supabase back in the project. There it is,
it appears to be connected, so that has now satisfied. That should
satisfy our friend back in the chat. So let's return. And you could
very easily start new sessions.

I would recommend, doing that, at various times. And the, project has
been designed to [00:37:00] try and prompt you to also start fresh
sessions from time to time. If it doesn't, just keep in mind that you
may need to, particularly if you begin to notice that the memory is
compacting, it says compacting, and then it's, taking a long time to
run again.

What that compacting means is that it is, filled to the brim with all of
the context you've provided it. It tracks that context by tokens and
token usage. And once that token, maximum is hit, it has to then go
through its entire context memory and begin weeding out information to
create fresh memory.

Generally you want to try and avoid doing that too much because it can
at times be a bit sloppy in the way it compacts memory. I do find it
works quite well these days, I think. But it is just something to be,
something to be aware of. Okay, so, let's see. Let's try it now.
Let's click, test it now and let's see what it does.

Okay, it's [00:38:00] thinking.

My guess is this is a good moment to restart. So I just hit Command Q
and that shuts Claude down. And that's important to keep in mind as you
do this, that there are a couple of points where, Claude will need to be
restarted to recognize any changes or any updates.

Right? Excellent. So if we go back to this now, we can see it's
starting the workspace fresh. We will wait for that to complete. It's
complete. We'll check the connectors. I see Supabase. Let's try test
now.

It'll take a moment again because it's,

here we go.[00:39:00]

Hmm.

That's interesting.

I am gonna try, when in doubt right. Please test.

It could be possible that we need to just start a fresh session here.
This particular session seems to be in denial that we have, done what
had asked us.

Ah, okay. It wants us to start a new conversation, so let's do that.

Okay. So we've started a new conversation and we've said run. So
let's let that go for a moment and we'll see what happens. Okay. This
time it's recognized that the three skills are registered. [00:40:00]
It still recognizes as starting from scratch, but it does have the
skills.

Okay. Supabase project, please.

 Okay. So
it's looking into it. It's $10 a month. That's fine by me. US east
one is good. The location really, I mean, it can be a little faster if
it's closer to you. I don't think it matters a ton.

I usually just go with, US one east. Okay. Confirmed that it has
explained its cost to me, box checked, and it is now creating the
project. So, the project creation piece is going to take a little bit of
time, to initialize so we can go over [00:41:00] to, oh, well actually
here. Very smart. It's saying while we wait, I need one thing from you.

I need your OpenAI. So it's giving an address, a URL, and it says, go
to this URL and then, under the secret keys copy the default secret key.
Click the I icon to reveal it. Okay, cool. Let's try that. So we're
gonna go over here. Let's close this. And, just for, for kicks, let's
go. Oh, there it is starting, but it's created.

So let's go to open AI's API, oh, no, that wasn't right. Hello? Oh, I
see it needs a Supabase. I was reading OpenAI. Okay, so here we are. So
we are in the right place. We're under Rag Pipeline. And here's the
API key. So it actually gave us the link to where we need to copy the
Supabase API. So it says to copy the I to reveal it, but we don't
actually need to do that.

I'm gonna click copy here. [00:42:00] I'm gonna go back to Claude
and yes, I'm going to paste it in. 
Claude Cowork is running on your local environment, so the, possibility
of a security lapse is pretty low. However, if this is concerning to
you, it's definitely not a problem to go into the folder, for the
lesson and find the, ENV file.

It doesn't appear to be set up yet, but once the ENV file is set up, it
will show up here. It would be, I think the best thing to do would be to
paste that into the ENV file. We can even try it, right? Create the ENV
file and I'll paste it directly in.

and obviously you, the key is exposed here on the, the recording. And I,
I will delete this after I'm, I'm [00:43:00] done with the lesson,
but that's okay. Okay. It's in, right. Okay. It's in Pipeline
Scripts. ENV. So we're gonna go to Power Up. We're gonna go to
Pipeline.

We're gonna go to Scripts, and there's the ENV file. We're gonna
click on that. It opens it, and you can see. Put this a little bigger.
And it is already out of the URL and it's asking for the key. It says
paste it here. So I'll paste it. There we go. 

 Okay. Oh, still needs the OpenAI key, right? How do I get the,

I am lazy. Tell me how to do it. I don't know. There we go. There you
go. Spoon feed me. That's what I want. Alright. API. Keys. Mm-hmm.
We're gonna create any secret key now, important that you have this,
account set up on the backend. I'm [00:44:00] assuming, that you
would have an OpenAI account. You may not.

You could use, Gemini, API. You could use, really any LLM that you want.
You would just need to figure out the process for getting an API key
your own way, and then tell this project, Hey, instead of using OpenAI,
I am gonna use something else. Keep in mind though, it's really
important we're not using just the regular OpenAI API, we also are
using it for embeddings, which is technically a different model that it
can access through the API endpoint.

But you do need a specific type of model and not every LLM is gonna
offer that out of the gate with the same API. So buyer beware with that.
If you're going to try and use something that's not OpenAI, definitely
ask Claude first. Hey, will this project run? If I give you a Gemini API
research this and let me know what you think.

I would eliminate variables like that, by doing it exactly the way I do
it. Setting up a OpenAI account for a month and paying $20 and a couple
dollars for this, API, I think is [00:45:00] worth it as a learning
tool. And, yeah, you know, many people can write it off as a business
expense.

So let's clip create a new key and we're going to say, Innovating with
AI test key. And we're gonna put the project in. Yep. I've already
created a project. Create the key copy. If you haven't created a
project for it yet, you can create a project up here. That way you can
track different things that you're doing for different clients and
you're getting data about, you know, consumption and token usage and
cost and things like that.

It's good to just keep these things sorted. Okay. We have the key that
we need. So let us return and I'm gonna just do this lazy way. Now.
Take my key, take my key, sir. Got it. Let me add that to your ENV file.
You do that, man. You do that. Okay. Updated. Now it's going to install
Python dependencies and set up your database.

Want me to run, set up, rank and handle that [00:46:00] automatically
or would you prefer to step through it manually? I definitely do not
want to do anything manually, spoon feed me. Please ease. I'm not gonna
make this easy for you, my friend.

Now it's working on it, it's thinking ha say no more. Ha. Good natured
chef. We jape. Alright. There it is. And it's now running. You can see
the setup rag skill and it's actively using the Supabase, MCP
connector. So, cool. And there it is. It has, let's see what it's
done. It ran that skill. It created a to-do list.

Then it's checking all of its environment variable flags to make sure,
and you can see when you click here, there are flags. That are being
set, that are letting it know where it's at in the process. And these
different, [00:47:00] gates are what is helping it understand from
session to session what's been done and what's remaining.

So if you ever find yourself at a place where you feel like, oh, well I
did X and I'm starting a fresh session and it doesn't understand me,
and it's like, well, you need to do why, but I've already done it.
That may just require you having to update these flags here. And the way
that you can do this is, you know, I think the easiest way if you don't
wanna dig into the actual files and manually adjust them is to just ask
Claude to find where, 

 Okay, so the environment variables are set.

So now it's moved on to what are called the dependencies, which just
means the, applications and libraries and, other tools that run in the
background that, it needs, to be able to execute these Python scripts.
So it, is finding these dependencies and many of them are related to
Python because we are running Python code.

So it needs to set up an environment for Python to run in, at this
virtual environment. Then has a virtual environment for Python. So there
are multiple layers of virtual, [00:48:00] here. 

 So, moving on. Now it is, looking at the database migration
files and it is looking into setting up our database on Supabase. Oh, no
correction. It is already

built that Supabase database while I was, rambling, about, French,
structuralist and post-structuralist philosophy. So let's go to, let's
go to that project then. Where is it? We're in test lessons. How do I
get out of here? Oh this. I'm in OpenAI. Second time today. I've done
that.

Alright. Here we are in Supabase, not OpenAI. We're in Rag Pipeline.
We're in that project and if you want to see the tables that have been
created, click table editor. There are two tables here, there chunks and
file metadata. And they are already structured with the exact, setup
that we need with the exact type of, column.

The column type is already established. These things in a, SQL database
are really important. It's not like Google where you can just enter any
type of data [00:49:00] into any field and then have it, be
understood. 

For now, I want to point out two very important things. These bright red
parts that say unrestricted and R-L-L-R-L-S disabled. That's really
important. And so, there's a couple ways that we can handle this. One
way is to, well, let's just click on one of the red things.

We can, one, we can just enable RLS for this table. We can also go to
the advisor here and you can, it'll show you security issues. You can
click on them and you can click right here or ask assistant. And then
Supabase has its own, its own agent that, understands, its systems and
can help you make the changes to, harden up the security on the
database.

So we're gonna tell it to make the change. So it set everything up and
that's all it did. So this is a good place to sort of, you know, tweak
it. So we're gonna say, reviewed Supabase and security is a concern.
RLS [00:50:00] is not enabled. And I got this message for both tables.

What are you gonna do about that, my friend?

Without RLS Enva enabled, anyone with your on key could read and write
those tables directly from a browser. For this pipeline, the tables are
only accessed by your Python scripts and the MCP connector, not by end
users. So the simplest fix is to enable RLS with no policies, which
locks the table down from the public, API while the service roll key
bypasses RLS.

Okay, done. Both tables now have RLS enabled with no policies, which
means service roll key, full access unaffected, a unpublishable key zero
access, completely locked out. That warning should be gone now.  Let me refresh the page.

There are some warnings though. So  for
the sake of the lesson, this might be a good place for you to pause the
video and continue, this process that I just started and make sure
everything here is, [00:51:00] secure, to your liking. I am not going
to do that.

I'm gonna actually start a fresh session. So I'm gonna click new task
and we're still in the same folder here. And I'm going to say, just
run. I'm gonna be lazy, still run, run free. Okay. It's thinking it,
and there you go. It automatically knows because of those flags in the
ENV file, it knows exactly where it is in the process.

See, this is memory management right here. You don't need a final
folder for this project with 500 pages of every, prompt that you've
ever, executed, right? I just need it to know that certain key status
flags have been passed and then everything else is in material.

If it got to that place, that's all it needs to know, right? It's a
need to know, a need to know basis with, with, Claude. Alright, so it's
now running through all the pre-flight checks, which means that it's
making sure [00:52:00] that all the skills are there and Supabase is
running, and, everything else is connected.

See, environment variables set, source files are in the folder. The
Supabase tables exist. Oh. It had a permission problem, but it just had
the wrong project id. That could be something that we may want to pursue
right down the road. It could be just annoying that every time it tries
to access this project, it gets the wrong id.

So you could say, look, do you have the wrong project id? Update it.
Where are you getting the project ID from? Why is it wrong? Like, and
just query that and iron it out. It may seem like you're sort of
chasing little things for no reason, because ultimately it worked. But I
find that anything like this that goes wrong,  it
introduces an element of uncertainty where the LLM can kind of go askew
and be like, oh, I gotta fix something.

And then that's when it starts going down Weird roads. As long as
everything that it does is something that it predicted should happen and
there's clearer, rules and guardrails established, it's just
[00:53:00] less likely that it's gonna go wild on its own. 

 So it has now, made sure that all of its dependencies are
installed. It has registered all of the files that we created. 
So it converted the files to mark down already.

So regardless of PowerPoint, CSV, whatever it was, PDF, it's all
converted. There are chunks created across 12 files.  Look
at this. It's even chunked all the data and added it to Supabase
ingestion is complete. Here's the summary. 12 files processed, 89
chunks embedded zero failures. File chunks and strategy.

Strategy means, how do you chunk this document because there are
different ways a document can be chunked. You don't want a document to
be chunked such that it just breaks off mid-sentence, right? You don't
want a table of data being chunked so that you're getting all of the
data from the tables, but then the schema headings are in another
[00:54:00] chunk.

 So this is
just, the strategy means based upon this type of file, the AI made its
own intelligent decision to chunk the data in a particular way.

Most of them were done by headings, meaning that, it just, every
heading, it chunked it. And a part of the scripts that run, a part of
the things that they do is they build these document anchors that map
out, how the document is structured, and takes note of are there
headings, is it organized well?

What is the organizational structure? And based upon that organizational
structure, it recommends by headings, recursive means, right? It's just
pulling back layers and levels, like, you know, looking at a, then
looking behind it and then looking behind it and making the decision
based upon that. Good strategy.

It's CSV, so just dump the whole thing in together in, in a piece. And
you can even see this is two chunks and this one is literally just one.
It's just the whole TA table. And certainly with things like,
structured data, having the data chunked and embedded [00:55:00] is a,
a lot less important.

One could even argue, I, I may even want to, modify this in a future
version where the, the, structured data is not being chunked at all. AI
does a very good job just, you know, running edge functions and, and,
executing, SQL queries, directly, into structured data. So in many ways
this is, 

 it's really the unstructured stuff that I
think matters the most when it comes to, when it comes to, chunking and,
embedding nonetheless, currently at least it's embedding, even the,
these pieces of data. And I'm a little bit less worried about it. One
of the big things against it, of course, as I said earlier, is that the,
the, the headings of the data, can get mixed up.

 Again,
not something for me to worry about right now. This is something that
you can tweak, but keep in mind that if you're having issues with your
structured data, you may want to just cut this piece out and tell the AI
to cut this piece out.

It has the ability to update the files that we've given it. So if you
wanna change its core instructions, go ahead and change it and say, I
need you to add in your core instructions. Do not [00:56:00] chunk
structured data, just add it into a database to create a new table. Put
it in a new table and then link that table and that's it, right?

Okay, so let's go over to Supabase and see all of this data, that it's
supposedly added. Let's verify this, independently. Whoa, that was
empty before. And so was this. And you can see here, file metadata. This
is just a broken down inventory of each file that was ingested. The
embedding model, its status, the strategy that was used to chunk it.

The chunk count, it's got its own unique hash, so it can be found. It
labels its file size, the file type it lists even where it's located.
And then it's linked to the chunks, right? So you have these two IDs.
One file ID. Is for the metadata column. [00:57:00] The other is
internal to this particular table.

So that way it's cross-referenced. If you pull this, you'll know that
this is where it is connected in the file metadata table, right?
They're both linked together. So this is the big one. These are all the
chunks. And you can see, let's click on one of these, vector
embeddings. Oh, it won't even show it.

They're ginormous, they're huge files. If you were to open one of
these, let's, yeah, let's actually go and I'm gonna take a look and
see if I can find,

well, there's the chunks and you can see they're all chunked up piece
by piece. Okay. Here were the files that were converted into markdown
from their original format, and here's the registration of all the
files and their metadata. So these were the output files that were
created. Okay, 

 interesting. So that makes
sense to me. It's chunking it, putting it directly into the database.
There doesn't seem to be a particular reason why you would need to have
that file of [00:58:00] embeddings on your computer directly.

If you did want it, again, that's a modification that you can make. Not
a problem. That's an interesting design choice. You can see there are
pieces of this here, where even though this whole thing was built on
scripts that I already wrote, it was making intelligent changes to those
scripts, as it was creating this new system that I packaged up for this
lesson.

So, that seems to be a more efficient way to doing it. It seems to work.
Let's, let's find out. So I'm going to create a new task here. We're
gonna go fresh and I'm going to say, run. Let's just say run and
let's see what happens. Now. We've said run price. Th rice, I said
run. All three skills are already installed.

Yeah, they are. It's checking, its flags. Everything is set up and
justice and ingestion is complete. That means you're ready for the
calibration step. Testing, retrieval quality. Yeah, that's correct.
Your environment is fully configured. 

[00:59:00] Let's calibrate it baby.

It's explaining, it's going, there we go. There's that execute.

Project ID problem again. So this is interesting. Again, this is
something that I would, and may even end up reviewing and tweaking
before I, release this lesson. If not, you know, again, not the biggest
deal. Everything worked out here. It's just, you know, a, a a to a
token run extra context, and a potential opportunity for something to go
wrong.

It tried to run again, but it doesn't have the OpenAI module for
Python. It needs that to be able to, to run, these calibration queries.
So it just installed, another dependency. So, yeah, keep in mind,
you're probably gonna want to have maybe five or six gigs worth of
space to let this whole thing play out.

 It lists the query, the
expected source, the top score, [01:00:00] and it hit the file that it
needed to hit five for five. Every query returned the expected source in
the top results. Vector search is doing the heavy lifting.

Most results have a text score of 0.000, meaning the full text component
only kicked in when there was a strong keyword match. The 0.7 0.3 vector
text weighing is appropriate for these conceptual HR queries. This is
running what we would call a hybrid search, meaning that it is, running
for keywords to match and it is running vector similarity.

So a vector similarity would be something like cat feline, animal dog,
kitty, kitty, cat. So on and so forth. They're not necessarily similar
in terms of the actual, like letters of the alphabet that are used to
create the word, but conceptually, semantically, we think of them as
being closely related.

It could also mean words that are closely, paired or come after one
another, like kitty, meow, kitty milk, kitty bowl, things like that are
gonna have a closer association than kitty [01:01:00] broccoli, kitty
napkin, kitty stereo speaker, right? Those are way less semantically
related, right? So what this is doing is a combination of those two,
types of searches, and then it is, it has this very simple algorithm
that weighs them.

And so the vector search is 0.7 weighed, meaning that if you run a
search for cat and then you find semantic matches that are close to cat,
that's going to factor in 70% of what the top hit ultimately is. But if
you say search for cat and there is a file that is literally called the
CAT file, that would return if you ran a keyword search, right?

And so let's say you say CAT and cats are mentioned all throughout all
the files, right? So 20, 30 different files are gonna pop up that have
cat in it, right? But only one of them is the master cat instructions.
The master cat instructions file is gonna be listed master cat
instruction files. Because that [01:02:00] word cat is literally in
the title of the file, it will then also pop up for the keyword match.

And because keywords matter for 0.3, in this larger, algorithm, 30% of
the search algorithm, that means that if you have 40 files with CAT in
it, but one of them is labeled CAT file, that one will then be pushed
over the edge and be the number one file that is returned in the search.
So that's a quick explanation of what a vector hybrid search would do.

Okay. So it goes through and it evaluates everything. The pipeline is
working well. Your chunks and beddings and search functions are all
producing relevant results. No action needed unless you want me to fine
tune, Nope. Classify this as done. Update your Pod MD and instructions
to note that we can now use [01:03:00] this as a fully functional
knowledge base, view the files and add some very basic information about
the client.

Create a tree. In the claw mb file as well. And what the, the tree idea
here is just like, look at what the files are that you have and create
some sort of map that, will be loaded into the context from the GetGo of
like, here's the type of information that we have. That was my
thinking.

Might not be necessary, but, depending on how you, how many files you
have and what you've added, it could be, potentially helpful for, the,
the agent to figure out, how, how it should be accessing things. 

 okay, so that's running for a
moment. So this will take a little bit of time to update and adjust, but
the big [01:04:00] picture here is that, we're more or less done. So
I'm gonna let this run, and it's done.

Okay. Big claim, my friend. Let's see. Run.

Wow. Okay. Do you wanna run a query? Do you want the ingestion pipeline?
Do you want calibration or something else? Entirely? What do you have in
mind? I want to run some queries. What information do you have

there? It [01:05:00] is. Yes. I need to know overtime policies from
the employee handbook. 

Wow. Okay. List the source and when it was, last modified and or
created.

No, I need to know where that information you write. It came from.

Wow. Okay. Cool. There we go.

It pulled the right information. Its retrieval score is a little bit
low. I think there are ways that this could be modified. [01:06:00]
For example, keywords could be added. It could strip keywords out and
then add keywords to a metadata. Column that does exist in Supabase, but
there wasn't much there.

So doing some form of metadata tagging could increase that. You may
wanna do, for example, if you have different, handbooks for different,
clients, you could create tags and you could tag the data, by client
name. So that would help, noticeably also, it says last modified here.
And it doesn't actually include the information about when this file
was created.

That's something else that I would look into and tweak and certainly
update so that that would be included as a part of the data that it
pulls. When you run a search like this, it may need to take one of the,
migration. Files that were created. 

These may need to be updated and modified and then run, by Claude, to
update, the database. The database and these migrations are, idempotent,
which means that, if you run them again, it will not corrupt or delete
or remove or alter [01:07:00] any of the data that's currently in the
database.

So it is safe to rerun these migrations. It should also have, an undo
link to it as well. So if the migration goes wrong, you will be able to
undo that migration. And again. You will not, lose any of the data in
the process. But again, whenever you're messing around with a database
and if the database is in production with the client already, you're
probably gonna want to create like, different environments for it, like
a testing and development environment, and then only push those changes
to the development environment when you feel comfortable with them.

 We've  created our own,
knowledge base in, well it took an hour, but it felt like there was a
lot of, explanations and sort of, detours to walk you through the
details. If we were just running this end to end without the tutorial,
what, 15, 15 minutes to get this set up, and process.

And, you know, if you were to, run this on hundreds of files, it is
built in such a way that it does one file at a time. So, it's pretty
good at tracking its progress. You can [01:08:00] either add on new
flags in the environment, variables to kind of go phase by phase, or
documents type or whatever you want, or just let it run.

And when it, seems to be running outta steam or compacting start a new
session, it'll see what files were already there. It'll have an
inventory of everything as you saw. It'll just pick up where it left
off and it'll continue, breaking those documents into pieces.
Excellent. So that is all. Thank you so much for watching and, good luck
with your knowledge bases.

Now you have the ability to build, a, a rag retrieval database and then
of course, connect it to Claude via a connector. Pretty exciting stuff.
And, from there there's all sorts of exciting things that you can do
with it. You could make, an MCP, out of it, for example. And then pass
that MCP to your client.

All they would need to do is add those environment variables. You can
even. Pre-create an environment, environment variable file for your
client. And as long as you're sharing that securely on something
that's [01:09:00] encrypted, end to end, like, I don't know, signal
or something else that's safe and secure online, I think things like
Bit Warden have the ability to do file sharing whatnot.

As long as it's encrypted end to end, you can just create that ENV file
for your client, add in the APIs on your end for Supabase or whatever
else is needed, pass it to them. All they need to do is put that
environment variable folder, file in the right folder. Or even just tell
Claude, I downloaded the ENV for this project.

Please add it where it needs to be added, and Claude will just find it
itself and add it on its own. So that's it. A lot of possibilities
here. A lot of ways this can go, a lot of things that you could do
either packaging this for your clients, making things for your clients,
or just using this to run your own consultancy.

There's a lot of value in this project. I have just a year ago charged
a client, I think it was a $25,000 project to do. Probably if I had had
this, it probably would've taken me a week to do it, total. So, that's
a [01:10:00] huge advantage for you outta the gate. So again, thanks
watching, enjoy and good luck.
