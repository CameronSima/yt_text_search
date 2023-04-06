export function Matches({ matches, selected, setSelected }) {
  console.log(matches);
  return (
    <div className="flex flex-col gap-4">
      {matches.map((match) => (
        <Match
          key={match.id}
          match={match}
          selected={selected}
          setSelected={setSelected}
        />
      ))}
    </div>
  );
}

export function Match({ match, selected, setSelected }) {
  const selectedClass =
    selected?.id === match.id
      ? "bg-gray-400 hover:bg-gray-400"
      : "bg-white hover:bg-gray-200";

  const clickHander = () => {
    setSelected(match);
  };
  return (
    <div
      className={`w-full overflow-hidden shadow-lg cursor-pointer ${selectedClass}`}
      onClick={clickHander}>
      <div className="px-6 py-4">
        <p className="text-gray-800 text-base italic">
          {' "...'}
          {match.preceding_text}
          <span className="font-bold">{" " + match.exact_text + " "}</span>
          {match.following_text}
          {'..."'}
        </p>
        <p className="text-gray-500">{match.start_seconds_formatted}</p>
      </div>
    </div>
  );
}
