### Overview

- [Examples &amp; Tutorials](\examples-and-tutorials)

### Agentic Workflows

- [Overview](\examples-and-tutorials\ai-copilots)
- [Pair Programmer](\examples-and-tutorials\ai-copilots\pair-programmer)
- [OpenClaw Monitoring](\examples-and-tutorials\ai-copilots\openclaw-monitoring)
- [Call.md](\examples-and-tutorials\ai-copilots\call-md)
- [Bloom](\examples-and-tutorials\ai-copilots\bloom)
- [Focusd](\examples-and-tutorials\ai-copilots\focusd)

### Video Search and Understanding

- [Overview](\examples-and-tutorials\video-rag)
- [Keyword Search](\examples-and-tutorials\video-rag\keyword-search)
- [Character Extraction](\examples-and-tutorials\video-rag\character-clips)
- [Multimodal Search](\examples-and-tutorials\video-rag\multimodal-search)
- [Case Study: NFL Game Analysis](\examples-and-tutorials\video-rag\case-study-nfl)
- [Use Case: Conference Slide Extraction](\examples-and-tutorials\video-rag\use-case-conference-slides)

### Live Intelligence

- [Overview](\examples-and-tutorials\live-intelligence)
- [Baby Crib Monitoring with AI](\examples-and-tutorials\live-intelligence\baby-crib-monitoring)
- [Intelligent Property Intrusion Detection](\examples-and-tutorials\live-intelligence\intrusion-detection)
- [Flash Flood Early Warning System](\examples-and-tutorials\live-intelligence\flash-flood-detection)
- [Multi-Use Road Monitoring System](\examples-and-tutorials\live-intelligence\road-monitoring)
- [Dashcam Monitoring of Traffic](\examples-and-tutorials\live-intelligence\roadcam-monitoring)
- [Traffic Violation Detection](\examples-and-tutorials\live-intelligence\traffic-violations)
- [Live Cricket Highlight Detection](\examples-and-tutorials\live-intelligence\cricket-match-monitoring)
- [Multi-Camera Basketball Analytics](\examples-and-tutorials\live-intelligence\multicam-basketball-analysis)
- [Multi-Camera Public Safety Surveillance](\examples-and-tutorials\live-intelligence\multicam-public-surveillance)
- [TwelveLabs Integration](\examples-and-tutorials\live-intelligence\twelvelabs-integration)

### Content Factory

- [Overview](\examples-and-tutorials\content-factory)
- [Faceless Video Creator](\examples-and-tutorials\content-factory\faceless-video-creator)
- [AI-Generated Ads](\examples-and-tutorials\content-factory\ai-ad-films)
- [TikTok Style Lyric Video Creator](\examples-and-tutorials\content-factory\tiktok-lyric-video)
- [Video Dubbing](\examples-and-tutorials\content-factory\dubbing)
- [AI Voiceovers](\examples-and-tutorials\content-factory\voiceovers)
- [Trailer Narration](\examples-and-tutorials\content-factory\trailer-narration)
- [Voice Cloning](\examples-and-tutorials\content-factory\voice-cloning)
- [Text to Video](\examples-and-tutorials\content-factory\text-prompts)
- [AI Storyteller for Kids](\examples-and-tutorials\content-factory\ai-storyteller-kids)
- [Annual Video Statistics Recap](\examples-and-tutorials\content-factory\year-in-frames)
- [PromptClip](\pages\community\open-source\promptclip)

### Programmatic Editing

- [Overview](\examples-and-tutorials\programmatic-editing)
- [Intro/Outro](\examples-and-tutorials\programmatic-editing\intro-outro)
- [Brand Elements](\examples-and-tutorials\programmatic-editing\brand-elements)
- [Audio Overlay](\examples-and-tutorials\programmatic-editing\audio-overlay)
- [Dynamic Ads](\examples-and-tutorials\programmatic-editing\dynamic-ads)
- [Dynamic Streams](\examples-and-tutorials\programmatic-editing\dynamic-streams)
- [Word Counter](\examples-and-tutorials\programmatic-editing\word-counter)
- [Chess Match Montage Generator](\examples-and-tutorials\programmatic-editing\chess-montage)

### Safety &amp; Compliance

- [Overview](\examples-and-tutorials\safety-compliance)
- [Profanity Detection](\examples-and-tutorials\safety-compliance\beep-profanity)
- [AI-Powered Content Moderation](\examples-and-tutorials\safety-compliance\remove-content)
- [AI Video Copyright Detection](\examples-and-tutorials\safety-compliance\copyright-detection)

## On this page

