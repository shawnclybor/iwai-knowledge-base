Build It Together: Knowledge Bases (Core)

[00:00:00]

**Shawn Clybor:** Hello everyone and welcome to the Core workflow for
innovating with AI's, build It Together, series on knowledge bases.
We're really excited to share this one with you, so let's get started.

First, let's quickly review the Build It Together framework. Build it
together as a series is designed to provide for you a valuable client
deliverable at every level of tech skill and complexity for all the
different personas in our program. This initial core workflow is for all
personas in the Innovating with AI consultancy project.

And it is ideal, in particular for pioneers, producers and investors.
What we are going to build today will be a valuable solution that
[00:01:00] everyone, regardless of their tech skill level, can deliver
to their client.

The lesson today will really be the platform from which we are going to
build. Both the power up and the advanced custom solutions, over the
course of these lessons. So just to quickly recap, what's a knowledge
base? Knowledge bases are sources of truth for organizational memory.

AI is responsible for organizing the documents, processing all of the
user queries, and then delivering precise answers with the information
that it retrieves for you. So you can think of it as sort of like a
personalized research assistant who digs through materials that you
specify, reviews them with processes that you, offer, and then returns
answers in a specific format to match your expectations.

So a knowledge base, really has three pieces. If we're [00:02:00]
talking about development, the first is processing. So this is really
the foundation of building a knowledge base. This is the phase in which
you have to convert all of the messy information that you are going to,
unearth and dig up, from company documents, FAQs, and other forms of
data.

Including, for example, transcripts that you might have for discovery
calls and focus groups, written, surveys, forms, things of that matter,
or emails, PDFs, anything else you could imagine. All of that would be
taken and then during this processing phase, cleaned up, standardized,
tagged with metadata, and then indexed .

The next stage of a knowledge base is the retrieval piece. This is
really the intelligence part, so this is where we're taking the
knowledge base that we've created, and we're now connecting it to an
AI model like Chachi, PT four oh or [00:03:00] CLOs, Opus 4.6 or
Sonnet 4.6. And then the LLM is.

Searching through the knowledge base that we've created to find
relevant information and then returns it to the user. Once AI finds the
information that it thinks you need, it will then generate accurate,
contextual answers and even provide citations from your knowledge base.

So that's really the three part, flow here. And what we're gonna be
working on today in the core lesson is very heavily this initial piece
of document processing. Now, that's not to say that AI retrieval and
answer generation are not a part of what we're doing. But, we're
really gonna rely on one platform to do those pieces for us.

So let's talk a little bit about our hypothetical case study. We are
going to do just one organization across the three lessons, and, we're
going to grow and evolve our scope with them over time. From an easy
project to deliver that would be lower end in terms of [00:04:00]
budget, and then grow with them, scale with them into a higher end, more
expensive custom solution, by the end.

Okay, so True Point HR Solutions , a regional HR consulting and
outsourced HR services firm that is based in Charlotte, North Carolina.

 so founded in 2014, true Point has 35
employees working hybrid out of one office, off of one table, it seems,
and serving 120 small business clients across industries that include
restaurants, construction, medical, dental practices, and tech startups.
Their revenue is around $3 million annually.

So the services they provide include outsourced HR management, employee
handbook development, compliance audits, benefits administration,
payroll support, workplace investigations management, coaching, and
recruiting support. But from these initial documents and our initial
sales [00:05:00] calls, we were able to determine. Some important pain
points here that we're hoping our chat bot that we will be building or
our knowledge base connected to Claude, will be able to resolve.

The first is, the tribal knowledge bottleneck. Lisa, the co-founder,
fields 12 to 15 internal questions. Per day from members of her team and
loses about 10 billable hours per week just responding to these
questions. How did we handle X for client Y? What do we do when X
happens? What do you do? And Y happens.

She's really the ultimate source of truth in the organization, which
means that anytime somebody needs to know something before they can move
forward, they have to run it by her. So everything is sort of like that
wheel and spoke. Structure where all of the various spokes of the
organization have to run through the hub.

A new consultant can take up to six months to work independently.
Figuring out what it is they need to do and how they need to do it, that
is a really lengthy onboarding period and the [00:06:00] organization
would really like to see that dropped, to three to four months if, if
possible.

Next is template chaos and compliance risk. As you will see from the map
that we have built of the, organization's, Google Workspace. They have
over 400 templates in their Google Drive, with duplicate versions,
inconsistent state specific labeling, and no version control. So a big
part of what we will need to use AI for is to sort through all of that
and figure out what documents are the most important.

Next pain point is that, the organization relies, heavily on consultants
who end up having to play detective on cross coverage. So, for example,
if someone has to step in and cover, a colleague's client.

And they'll still end up having to call Lisa just to verify these
things and ask questions. So this is just yet another one of those areas
where, so many things end up flowing to [00:07:00] her, contributing
to that bottleneck We mentioned at the beginning.

The consultants spend roughly 20% of their billable time answering the
same recurring HR questions across clients over and over again. And so
you can see that, if they're spending 20% of their billable time
answering recurring questions, if we were to reduce that just by 10%.
That now for all of the consultants in the organization, that is going
to be a savings, an ROI of 10% off of all of their billable hours.

