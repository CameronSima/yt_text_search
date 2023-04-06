import React, { useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom";
import { get } from "../utils/api";
import YouTubeVideo from "../YoutubeVideo";
import Loading from "../Loading";
import { Matches } from "./Matches";

function VideoResults() {
  const [searchParams] = useSearchParams();
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [searchResult, setSearchResult] = useState({
    matches: [],
    num_results: 0,
    search_text: "",
    video: {
      id: "",
      url: "",
      published_at: "",
      title: "",
      description: "",
    },
  });
  const [selected, setSelected] = useState({});

  useEffect(() => {
    console.log(searchParams);
    const videoId = searchParams.get("video_id");
    const text = searchParams.get("text");
    if (!videoId || !text) return;

    get("search_video/?" + searchParams.toString(), { video_id: videoId, text })
      .then((data) => {
        console.log(data);
        return data.json();
      })
      .then((searchResult) => {
        if (searchResult.error) {
          setError(searchResult.error);
          return;
        }
        console.log(searchResult);
        setSearchResult(searchResult);
        if (searchResult.matches.length > 0) {
          setSelected(searchResult.matches[0].id);
        }
      })
      .finally(() => setLoading(false));
  }, [searchParams]);

  return (
    <div className="flex flex-col gap-4 h-screen">
      {loading ? (
        <div className="flex flex-col flex-1 justify-center items-center">
          <Loading />
        </div>
      ) : (
        <>
          <YouTubeVideo
            videoId={searchResult?.video?.id}
            seekTime={selected?.start_seconds}
          />
          <ResultsText searchResult={searchResult} />
          <div className="overflow-y-scroll">
            <Matches
              matches={searchResult.matches}
              selected={selected}
              setSelected={setSelected}
            />
          </div>
        </>
      )}
    </div>
  );
}

function ResultsText({ searchResult }) {
  if (searchResult?.num_results > 0) {
    return (
      <h2 className="text-gray-100 text-2xl underline my-6">
        {searchResult.num_results} results found for
        <span className="font-bold italic">"{searchResult.search_text}"</span>
      </h2>
    );
  }
  return (
    <h2 className="text-gray-100 text-2xl underline my-6">
      No results found for
      <span className="font-bold italic">"{searchResult.search_text}"</span>
    </h2>
  );
}

export default VideoResults;
