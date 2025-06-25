# Different Types Of Text Track

<!-- tl;dr starts -->

"Text track" is the general term I used to indicate subtitles, captions (both open and closed), SDH, in-band, out-of-band, burned-in, forced subtitles ...

<!-- tl;dr ends -->

## Terminology

According to EBU-TTMP specification:

```md
- **Subtitles:** screen text for translation purposes.
- **Captions:** screen text for both translation purposes and use by deaf and hard of hearing audiences. They include indications of the speakers and relavant sound effectsc (e.g. [crowd cheers], [eerie background music plays], ...)
```

My understanding:

- **Opened Captions:** captions which are perminently embedded into the video frames.
- **Closed Captions/CC:** captions that can be toggled on/off.
- **Burned-in Subtitles/Opened Subtitles/Hard-coded Subtitles/Hardsubs:** subtitles which are perminently embedded into the video frames.
- **Forced Subtitles:** subtitles which provided when the characters speak a foreign or alien language, or a sign, flag, or other text in a scene is not translated in the localization and dubbing process.[^jf]
- **SDH**: "Subtitles for the Deaf and Hard or hearing", the term Apple refers to **Closed Captions**.

Technically speaking, captions are just subtitles with sound effects. Engineers don't create new format and specification for captions but reuse from subtitles' counterpart.

From now on, all of these terminologies will be referred to as "text tracks".

[^jf]: https://jellyfin.org/docs/general/clients/codec-support/#forced

## Ways to transferring text tracks: In-band and Out-of-band

### In-band text tracks

"In-band" is the term that refers to text tracks that are transmitted or stored _along with_ the video and audio data. They are either put in the same analog/digital signal or media container digital file.

#### Broadcast text tracks

_Definition:_ Text tracks are transmitted as part of the live television broadcase signal (over-the-air, cable, satellite). The text tracks are multiplexed (muxed) along with the video and audio signals then your TV or Set-top box/Over the top/OTT devices can demultiplexed (demuxed), then decodes the text tracks to display them on screen.

_Formats:_

- **CEA-608**: analog captions system. Only white text on a black background can be display, supported two languages at max. Commonly used for Closed Captions in North America.[^nad]
- **CEA-708**: digital captions system. Allow viewers to change the size, color, font and other features of the captions. commonly used for Closed Captions in North America.[^nad]
- **DVB EN 300 743**: a bitmap-based subtitles format used in DVB broadcast, commonly used in Europe and other regions.
- **Teletext:** an older system, also common in Europe.

> This type of transferring text tracks are archaic since internet streaming is so popular now, still it's good to know about it.

[^nad]: https://www.nad.org/resources/technology/television-and-closed-captioning/analog-and-digital-closed-captioning/

#### Digital File text tracks/Embedded text tracks

_Definition:_ The text tracks data (which can be text-based like SRT/ASS/WebVTT or image-based such as FGS/VobSub) is packaged as subtitle streams, along side with video and audio streams within a media container file.

Text tracks are _toggleable_ which means they can be switched on/off or change from one stream to another stream.

> **NOTE:** formats and external file extensions are two very different things.

_Example:_ if you opened a media file embedding a lot of subtitle streams, they are digital file text tracks.

### Cons of in-band text tracks

- The media container file must be re-packaged when a new text track file supporting a new language is created or an update to the existing text tracks need to be made.[^mux]

[^mux]: https://www.mux.com/blog/subtitles-captions-webvtt-hls-and-those-magic-flags#in-band

### Out-band/Out-of-band

_Definition:_ The text tracks are delivered separately from the media container file. They can reside in a separate text file (or a collection of text files) which are then referenced from the HLS or DASH manifest (or playlist) `.m3u8` file.

_Formats:_

- SRT (SubRip Text): born of the application bearing the same name, unpopular in the ripping community dues to its lack of support on OTT devices and limited feature set.
- ASS (Advanced SubStation Alpha)
- WebVTT (Web Video Text Tracks): a W3C standard for the interchange of text track resources. Simple, closely resembles SRT, can be formatted and positioned. Beside being used as text tracks, it can also be used for other forms of structured metadata that you might want to deliver alongside your content.
- PGS (Presentation Graphic Stream) (common on BluRay)
- VobSub (SUB/IDX) (common on DVD)
- `tx3g`/`mov_text` (common in MP4 containers)

_Example:_ `.srt`/`.ass`/`.vtt` files that you put in the same directory as your `.mkv`/`.mp4` file