- [Live video to Instant Action](#live-video-to-instant-action)
    - [Reality of Building Video AI](#reality-of-building-video-ai)
    - [Simplifying Video AI Infrastructure with VideoDB](#simplifying-video-ai-infrastructure-with-videodb)
- [Introducing the TwelveLabs Integration: Your Frame Understanding, Supercharged](#introducing-the-twelvelabs-integration-your-frame-understanding-supercharged)
- [Real-World Use Cases: From Theory to Action](#real-world-use-cases-from-theory-to-action)
- [Real-World Use Cases in Action](#real-world-use-cases-in-action)
    - [🌊 Flash Flood Detection](#-flash-flood-detection)
    - [👶🏻 Baby Crib Monitoring](#-baby-crib-monitoring)
- [How It Works: One Line of Code to Unlock a New World](#how-it-works-one-line-of-code-to-unlock-a-new-world)
- [Try It Now: Interactive Notebooks](#try-it-now-interactive-notebooks)

[Live Intelligence](\examples-and-tutorials\live-intelligence\index)

# TwelveLabs Integration

Copy page

Real-time video understanding with advanced AI models

Copy page

**Human Monitoring is Expensive, Exhausting, and Doesn't Scale**

From baby monitors to warehouse cameras or endless CCTV feeds, many companies still depend on human eyes to monitor live video-a costly, tedious, and highly error-prone approach. Fatigue inevitably sets in, accuracy declines, and scaling up means hiring more personnel rather than enhancing systems. But in an AI-driven era, monitoring shouldn't be manual, miss critical details, or become a bottleneck. Imagine receiving instant alerts when packages are stolen, notifying parents the moment a baby attempts to climb out of a crib, proactively highlighting safety risks before they escalate, or doctors instantly knowing when ICU patients need immediate attention. This is precisely the responsive monitoring [**VideoDB**](https://videodb.io/real-time-video-intelligence#header) delivers through its real-time infrastructure. VideoDB now provide first party integration with [**TwelveLabs**](https://www.twelvelabs.io/) 's advanced **Pegasus 1.2** AI model for precise frame understanding.

## [ Live video to Instant Action](#live-video-to-instant-action)

Real-time video analysis isn't merely a nice-to-have-it's a fundamental shift in capability.

- **Safety and Security** : Transforming reactive measures into proactive alerts, potentially saving lives during emergencies like flash floods or security breaches.
- **Enterprise Productivity** : Converting passive meeting archives into interactive, searchable knowledge repositories, vastly enhancing collaboration.
- **Content Platforms** : Automatically tagging, chaptering, and moderating content in unprecedented detail, elevating user experiences.

The opportunities are immense, yet technical barriers have historically prevented many development teams from unlocking this potential.

### [ Reality of Building Video AI](#reality-of-building-video-ai)

If you've ever attempted to build a robust video understanding system, you know the pain firsthand. You're often stuck playing the role of a systems integrator, wrestling with:

- **API Spaghetti** : Managing credentials, juggling rate limits, and navigating diverse SDKs across multiple video processing, AI modeling, and storage services.
- **Scaling Nightmares** : Each component scales independently, causing bottlenecks and inefficiencies-particularly with resource-intensive GPU workloads.
- **Latency Issues** : The delays involved in interactions between storage, AI models, and your applications undermine genuine real-time capabilities.

These challenges can quickly stall innovation, turning promising ideas into lengthy, frustrating engineering endeavors.

### [ Simplifying Video AI Infrastructure with VideoDB](#simplifying-video-ai-infrastructure-with-videodb)

VideoDB is a purpose-built infrastructure for AI driven video management. It provides a unified, AI-native infrastructure handling the complete lifecycle of video content-from ingestion and indexing to alert management-all via a streamlined, developer-friendly API. Leveraging VideoDB, you can effortlessly ingest multiple real-time video streams, manage customizable indexes uniquely tailored for specific analyses, and simultaneously analyze diverse aspects of a single video stream. Additionally, VideoDB's targeted alerting system triggers automated webhooks, ensuring rapid responses to critical events. And now, we've equipped that powerful infrastructure with an even more powerful intelligence.

## [ Introducing the TwelveLabs Integration: Your Frame Understanding, Supercharged](#introducing-the-twelvelabs-integration-your-frame-understanding-supercharged)

We're excited to announce our native integration with TwelveLabs-going far beyond a traditional partnership. We've seamlessly embedded TwelveLabs' advanced AI, powered by the exceptional Pegasus 1.2 model, directly within VideoDB.

VideoDB and TwelveLabs integration architecture showing seamless AI embedding

<!-- image -->

**What does that mean for you?**

- No additional accounts.
- No extra API keys.
- Zero integration headaches.

Now, accessing TwelveLabs' sophisticated video understanding models, like Pegasus, is as easy as adding a single parameter to your indexing call. All the AI power you need is fully integrated into your VideoDB environment-effortlessly blending world-class intelligence with unmatched simplicity.

## [ Real-World Use Cases: From Theory to Action](#real-world-use-cases-from-theory-to-action)

With VideoDB + TwelveLabs, sophisticated real-time video monitoring is just minutes away:

## [ Real-World Use Cases in Action](#real-world-use-cases-in-action)

### [ 🌊 Flash Flood Detection](#-flash-flood-detection)

Real-time flash flood detection example - Click to open notebook

<!-- image -->

[Click image to open interactive notebook →](https://colab.research.google.com/github/video-db/videodb-cookbook/blob/main/integrations/twelvelabs/Flash_Flood_Detection_TwelveLabs.ipynb)

Imagine a camera monitoring a dry riverbed in a flood-prone area. With TwelveLabs integrated into VideoDB, you can continuously detect critical events-like rapidly rising floodwaters-in real-time. The moment Pegasus recognizes the signs of a flash flood, VideoDB immediately triggers life-saving alerts. This isn't just video analysis; it's proactive, intelligent disaster prevention.

### [ 👶🏻 Baby Crib Monitoring](#-baby-crib-monitoring)

Baby crib monitoring example - Click to open notebook

<!-- image -->

[Click image to open interactive notebook →](https://colab.research.google.com/github/video-db/videodb-cookbook/blob/main/integrations/twelvelabs/Baby_Crib_Monitoring_TwelveLabs.ipynb)

After a long day, parents deserve restful, worry-free sleep. With VideoDB's real-time monitoring powered by TwelveLabs' Pegasus, you'll instantly know if your baby tries climbing out of the crib or needs immediate attention. Sleep easy, knowing VideoDB and TwelveLabs have you covered-every second of the night.

## [ How It Works: One Line of Code to Unlock a New World](#how-it-works-one-line-of-code-to-unlock-a-new-world)

Ready to see how simple this is? To index a video stream with TwelveLabs' powerful Pegasus model, you just specify it as the `model_name` .

Python

Node.js

```
# Your existing stream object
# flood_stream = coll.connect_rtstream(...)

# Index visuals using TwelveLabs' Pegasus model
flood_scene_index = flood_stream.index_visuals(
batch_config = {
"type" : "time" ,
"value" : 10 ,
"frame_count" : 6 ,
},
prompt = "Monitor the dry riverbed and surrounding area. If moving water is detected across the land, identify it as a flash flood and describe the scene." ,
# This is the magic line!
model_name = "twelvelabs-pegasus-1.2" ,
name = "Flash_Flood_Detection_Index"
)

print ( "Scene Index ID:" , flood_scene_index.id)
```

```
// Your existing stream object
const floodStream = await coll . connectRTStream (
"rtsp://your-stream-url" ,
"Flood Detection Stream"
);

// Index visuals using TwelveLabs' Pegasus model
const floodSceneIndex = await floodStream . indexVisuals ({
batchConfig: {
type: "time" ,
value: 10 ,
frameCount: 6 ,
},
prompt: "Monitor the dry riverbed and surrounding area. If moving water is detected across the land, identify it as a flash flood and describe the scene." ,
// This is the magic line!
modelName: "twelvelabs-pegasus-1.2" ,
name: "Flash_Flood_Detection_Index"
});

console . log ( "Scene Index ID:" , floodSceneIndex . id );
```

This integration lets you seamlessly test out TwelveLabs models right inside VideoDB's indexing pipeline-giving you maximum flexibility, control, and ease. Now, you can instantly build real-time visual understanding apps without friction. We can't wait to see what you create!

## [ Try It Now: Interactive Notebooks](#try-it-now-interactive-notebooks)

Ready to build your own real-time video intelligence system? Open these interactive notebooks directly in Google Colab and start experimenting with TwelveLabs' Pegasus model:

## Flash Flood Detection Notebook

Build a real-time flood detection system that monitors dry riverbeds and sends instant alerts

## Baby Crib Monitoring Notebook

Create an AI-powered baby monitor that detects escape attempts and keeps parents informed

[Multi-Camera Public Safety Surveillance](\examples-and-tutorials\live-intelligence\multicam-public-surveillance) [Overview](\examples-and-tutorials\content-factory)

⌘ I