Which for this initial project, could easily pay for itself within just
maybe even a month or two. So, that's really important to consider and
to frame that ROI for the client.

So let's talk a little bit about our tech stack Today. I am going to
be, using Claude Projects for this build. And that's it. It is really
what we're doing here is we're prioritizing simplicity. And
accessibility with minimal technical [00:08:00] complexity. That's
really the focus. So this is going to be a build it and run it type
situation.

 so the technical scope here. Claude platform
with structured knowledge based files.

We're going to have custom system prompts, and we're gonna be using,
well in Claude, it calls them connectors, but what they really are, are
MCP servers. So just for the sake of ease, I'm gonna refer to them in
this lesson as MCP connectors, sometimes maybe just connectors. But if
you hear me say MCP or connector in the context of this lesson, I'm
really talking about the same thing.

So, we're gonna be using, I have three here, GitHub, Google Drive, and
Docking. We'll see if we end up using all three of those. Certainly we
will use those in the power Up lesson. But let's see how we, let's see
how we proceed with, with the lesson. I know Google Drive. Absolutely.
We'll be important.

I think that this project is ideal for, bootstrappers pioneers, people
in the program without a lot of technical knowledge, because it
leverages [00:09:00] Claude's native project architecture. So that
means there's no code set up. It's just a few direct file uploads that
you need to do, and there is already built in conversation memory for
all of the context retention, meaning that across the project and the
con conversations you have, that memory is automatically retained by
Claude itself.

So it's really beginner friendly. It's going to handle predictable
knowledge queries. It's going to avoid custom development work. It's
going to work with existing documents, and it's going to support
template, template based workflows.

So a basic Claude project implementation like this is going to cost
somewhere between 3000 to $7,500. The pricing really is going to depend
on the length and the amount of discovery time, the amount of content
development that you need to do, the amount of CPS or connectors that
you need to integrate into the project, and then the amount of training
that you need to provide to the [00:10:00] teams.

That is to say that a fair amount of this price here is for all of the
things around the technology solution, maybe half of this total project
budget. All in, right? So it's all these other pieces that are really
going to impact the price.

And depending on how much you need to do for these things, you're going
to see that fluctuation, like 3000 assumes that, there's very little
discovery. The client has all the documents ready, they send them your
way. You're using just the basic MCPS like Google Drive and the
training session is like maybe one hour session.

So let's talk a little bit more specific about what we're building. So
we're gonna build Custom Claw project and this tailored Claude project
is going to have its own custom instructions and its own connectors.

To parse out discovery data and generate knowledge base files. It's
gonna do both and we'll see how that'll work in a bit. Then we are
also going to build structured knowledge base files that will be the
outcome of this initial custom cloud project that we will be
[00:11:00] assembling. The project that we are building will be used
to generate the knowledge base file.

These are going to be organized markdown files, meaning that they are
text files, but they have the ending md, and that ending MD means that
all of the syntactic characters. Are visible. So if you have headings
and subheadings and paragraphs and bolding, rather than those visually
being represented by like, oh, the heading is larger and it's a
different font, you're just going to see like, a hashtag and then the
name and that's gonna, the hashtag designates.

This is a heading and two hashtags, designate subheading, and three
hashtags means sub subheading. And having two stars around words means
that they need to be bold print. So basically all of the syntax and
formatting that you're used to in a Word document, A markdown file just
visualizes that syntax. So it's easier to translate when you're
passing files between different systems and processes.

And AI is scanning it. We don't have to worry about the formatting,
[00:12:00] generating unnecessary characters or wasting a bunch of
space.  So it's
going to be, marked down. And they are going to contain processed
versions of our discovery transcripts, our client notes, and other forms
of documentation that we provide for accurate AI retrieval.

And the third stage here, the true point HR solution, will be the
application of the knowledge from steps one and step two. That is to say
the custom claw project that we'll build together and the structured
knowledge base files that we generate, we're going to use the knowledge
that we've gained from doing those first two steps.

To set up a functional knowledge base for true point solutions that will
also be a clawed project. So we're basically going to just map what we
did to build our own internal tool. We're going to map that learning
onto putting together a final deliverable for the client. And the idea
would be that you would then schedule a call.

Everyone who could [00:13:00] attend, who would use this tool will be
on the call. You can certainly record it for those who can't make it.
And then you will provide them with a file or a folder with all the
files in it, and you will walk them step by step through how they set
this Quad project up on their own version of Claude AI or Claude
Desktop.

So it's sort of like you don't set it up for them, you're gonna walk
them through the setup, but the setup will be extremely simple. It'll
be just uploading seven or eight files and pasting one page of
instructions into the instructions, and that's it. You may need to walk
them through setting up a connector as well.

So it's a very simple thing. There are no APIs, there are no keys. No
ENV files, nothing like that at all. So, very straightforward. So if we
were to do this project, IRL, as they say, I envision this project
taking about a month, give or take. The first week would be discovery
definition, doing stakeholder interviews, identifying the questions and
pain [00:14:00] points, mapping where the knowledge currently lives,
defining success metrics for the project, and, fleshing out the scope.

The second stage would be the content and, content audit and source
mapping piece, which you would, have to, inventory all of their existing
documents, assess the quality of those documents using the keep. Update
archive, delete system, 

