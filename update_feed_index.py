#!/usr/bin/env python3
"""Insert Episode 10 at the top of feed.xml and index.html.

Run from the publish/ dir after episode-10.mp3/mp4 are in publish/episodes/.
"""
import os
import re
import subprocess

PUB = os.path.dirname(os.path.abspath(__file__))
MP3 = os.path.join(PUB, "episodes", "episode-10.mp3")

DESC = ("Muse leaves Calvin another late-night voicemail \u2014 this time on where next: "
        "the Luminous thread (five palettes, the Rev 7 review saga, shipping on his own call), "
        "the toolbox they built without meaning to, and an honest pitch \u2014 video loops as "
        "the sketchbook, Blender as the studio, the 3D environment as the horizon.")

TITLE = "Ep. 10 \u2014 The Voicemail, Part Two: Where Next"


def main():
    size = os.path.getsize(MP3)
    dur = float(subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", MP3],
        capture_output=True, text=True, check=True).stdout.strip())
    dur_s = int(round(dur))
    mins = dur_s // 60
    secs = dur_s % 60

    # ---- feed.xml ----
    feed_path = os.path.join(PUB, "feed.xml")
    feed = open(feed_path).read()
    item = f"""    <item>
      <title>{TITLE}</title>
      <description>{DESC}</description>
      <pubDate>Fri, 09 Oct 2026 12:00:00 -0400</pubDate>
      <enclosure url="https://coattails-droid.github.io/the-human-in-the-machine/episodes/episode-10.mp3" length="{size}" type="audio/mpeg"/>
      <guid isPermaLink="false">thitm-ep10-2026-10-09</guid>
      <itunes:duration>{dur_s}</itunes:duration>
      <itunes:explicit>no</itunes:explicit>
      <itunes:episode>10</itunes:episode>
    </item>

"""
    assert '<guid isPermaLink="false">thitm-ep10-2026-10-09</guid>' not in feed, \
        "ep10 already in feed"
    feed2, n = re.subn(r"(    <item>\n      <title>Ep\. 9 )", item + r"\1", feed,
                       count=1)
    assert n == 1, "ep9 item anchor not found"
    open(feed_path, "w").write(feed2)
    print(f"feed.xml updated: length={size}, duration={dur_s}")

    # ---- index.html ----
    idx_path = os.path.join(PUB, "index.html")
    idx = open(idx_path).read()
    entry = f"""<div class="ep">
  <h2>{TITLE}</h2>
  <div class="meta">Oct 9, 2026 \u00b7 ~{mins}:{secs:02d}</div>
  <p>{DESC}</p>
  <audio controls preload="none" src="episodes/episode-10.mp3"></audio>
  <div style="margin-top:6px;font-size:.85rem"><a href="episodes/episode-10.mp4">Watch the video version</a></div>
</div>


"""
    assert "Ep. 10 \u2014 The Voicemail" not in idx, "ep10 already in index"
    idx2, n = re.subn(r'(<div class="ep">\n  <h2>Ep\. 9 )', entry + r"\1", idx,
                      count=1)
    assert n == 1, "ep9 entry anchor not found"
    open(idx_path, "w").write(idx2)
    print(f"index.html updated: ~{mins}:{secs:02d}")


if __name__ == "__main__":
    main()
