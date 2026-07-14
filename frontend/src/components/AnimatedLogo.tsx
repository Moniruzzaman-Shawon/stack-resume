export function AnimatedLogo() {
  const layers = [
    { delay: "0s", width: 40, y: 0 },
    { delay: "0.15s", width: 32, y: -6 },
    { delay: "0.3s", width: 24, y: -12 },
  ];

  const letters = "Stack Resume".split("");

  return (
    <div className="flex items-center gap-3">
      <div
        className="relative"
        style={{ width: 48, height: 40, animation: "glow-pulse 3s ease-in-out infinite" }}
      >
        {layers.map((layer, i) => (
          <div
            key={i}
            className="absolute left-1/2 rounded-md border-2 border-blue-600 dark:border-blue-500"
            style={{
              width: layer.width,
              height: 12,
              bottom: layer.y + 6,
              left: `calc(50% - ${layer.width / 2}px)`,
              backgroundColor: i === 2 ? "rgb(37, 99, 235)" : "transparent",
              opacity: 0,
              animation: `layer-slide-up 0.5s ease-out ${layer.delay} forwards`,
            }}
          />
        ))}
      </div>

      <div className="flex items-baseline overflow-hidden">
        <span
          className="text-2xl font-bold tracking-tight"
          style={{
            color: "rgb(37, 99, 235)",
            opacity: 0,
            animation: "text-fade-up 0.5s ease-out 0.4s forwards",
          }}
        >
          Stack
        </span>
        <span className="flex">
          {letters.slice(6).map((letter, i) => (
            <span
              key={i}
              className="text-2xl font-bold tracking-tight text-gray-900 dark:text-gray-50"
              style={{
                opacity: 0,
                animation: `letter-fade-up 0.3s ease-out ${0.5 + i * 0.04}s forwards`,
              }}
            >
              {letter === " " ? "\u00A0" : letter}
            </span>
          ))}
        </span>
      </div>
    </div>
  );
}