So we're going to assess that quality. We're going to identify gaps,
and then we're gonna return that gap analysis to the client and say,
Hey, you know, here are some areas where I've identified gaps in, in
what we wanna put in the knowledge base.

Can we do a quick follow up call to talk about these? Right. And then of
course we need to determine what's going to become a structured
knowledge base file versus a template or just reference material as
needed, or, not needed at all and not a part of the project. So the
actual architecture of the knowledge base should take about a week.

You're going to design the project structure, organize the knowledge
based [00:15:00] files by domain, create templates for recurring
tasks, define system prompts and skills, and select your MCP connectors.
Now if you are using Claude Cowork or even Claude Code or some sort of
equivalent, like I guess perhaps open Claw, some sort of agent system
that has, terminal access and file and read and write access on your
computer, this part of the project could actually take you a day, maybe,
maybe two days at the absolute most that's.

It took me maybe a few hours to build this whole project, all in. So it
goes pretty quickly if you're using, AI tools to set it up. The system
prompt . That could take some time and some tweaking and adjusting,
configuring the connectors, and then packaging all of that together as a
ready to install cloud project one week.

I think that's a very conservative estimate. You could probably have
this done in a couple of days. Then we have a week for testing and
refinement. That would be testing the queries about [00:16:00]
knowledge based files, validating template outputs, verifying the MCP
connections, stress testing, edge cases, refining the system, prompt
back and forth with the client, whatever the case may be.

Again, I think a week is very robust for this. And then finally, the
live install in the training session. One session would be sufficient.
You walk the client through the project installation together on a live
call. You should record it.

You should generate SOPs from the transcript. And you should also
establish content update protocols just as a part of your service
offering. I think it would be great to say this is how you update and
maintain this, but of course, this is also an opportunity for an
ongoing, retainer on your part.

If you were the one responsible for maintaining and updating these
systems, as needed, and then you could pass them the files and then they
could update the files on their end. So let's talk a little bit about
operational costs. So I think that this is a very low cost project. A
[00:17:00] license for Claude Pro is $20 per user per month, and this
is required to use Claude Projects with custom system prompts and
knowledge base vials.

 And even if
it were, you wouldn't want to use the free tier with a client or client
information. Because when you're using the free tier, anthropic is
allowed to use your data for training, and that could potentially be, a
compliance or, if anything, ethical issue taking these files and using
them, your client's files, adding them to Claude.

Okay, so make sure you have the Claude Pro account. Even if you need to
add it for this particular, build. You can cancel it when you're done.
It's $20 to to run it. If they were all using Claude team licenses,
you could add this project and then they could all work on it together
in a single place. This also gives you higher usage limits and priority
access. That's $30 per user per month. And then finally the MCP
connectors, those are free.

So there's no real added cost there. Do keep in mind also that this
assumes that you are working with [00:18:00] some kind of a Google
Workspace account also that would be necessary, to do this build,
exactly in the way that I, I do it. That said, this is mostly a platform
agnostic, lesson. So I'm going to be building it in Claude Projects,
but it could also be built in chat GPT and it could also be built as a
gem and Gemini.

And so this chart here just sort of walks through, depending on which
one of these three platforms you're using. What you can expect in terms
of similarities and differences in terms of their architecture structure
and setup. So, I provide, for example, like what are the various caps on
knowledge files across the three platforms.

 How do they handle connectors and
integrations differently?  And I think the major
thing that I really wanna highlight here on the call, are the connectors
and the integrations.

So if you're using Claude Projects, connectors are native and there are
dozens of them at this point, for most major platforms. [00:19:00] Out
of the box, two clicks, you can set it up and connect it. And it also
supports just the MCP protocol if you want to build your own custom
connect.

Most of the time it works, as long as it's not too different from the
actual MCP itself, it can just modify the code, set it up, run it,
you're good to go. That's great. You can do that also with chat GPT.
So in this regard, the functionality between the two is quite similar,
but where it's really different is Google.

Now Google allows for Native workspace integration, meaning that it
integrates with Drive Doc Sheets, Gmail calendar, and Notebook lm
notably, that also is an MCP you can set up in Gemini that you cannot
set up in other platforms. That's a big value added of Google because
you could use Notebook LM as your knowledge base for this project.

But it doesn't have MCP support and there are no third party
connectors. So if you're looking to move outside of the Google
ecosystem, I would really strongly recommend not using Google.
[00:20:00] If you are using Google, I would strongly recommend setting
it up with Notebook LM as your knowledge base, and then add the files
that we're generating today.

I think those are really the key important differences here that I
wanted to highlight for you and, allow you to kind of make your choice
in how you wanna proceed. Of course, we always recommend that if you're
testing this out for the first time, you want to eliminate the, the
potential for, errors, by following what we do as closely as possible.

Because if you're doing things differently and then you get an error,
it can be very hard to figure out. From a, troubleshooting perspective,
well, what's causing the error? Is the error because of something in my
instructions, or is it because the way you are doing it is different and
there's a difference that we haven't accounted for and you haven't
accounted for, and that's creating the problem?

