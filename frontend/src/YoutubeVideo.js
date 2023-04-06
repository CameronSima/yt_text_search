import React, { useEffect, useRef } from "react";
import YouTube from "react-youtube";

const videoOpts = {
  height: "390",
  width: "100%",
};

function YouTubeVideo({ videoId, seekTime }) {
  const playerRef = useRef(null);

  useEffect(() => {
    if (playerRef?.current?.internalPlayer) {
      playerRef.current.internalPlayer.seekTo(seekTime);
    }
  }, [seekTime]);
  return videoId ? (
    <YouTube videoId={videoId} opts={videoOpts} ref={playerRef} />
  ) : (
    <div></div>
  );
}

export default YouTubeVideo;
