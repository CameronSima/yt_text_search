import { useEffect, useState } from "react";
import { useSearchParams, Link } from "react-router-dom";
import { API_URL } from "../utils/api";
import { Matches } from "./Matches";
import Loading from "../Loading";

function ChannelResults() {
  const [searchParams] = useSearchParams();
  const [searchResults, setSearchResults] = useState([]);
  const [selected, setSelected] = useState({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const sse = new EventSource(
      `${API_URL}search_channel?${searchParams.toString()}`
    );
    sse.onmessage = (event) => {
      if (loading) setLoading(false);
      const searchResult = JSON.parse(event.data);
      console.log(searchResult);
      setSearchResults((searchResults) => [...searchResults, searchResult]);
    };
    return () => {
      sse.close();
    };
  }, [searchParams]);
  return (
    <div className="flex flex-col gap-4 h-screen">
      {loading ? (
        <div className="flex flex-col flex-1 justify-center items-center">
          <Loading />
        </div>
      ) : (
        <div className="overflow-y-scroll">
          {/* {searchResults.map((searchResult) => (
            <Matches
              matches={searchResult.matches}
              selected={selected}
              setSelected={setSelected}
            />
          ))} */}
          {searchResults.map((searchResult) => (
            <ChannelResult searchResult={searchResult} />
          ))}
        </div>
      )}
    </div>
  );
}

function ChannelResult({ searchResult }) {
  return (
    <div className={`w-full overflow-hidden shadow-lg cursor-pointer`}>
      <div className="px-6 py-4">
        <p className="text-gray-800 text-base">
          <Link
            to={`/search_video?video_id=${searchResult.video.id}&text=${searchResult.search_text}`}>
            {searchResult.video.title}
          </Link>
        </p>
        <p className="text-gray-800">
          {searchResult.num_results} results found
        </p>
        <p className="text-gray-500">{searchResult.video.published_at}</p>
      </div>
    </div>
  );
}

export default ChannelResults;