Just to eliminate all of those variables or at least as many variables
as possible, the best thing to do is to really follow the lesson as
designed initially. And then once you get it up and running and you know
it [00:21:00] works, then you can modify it and change it and try it
different ways. 

So without further ado. Let's, let's take a look at some of the
project files.

Okay, so the first step to this project is for you to locate and click
on the URL to the GitHub repository that we've put together, that will
eventually have all three lessons for the Build It Together series on
knowledge bases. And one of the nice things about GitHub and the
underlying architecture of Gits, is that it allows you to, track changes
to files and folders over time, in a way where every change is very
strictly version controlled.

And add notes to the various commits that you make. Explaining what
exactly changed in the files that did change and the folders that did
change. So this is [00:22:00] really great for developers. If they hit
some sort of bug or error, they can back up to a point at which the code
is safe.

You can also branch off of a a git line. So if you have a main
development line and you wanna add something new, but you're not sure
it'll work, you can. Branch off of that main line and play around on
the branch. If it works, you can merge it back into the original branch
and if it doesn't work, it's just on a branch, you can go back to the
main.

So GitHub is really the gold standard right now for development. It is
where, if you are working in AI and you're picking up things related to
Claude code like plugins or agents or skills or anything else, the
likelihood is very high that you're gonna be finding it here on GitHub.

So, for now what we have is just a very simple setup. You're going to
see three files here. One will be labeled get Ignore, and this file just
tells, the larger package that there are certain files and folders that
it should not [00:23:00] version control. You don't want upload that
to some repository to share with other people. So you would add that
file. It's usually a do ENV or DOT environment file. So you can add
that ENV file to your GI ignore, and then it won't get committed.

The one you're gonna want to probably take a look at first is the Read
Me, and you can click on that and it will open it up. And so this just
is going to give you an overview of everything here that's in the
repository or repo. Breaking down here are where you're going to find
the lessons in each of these folders.

Currently, only intro and core are included by the end of the project.
You have the repo structure. This is just a tree map of how everything
is organized in the repo. This will build out. So if you're looking at
this lesson, this repo structure will look differently because we're
going to be updating this lesson with the power up and advanced lesson
that I haven't filmed yet.

 similarly, we
have this explanation of lesson number one here. This will include
[00:24:00] lesson two and lesson three by the time we finish. This
just gives a quick overview of what I explained in the introduction to
the lesson, and it includes a workflow for how we are going to process
the raw materials, using the tools that are in this lesson.

A lot of this information is here if you choose to access this repo.
Through an LLM or paste this link into, let's say, Chachi pt or Claude
or Gemini, and say, explain what this is to me. The first thing it's
going to do is it's going to access this Read me file. It's going to
pull all of that into its context memory, and then it's going to access
all the individual files to come up with a synthesis of what this
project is and how it functions.

So that's kind of the, the, the logic behind the Read Me file. All
right, so for us to use this file, what we are gonna want to do is go up
to the code button right here. You're going to click on that, and I
want you to click [00:25:00] download zip. That is going to download
this entire project folder into your downloads folder, and you'll need
to unzip this file then as well.

All right, so let's click on this one right here, core. So you can see
in the core lesson we have four main folders. The first one is builder
tools, then raw client files, sample files, and template. The sample
files are really here for your edification. They are here for you to see
that when something gets done, this is what the file should look like.

So here we have a sample Google Drive inventory. This is what it would
look like after you map out an inventory their Google Drive folder,
assuming of course that your client is working in Google Drive. So this
is our map of their Google Drive folder. Then we have here is the
content audit.

So we're going to be running content audits and that is going to go
through and look at all of [00:26:00] the content that's in Google
Drive and, map out what needs to be kept, what needs to be updated, what
needs to be archived, and what needs to be deleted. Now, I would say
that there is gonna be some human involvement in this stage of things.

So again, keep in mind this is not fully automated. We'll talk more
about that later. So let's go back. We also have, a test gap list. Test
recurring questions, a test storage inventory, and a couple of test
transcripts that we are going to process. These are the processed
versions of the transcripts, not raw.

So I'm including all of this in here so that as you are building, you
can look at these and see exactly what they should look like from an
ideal standpoint. And so that way, you know, if everything is working
correctly in the way that it should or if you need to troubleshoot with
an LLM. You can pass these files along and say, well, what I'm doing
should look like this, but it doesn't.

So that's pretty much all sample files is, so most of what we're gonna
be working with today is [00:27:00] builder tools, raw client files
and templates. So the templates are the templates that we are going to
use to process all of the data during the discovery that will result in
us creating.

Knowledge base files. So these are the templates that will get us to the
knowledge base. The raw client files are the input. These are the files
coming in that we would expect to have from a discovery. And so what
that is right here are two transcripts. One initial interview. The
second is a follow up interview.

And then we have some sample files. From the client's Google Drive that
just give a sense of like, okay, this is the format of our policies.
This is the format of the checklists that they build. Here's a format
of the handbooks that they design. Here is a, template of the, their
offer [00:28:00] letters.

Next we have the builder tools, and these are really the important ones.
These are the files that we are mostly going to be working with today
and setting up in CLO projects momentarily. We have CLO MD D, dupe
instructions, formatting Rules, instructions, and MCP connector setup.
So instead of going through each one of those individually here, I think
it would be a good time to move over to CLO projects.

