import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

function SearchVideo() {
  const navigate = useNavigate();
  const [videoId, setVideoId] = useState("");
  const [text, setText] = useState("");
  const isDisabled = videoId === "" || text === "";

  const submit = () => {
    if (isDisabled) return;

    navigate(`/search_video?video_id=${videoId}&text=${text}`);
  };

  return (
    <div className="flex flex-col justify-around" style={{ height: "100%" }}>
      <h1 className="text-4xl text-center text-emerald-300">
        Search for text in a youtube video
      </h1>
      <form className="flex flex-col gap-y-4" action="/search_video">
        <Input
          id="video_id"
          name="video_id"
          placeholder="Youtube video url"
          value={videoId}
          onInput={(e) => setVideoId(e.target.value)}
        />
        <Input
          id="text"
          name="text"
          placeholder="Text to search for"
          value={text}
          onInput={(e) => setText(e.target.value)}
        />
        <button
          disabled={isDisabled}
          onClick={submit}
          className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
          type="button">
          Search
        </button>
      </form>
    </div>
  );
}

function Input({ id, name, placeholder, value, onInput }) {
  return (
    <input
      className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
      id={id}
      name={name}
      value={value}
      type="text"
      placeholder={placeholder}
      onInput={onInput}
    />
  );
}

export default SearchVideo;
