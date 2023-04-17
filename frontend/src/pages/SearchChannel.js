import React, { useState, useMemo } from "react";
import debounce from "lodash.debounce";
import { useNavigate } from "react-router-dom";
import { get } from "../utils/api";

function SearchChannel() {
  const navigate = useNavigate();
  const [channelId, setchannelId] = useState("");
  const [channels, setChannels] = useState([]);
  const [text, setText] = useState("");
  const isDisabled = channelId === "" || text === "";

  const submit = () => {
    if (isDisabled) return;
    navigate(`/search_video?video_id=${channelId}&text=${text}`);
  };

  const searchChannels = (channelName) => {
    if (channelName === "") return;
    get("channel/search?channel_name=" + channelName)
      .then((data) => {
        return data.json();
      })
      .then((channels) => {
        console.log(channels);
        setChannels(channels);
      });
  };

  const debouncedSearchHandler = useMemo(() => {
    return debounce((channelName) => {
      if (channelName === "") return;
      console.log(channelName);
      searchChannels(channelName);
    }, 500);
  }, []);

  return (
    <div className="flex flex-col justify-around" style={{ height: "100%" }}>
      <h1 className="text-4xl text-center text-emerald-300">
        Search for text in a youtube channel
      </h1>
      <Channels channels={channels} />
      <form className="flex flex-col gap-y-4" action="/search_video">
        <Input
          id="video_id"
          name="video_id"
          placeholder="Youtube channel"
          value={channelId}
          onInput={(e) => {
            setchannelId(e.target.value);
            debouncedSearchHandler(e.target.value);
          }}
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

function Channels({ channels }) {
  return (
    <div className="flex flex-col gap-y-4">
      {channels.map((channel) => (
        <div className="flex flex-row gap-x-4">
          <img src={channel.thumbnail_url} alt="channel thumbnail" />
          <div className="flex flex-col justify-center">
            <h1 className="text-xl">{channel.title}</h1>
            <p className="text-sm">{channel.description}</p>
          </div>
        </div>
      ))}
    </div>
  );
}

export default SearchChannel;
