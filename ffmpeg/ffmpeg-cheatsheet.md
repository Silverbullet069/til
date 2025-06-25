# FFmpeg Cheatsheet

<!-- tl;dr starts -->

This is the most complex tool that I've used.

<!-- tl;dr ends -->

```sh
#!/bin/sh

# TODO: vector indexed the following file in your LLM.
# HLS mux docs: https://ffmpeg.org/ffmpeg-all.html#hls-2
# Re-encode docs: https://trac.ffmpeg.org/wiki/Encode/H.264#Profile

# NOTE: Phil Cluff's "Subtitles, Captions, WebVTT, HLS, magic flags"
# NOTE: https://www.mux.com/blog/subtitles-captions-webvtt-hls-and-those-magic-flags

local -ra ffmpeg_options=(
  # overwrite files without confirmation
  -y
  # input file
  -i path/to/input/file.{mkv,mp4,...}
  # don't print copy right notice, build options, lib options
  -hide_banner
  # print encoding progress (on by default)
  -stats
  # set logging level and flags (quiet, panic, fatal, error, warning, info, verbose, debug, trace)
  -loglevel error
  # map video stream
  -map 0:v:0
  # map audio stream. Use `0:a:x` syntax to change starting index
  -map "0:${audio_stream_index}"
  # map subtitle stream. Use `0:a:x` syntax to change starting index
  -map "0:${subtitle_stream_index}"

  # ===================================================================== #
  # libx264-specific options, best video codec                            #
  # ===================================================================== #
  -c:v libx264
  # delegate bitrate control to CRF
  -b:v 0
  # Max keyframe interval.
  -g $(("$fps" * "$segment_time"))
  # disable scene change detection, make consistent quality + allow encoder to make optimize decisions about keyframe placement
  -sc_threshold 0
  # optimal for most use cases, good compatibility with devices while supporting high quality encoding up to 1080p
  -level "4.1"
  # Adaptive B-frame placement for best compression efficiency
  -b_strategy 2
  # Minimum GOP size
  # CAUTION: according to https://superuser.com/a/1600616/2206521, keyint_min within libx264 is capped at keyint / 2 + 1
  -keyint_min $(("$fps" * "$segment_time"))
  # Uses all available CPU cores/threads.
  -threads "$(nproc)"
  # preset, a collection of options that will provide a certain encoding speed
  # to compression ratio
  # slower preset = better compression = lower file size + save bitrate
  # bitrate = file size / duration (convention unit is kiloBits per second)
  -preset "veryslow"
  # change settings based upon the specifics of your input
  # "film"= high-quality movie content
  # "animation"=good for cartoon
  # "zerolatency"=low-latency streaming
  # CAUTION: omit is preferred if you don't know which value to specify
  -tune "film"
  # constant rate factor, one of the rate control modes
  # recommended for keeping the best quality and ignore file size
  # pros: provides maximum compression efficience + single-pass
  # cons: can't specify arbitrary file size or the maximum boundary of the file size or bitrate => not recommended for encoding videos for streaming
  # 0=lossless 8-bit, 23=def, 51=worst (8-bit). 17-18 is the most optimal (battle-tested)
  -crf 18
  # prevents VBV from lowering quality beyond this point
  -crf_max 18
  # limits the output to a specific H264 profile
  # CAUTION: best to omit, let the appropriate profile be chosen automatically
  -profile:v "high"

  # ===================================================================== #
  # libx265 specific options                                           #
  # ===================================================================== #
  -c:v libx265 
  -b:v 0
  -g "${gop}"
  -keyint_min "${gop}"
  # Slow is enough, according to https://x265.readthedocs.io/en/stable/presets.html#presets
  # NOTE: some Blender's movies are rendered using "slow" preset
  -preset "slow"
  # improve encode quality for animated content
  -tune "animation"
  -profile "high"
  # NOTE: According to https://www.reddit.com/r/ffmpeg/comments/luo5bm/comment/gp8qj8g
  # CRF 23 H265 == CRF 18 H264
  -crf 23
  -x265-params bframes=16:psy-rd=1.5:psy-rdoq=2:aq-mode=3:ref=6

  # ===================================================================== #
  # libvpx-vp9-specific options                                           #
  # ===================================================================== #
  -c:v libvpx-vp9
  -b:v 0
  # For VPX, CRF range is 4-63
  -crf 18 
  # Max keyframe interval. E.g. for -hls_time=10, 25fps * 10s = 250
  -g 250
  # good=nice trade-off between speed and quality when used with `cpu-used` option
  -deadline good # "realtime"
  # Set quality/speed ratio modifier. Lower is slower but better quality
  -cpu-used 0
  # Enables row-based multithreading for potentially faster encoding on multi-core CPUs without significant quality loss
  -row-mt 1
  # Number of tile columns (log2). E.g., 2 for 4 tile columns. Aids parallelism.
  -tile-columns 2
  # Enables automatic use of alternate reference frames, which can improve compression efficiency and quality.
  -auto-alt-ref 1
  # Number of frames to buffer for lookahead, allowing the encoder to make better decisions. Increases latency but can improve quality.
  -lag-in-frames 25
  # Uses all available CPU cores/threads.
  -threads "$(nproc)"
  # ===================================================================== #

  # ===================================================================== #
  # libopus-specific options                                              #
  # ===================================================================== #
  -c:a libopus
  # Audio bitrate # NOTE: depends on audio codec
  -b:a 96k # opus: 48k/96k for stereo, 128k for 5.1
  # Enables Variable Bitrate for Opus, allowing for more efficient bit allocation and better quality.
  -vbr on
  # Higher values = better quality, slower encoding
  -compression_level 10
  # Hints to the encoder that the content is general audio, optimizing for fidelity.
  -application audio
  # Re-encode subtitle stream to WebVTT format
  -c:s webvtt
  # create a HLS variant stream, specified in master playlist
  # include subtitle, name, language and default
  -var_stream_map "v:0,a:0,s:0,sgroup:subtitle,name:eng,language:en-US,default:YES"

  # ===================================================================== #
  # Hls-related Options                                                   #
  # ===================================================================== #
  -f hls
  # Enable Low-latency HLS
  # Add #EXT-X-PREFETCH tag
  # (i.e. pass '-streaming 1' and '-hls_playlist 1' options)
  # CAUTION: experimental feature
  -lhls 1
  # Disable generating HSL playlist file. Def=1
  -hls_playlist 0
  # If -hls_playlist=1, specify the format of master name
  -master_pl_name "${input_basename}_master.m3u8"
  # define output segment files' format
  # mpegts=.ts # fmp4=.mp4
  -hls_segment_type mpegts
  # independent_segments: FFmpeg will add a metadata tag to playlists whose audio segments (all of them) are guaranteed to start with a "key frame", not on frames other than "key frames".
  # program_date_time: Generate EXT-X-PROGRAM-DATE-TIME tags.
  -hls_flags independent_segments+program_date_time
  # hls_list_size forced to 0, it's cthe maximum number of playlist entries.
  # when hls_list_size should be limited is when live-streaming, where the number playlist entries are unknown
  -hls_playlist_type vod
  # Define the segment file name's format. NOTE: if there are more than 1 HLS varient streams, indicate them with %v placeholder
  -hls_segment_filename "${input_basename}_%05d.ts"
  # Target segment length.
  # TODO: develop an algorithm that determines the best hls_time based on movie duration, media file size, TS file size, network throughput, ...
  -hls_time 6
  #  %v is replaced by `name:` metadata specified at -var_stream_map
  # NOTE: metadata in master playlist won't show up if omitted
  -hls_subtitle_path "${input_basename}_%v_vtt.m3u8"
  # Enable AES-128 encryption, every segment generated is encrypted, and the encryption key is saved as <playlist name>.key
  -hls_enc 1
  # Minimize pkt_dts and pkt_dts_time, which prevents subtitles out-of-sync. Cre: https://github.com/videojs/http-streaming/issues/1216#issuecomment-1854110474
  -muxdelay 0
  "path/to/output/file.m3u8"

  # ===================================================================== #
  # Dash-related Options                                                  #
  # ===================================================================== #
  -f dash
  # Specified in MPD manifest AdaptationSets section, 3 maps, 3 sections
  -adaptation_sets "id=0,streams=0 id=1,streams=1"
  # Specify extension for segment files
  -dash_segment_type webm
  # Generate HSL playlist file
  # NOTE: HLS-specific options can be defined, but not vice-versa
  -hls_playlist 1
  # Enable Low-latency DASH
  -ldash 1
  # Set 1 ore more MPD manifest profiles
  -mpd_profile dash
  # similar to -hls_time
  -seg_duration 10
  # enabled if live streaming
  -streaming 1
  # disable the use of SegmentTemplate instead of SegmentList in the manifest. Def=1
  -use_template 0
  # disable the use of SegmentTimeline within the SegmentTemplate manifest section. Def=1
  -use_timeline 1
  # all segments are kept in the manifest file, discard the oldest one, useful for live streaming
  # 0=all segments are kept in the manifest. Useful for video-on-demand.
  -window_size 0
  # Minimize pkt_dts and pkt_dts_time, as in original command
  -muxdelay 0
  path/to/output/file.mpd
)
```