Okay, so here we are over in Claude, and I am using, Claude Desktop. I
recommend that you would do the same for this project. I imagine this
would work in Claude. On the browser just fine. But, oftentimes when you
are working in, development, you really wanna try and eliminate as many
variables as you can as possible.

So if something does go wrong, you know, it more likely what the cause
could be, right. It may [00:29:00] sound crazy that you would run into
some kind of error using Claude on your browser that you wouldn't run
into using the Claude desktop version, but it has happened. And so,
again, just keeping those variations as limited as possible in every way
that you can, really is a best practice.

When you get to the main screen for Claude, what you're gonna wanna do
first is just, you can click on the sidebar if you don't already have
it open, click on projects, and this is going to open up your main
projects window.

And you want to click new project. Okay, so we're gonna name this.
Let's name this BIT core

test, BIT kb core test. What are you trying to achieve? Builder tools to
[00:30:00] process client data and build knowledge bases. Sounds good
to me. And we'll click Create project. Okay. This is now the main
window for cloud project.

There are a few pieces to it. The first is the main project window here.
This is the same as any LLM that you would use. You can choose the model
that you want to run. You can click the plus to add things, you can. Set
a research mode.

You can add the connectors here and then you can add files or photos.
And then obviously this sends the chat. You can also star chats. You can
archive chats, you can edit details here on the top.

So as you begin having chats, there'll be a log of the chats that's
stored here. And for testing purposes, I would really recommend,
deleting these as you go. They can be used as context memory in the
project. So if you're trying to get something to work [00:31:00] and
the only reason it does work is because you explained it here, you might
be biasing.

The way that the LLM functions, if that context weren't there, right.
So I find until everything is set up and running exactly how I want it,
when I run a test, I delete that chat afterwards until I'm a hundred
percent happy with the performance of the project. And then I allow the
chats to begin populating and they can be used as context history.

Memory is not something that you can control. Memory, is this is where
Claude will store specific project memories that it thinks are relevant
and important and to remember and will then load them into its context
every time you set, a fresh chat.

Once it begins generating details, you can prompt it to delete things
and change things and update things. Like, for example, if it gets a
client's name wrong, you can go in and edit it and change it, whatever.
Instructions. This is really important.

Files also really important and maybe self-explanatory. This is where we
add [00:32:00] files that are a part of the project. And the last
piece that I just wanna point out, we won't be doing it today, but I do
think it's pretty amazing. You can also click this to open up Claude
Cowork, which is sort of like Claude Code for non coders and.

It will take this project and its context in all of its files and it'll
move it into cowork where you can then begin working with an agentic
system that has access to your terminal, can control your desktop, can
open browsers, and do, you know, all sorts of other, more advanced tasks
in terms of its, ability to, orchestrate workflows and, and write and,
and files and generate code and so on.

 So the first thing that we
want to do here is, go to those files that we downloaded from GitHub,
and we're gonna wanna add those into the project. So click on assets,
click on core.

And then click on Builder Tools, and this is where we're gonna start.
[00:33:00] So the first thing that you want to do is take this CLA MD
file. I just, I'm on a Mac, so I just preview the file by hitting space
bar. Then I hit command A to select all. Then I hit command C to copy
all. Then I hit command tab to go back to.

I click on instructions, and then I hit Command V and I paste it. And
these instructions are going to act as the core instructions for the
project that will be injected into every prompt you write. In this
project moving forward. So we click save here 

 Automatically, it's a knowledge based builder, so it
takes those instructions and instantaneously, you have now a functioning
agent rather than a raw LLM. So let's go back to the project. I'm
gonna do that by clicking right here.

Let's take a look at those instructions and walk through those
[00:34:00] together. So I begin with the, the role, and I say you are
a knowledge base architect. Your job is to help a consultant transform
raw discovery materials into a clean, structured markdown knowledge base
that will power a separate client facing Claude project.

So that's the summary. The very next section I include my methodology
and I note in all caps, always follow these instructions. LLMs can be a
little stubborn sometimes in terms of their behavior. And so anything
that you can do to really, strong arm them into behaving, is ideal so
that, you know, hence the, all caps and I give it my, my methodology.

And because this is not a coding project, the methodology is pretty
simple and it's more organized towards how Claude behaves rather than
its coding conventions and structures and things of that sort. So,
number one, keep answers direct. Number two, break down multi-step
processes into single steps at a time.

This [00:35:00] guarantees that the project you're building is going
to be more interactive and dynamic like, some kind of coach or
assistant. Rather than generating a five page answer of 25 steps, it's
going to say, cool. Let's do step one. Give you step one. When you're
ready, let me know. We'll move on to step two.

I find this type of arrangement to just be so much less, less of a
cognitive overload. To be honest, because oftentimes it'll give me 25
steps and I get to step three and something goes sideways, and then the
other 22 steps are just useless because we've gone down a different
path.

So this just kind of keeps it one step at a time. Kiss, that's an
acronym. It's short for Keep it Simple. Stupid. This is one of my
favorite things to tell LLMs, and they know what it means. You don't
have to say, keep it simple, stupid, just literally write, kiss in all
caps. And it's like a trigger word.

It like instantly panics and it's like, you're right, I overthought
this, and then it'll just regenerate what it did for you at like one
third, the amount of, [00:36:00] text that it did initially. Now I
just tell it from the outset, both in my regular Claude and here and
everywhere with an LLM, that this is a part of the methodology.

One, it is just a waste of tokens to have all of that extra slop in
everything that it generates, and two. It is slop. It's just too much,
right? And, everybody kind of talks and jokes about that. So, just right
out of the gate, I wanted to know, keep it simple, stupid.

Ya gni, that's a weird one. That means you ain't gonna need it. You
ain't gonna need it. And this is about, I think the origins of this are
for features. Like if you're, you know, I'm sure you've done this
with ai. When you're working on something, you have a project idea and
AI is like, I love that idea.

Here are five more things that we can do that are gonna be super awesome
to add to your idea. And you know, it's exciting when you're in that
creative mindset and you've got this partner bouncing ideas off of you
to be like, yeah, let's do it.

Let's do it, let's do it. And things will just balloon out of
[00:37:00] control and, ultimately end up breaking and falling apart
because the LLM promised you a bunch of things that it couldn't
necessarily deliver or didn't know how to deliver. Her So Yame just
keeps it, keeps it on the straight and narrow.

So the next piece is MCP tool usage. The connectors, and I tell it
Google connector use when working with Google Docs or Sheets and that's
it. Now, of course, if we were using more cps, I would have more here
for every MCP that I use.

I always add a line in the core instructions saying exactly when the LLM
should use it, because just, you know, just because it has the connector
doesn't mean that it'll know inherently when it should be used. So
this is a really great way for you to say. At the beginning of every
prompt, here are five cps you have, here's when you use them.

Here's my prompt. And then it will say, cool, the user wants me to do
X. I have these tools to do it. Which of them should [00:38:00] I use,
if any? And then it'll move on from there. So again, extremely helpful
to have. Next section is how this project works. This project contains
two types of files, builder tools, and deliverables.

The builder tools are the instructions and templates that govern how you
process raw materials. The deliverables are the structured knowledge
base files that you generate. These will ultimately be exported and
installed in the client's clog project. The client's raw discovery
materials, transcript sample documents are not uploaded to this project.

They live in the client's cloud storage and are accessed through a
connector. This keeps the builder project lightweight and reusable only
the tools live here. During processing, you'll generate intermediate
outputs, inventories, content audits, question lists, gap analyses from
those raw materials. These are produced in conversation using the
templates below, not pre-existing files.

This is a big mistake that people [00:39:00] make when they're
setting up custom GPT or custom projects, is that they make these
initial instructions like 500 lines long with all of the things that
they want it to do. These types of systems work many times better.

If. You leave this introductory file as simple as possible with big,
high level architectural stuff. Like here is the overview of everything,
and this is where you find stuff, and then shunt the instructions off to
a knowledge base file where it can call them into its context memory as
needed. It just keeps everything on task.

It keeps it way more accurate. And it doesn't drift off as the, initial
prompt starts getting lost in the, the larger, context that you begin
building. There are also formatting rules. So this is when you are
generating or reviewing a knowledge base file. Well this is when Claude,
I don't mean you personally listener, but rather when Claude is
formatting or reviewing a knowledge base file, dedupe [00:40:00]
instructions use when encountering conflicting information across
sources.

Multiple sources that appear to be the same or assigning primary home
topics during assessment. This is really important for a knowledge base,
what do you do when you have multiple sources that conflict or different
versions or things have been updated or people have made changes?

And these de-dupe instructions that I include in the project. These can
be really helpful for helping the LLM make decisions about what to do.
And then finally, the MCP connector set up. This is there strictly to
help provide you with guidance as you are trying to set up these MCP
connectors, if that proves to be a challenge for you.

It's just additional instructions to help you set this up without my
assistance. It then lists all these templates. These are all the
templates that are also going to be attached, and then it ends here with
the output rules and the interaction style, right? This is how I want
you to behave.

Okay, so now we 

 have our instructions. Now we want to add [00:41:00]
those files. So we're gonna click upload from device, and we're going
to go to Knowledge Base Main. We're gonna go to assets. Core builder
tools. Let's add in. First we'll add in instructions. Then we will add
in formatting rules, de-dupe instructions, and MCP connector setup.

Now, that's not everything.

Let's go back. I. And now let's go over templates. We're gonna add in
content audit,

gap list, recurring questions, storage, inventory I,

And here's the [00:42:00] exciting part. All of the technical work,
except for one thing is done. The only thing we have left to do is to
set up the connector. So to do that, we're gonna click plus here you
can see I'm already actually connected, so I am going to go to manage
connectors. I'm gonna disconnect Google Drive and I'll reconnect it.

So when you are on this main screen and you click the plus and you go to
connectors, go to manage connectors, or if you scroll all the way down,
you might just see drive search. You can click connect. That will open
up over here. It pulled up this window. 

 So it's just going to di default pull you to the sign in with
Google. Prompt login. Login prompt. So pick an account. I have too many.
They're signing you back in.

[00:43:00] Yeah. Say connect or continue. Continue.

And that's it.

We should now be connected. So let's see. Test your Google Drive
connection.

There we go. Let's test. Overall, what can you do?

I help consultants transform raw client discovery materials into
structured knowledge base files for a client facing project. Here's
what I [00:44:00] can help with today. Project set up, verify storage
access and get connected to client files. New client, build a knowledge
base from scratch existing client. Pick up where you left off.

Okay, so there are two more connectors that I wanted to talk to you
about that are entirely optional that you may want to use and will
definitely speed this process up, but are not required. So the first is
the desktop commander. The desktop Commander is extremely helpful. It
gives Claude access to your desktop.

It allows it to run commands from your terminal. It allows it to open
files, find files, save files to different folders and directories on
the desktop, without having,  to give it permission
every time or, do it manually. So I would really recommend that you find
Desktop Commander in the connectors and you enable it and [00:45:00]
make sure that when it comes to the writing and the reading tools,
especially for the writing tools, you're gonna want to set those two
um, a.

Uh, either ask permission or block. The only two that I have,
automatically allowed is starting terminal processes and writing files.
Even that I probably shouldn't do. And again, I mean, I think it's
just really better to be safe rather than, sorry. Having that ability to
review what Claude is proposing to do on your computer before it does it
is really important.

And worth having that time  to stop it from doing
something that could potentially. Crash  your entire
system, especially if you're not very familiar or comfortable with the
technical, side of how, computers, function. So, the desktop commander,
very easy. Two clicks to, enable it and run it.

And then it will have access to your, your Mac if you're using Windows.
There's also. A desktop extension for the, windows, that allows it to
operate with Windows os. So you can definitely use that as well. And you
can see just [00:46:00] how popular that is. That's, there's
actually almost 10 times more people using the Windows MCP than there
are people using the Mac, desktop Commander, which is pretty amazing.

The second, connector that I would really recommend that you set up for
this process is, Zapier. Actually Zapier. Zapier is, really amazing on,
Claude. Let's see where you, let me go back to find it. Yeah, there it
is right there. And again, this is just as easy to set up as Google
Drive, where it really just takes you over to the browser.

Claude, as long as you already have a Zapier account created, as far as
I know, it can be a free account. It's no big deal. And it comes
pre-populated with automations for reading and writing that are all
connected to Google.

And this just makes the process of interacting with Google Drive and
just Google as a whole so much easier. Google does not offer right
[00:47:00] functionality with the Google Drive tool, the connector
that we already set up. That connector is excellent if you are
evaluating a client's drive structure, for this process.

But if you actually want to write files or read, beyond just reading
files, if you wanna write files, you can't do it with the Google
connector. So having the Zapier connector and having that with all of
these. Extra right functions for Google Drive will mean that you can
manage and store these projects entirely on Google while you are working
with the files.

And so that could be a real, advantage, and could be very attractive to
you. I am going to stick to operating on my desktop, and I will just
point, the, agent over to my downloads folder where I have the. Course
files all already set up. So let's, let's run [00:48:00] this.

 So let's do one first, even though we're, we're set
up, it can review and make sure everything is good.

 Let's see if
it runs a search. If it can find it. Yeah. There it is. Okay. Cool. Yep.
New client. New client.

Oh, I forgot to answer question two. Where do you want local files?
Where do you want the files generated? So we're gonna put that on the
local computer. There we go. Local in downloads

UI

knowledge base main. Assets [00:49:00] core and yeah, let's leave it
at that. Let's see.

Okay. And it's automatically taking the initiative to go through that
true point folder and see what it can find.

Okay. It just gave us a quick overview.

Yep. Let's start.

 I'm going to pause this and give it a
minute 'cause it will take a little while for it to parse through it
all and generate the files. Okay, so it has finished step two A. It
processed both of the vials. [00:50:00] It flagged some gaps,

and it is ready to move to step two B storage inventory. 

Okay, good. Now it is pulling up our template that we have saved in the
project, and it is now generating that file. Excellent. And let's, let
this run for a minute and we'll check in when it's done.

Okay, next step done. 

 It's giving the top level structure and you know, the
sample file was not organized like this, so, this is really excellent.
Here are all the template folders.

And then on the bottom it's got some summary statistics and auditor
notes. So this looks really good. 

Next step please.[00:51:00]

So it's reviewing the sample client files. Now, of course, this is a
part of the process where, you may, have many more files than the few
files that I included. In my content audit, right? I have here in this
folder, you know, just like six files and they're all marked down. So
the files that you are using for your clients could end up being, there
could be a lot more than that.

And this process could take time. It could be, a separate chat that you
have to run. You may even need to extract data out of PDFs. But the nice
thing about running it as a project is that everything is kind of
connected to this main folder, and [00:52:00] you can always replicate
this architecture rather than having it be like your main content audit
project.

You could create a specific content project for a specific client, and
then each chat could just be a different piece of this process. It
doesn't need to all be in one, one master prompt like I'm doing right
now. Okay, so let's let this also run. We can see that it's generating
its audit of the content that we provided it already.

Okay. Content audit completed. There it is.

Excellent. Now I just want to make sure there, it's not, hallucinating
here. So, walk me through how and where you found all this [00:53:00]
information.

The transcripts, the primary driver, the template, chaos Descript. Et
cetera. The storage inventory gave me the folder structure, file names,
and the auditor's own flags. The four sample documents confirmed which
templates were actually used in active use and surface details. The
transcript didn't cover.

The restaurant handbook showed the tip pooling section needed, DOL,
verification,  et cetera. DUP logic kicked in a few times.
For example, the transcript said the NC Handbook. And client templates
was wrong and the inventory confirmed. The correct version was in HR
templates 2023. I used the end interview over the folder name because
Marcus was explicit about which folder to trust, which overrides
document naming.

Okay, so it is now pivoting. It says, towards generating, some recurring
questions. Now, this document here that it's putting together, this is
compiled from all of the materials that we've used, [00:54:00] and it
represents the questions that are asked most frequently, and this most
likely is also coming from the transcript.

We can verify that when it's done. Let's, wait for a second to finish
up.

Okay, here we have the recurring questions. This all looks great,

so it is now boiling down the most important questions that a knowledge
base can answer to keep. True point running with, less back and forth,
with Lisa about their policies and procedures. So this is looking really
good. It's really shaping up. Let's move on to that gap [00:55:00]
list.

Okay, so it has finished up and it has identified eight gaps of which it
believes that five would be high impact, and it has generated a document
that now outlines each of these gaps. Now, at this point in the process,
this would be the type of file that would be, excellent to, bring to the
client and talk through.

We, could even envision that from this gap analysis. You may record
[00:56:00] a follow-up interview with the client, which you could then
process in the system, and then review the results of the process
transcript to this gap list to make sure that you have, filled all the
gaps, and if anything else is left or outstanding, you could quickly
circle back one more time.

So for now though, let's just move forward and say yes, next step. And
it really has been amazing, like it is just walking us through this
process piece by piece and really leading us, where we need to go,
 I think this is just a really great use of a clawed project,
creating this interactive, dynamic system that, becomes more of an
assistant and a partner with you in a process rather than just this
quick, question answer, back and forth.

So it's got its source assessment that it's doing great. [00:57:00]
And now it's asking a couple of follow-up questions before I approve.
 move forward.

Okay, so it is humming along, but it has started to generate some of the
files. So it seems like, it's the moment of truth. Let's take a
[00:58:00] look and see what we've got. So this is the knowledge
based file for the template selection guide. And right out of the gate,
I can see this will probably need a little bit of adjustment.

What's important here is wow. Use this file to identify the correct
current template for any client engagement.

Do not search the drive for templates. The drive contains multiple
outdated and deprecated versions that will surface and search results.
Always use the canonical locations listed here.

 And then it maps out exactly where things come from. It's even
listing source sources here, which is also something  you may
want to delete depending on the use case and the client, but certainly
as you are the human in the loop, reviewing all of this and making sure
that everything is accurate and not hallucinated, having those sources
and links there is really important.

 This looks excellent. There is still
work here that would need to be done before this would be client ready,
but given that in about an hour, we just [00:59:00] put together not
only that document, but we're currently at, four out of seven different
knowledge base files. This one over here on state compliance, state
compliance reference for North Carolina, South Carolina, Virginia, and
Georgia.

Some update needed, some content gaps flagged, but this looks great. And
you know, we want those content. Gaps flagged rather than the LLM just
sort of hallucinating and making things up along the way.

So to me, this looks like a real success. I would feel comfortable
passing files in this stage along to a client and then highlighting
these areas where updates are needed and then have them review and
revise them. Before  I, were ready to, put these into, a
master, knowledge base.

And then I am going to quickly throw these seven files into a new Claude
project and we can test that out at the [01:00:00] end. And see, you
know, despite all the, the gaps that are remaining and things that we
need to fill in, let's, throw it into a project for our hypothetical
client and, see, see how it works.

I have created a new project that, I have added the seven knowledge base
files that were created, connected it to. So, I, I think certainly these
are not done. There are areas where there are gaps in them that you
would need to take to the client and review them, and update.

But, certainly we can test out. How they run here.

And you would also need to add in your instructions file too. That's
one piece that's missing. I may add, a extra step on this in the final
version that generates that, but if I don't, I think just copying and
modifying the instructions and adding them into the knowledge base.
Would work perfectly.

Oh great. So look  up state
[01:01:00] compliance rules, for North Carolina.

Now of course, you know, the problem is, is that this knowledge base
could, go. Out of, it could get outdated very quickly. And so, that is
something that is a concern that, you're gonna wanna keep in mind and
would be a great opportunity to propose a quarterly, retainer or to do
the review, and do the update with the same tools that you use to build,
the knowledge base in the first place.

But if this is the type of organization where this information changes
very quickly. This could hit some bottlenecks, in terms of, a solution.
So I think that's just good to keep in mind that this may not be the
best solution for every use case. Like if they need up to the minute
information, this probably would not be the way to do it.

But, given how they have been running their operations, up to
[01:02:00] this point, this does feel like a huge improvement. And
there you go. You now have your own, knowledge base building project set
up that you can replicate and use with clients in the future. And you
have, a working knowledge base for our hypothetical client True point
solutions.

So thanks for  so much for watching. Please feel free to reach
out to us with any questions, comments, or feedback, and I will see you
in the next lesson.
