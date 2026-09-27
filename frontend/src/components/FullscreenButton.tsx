import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faCompress, faExpand } from "@fortawesome/free-solid-svg-icons";

function FullscreenButton({ active, label, onClick }: { active: boolean; label: string; onClick: () => void }) {
  const description = active ? `Exit fullscreen for ${label}` : `Fullscreen ${label}`;
  return (
    <button
      type="button"
      onClick={onClick}
      aria-label={description}
      title={description}
      className="inline-flex size-9 shrink-0 items-center justify-center self-end border border-white/50 text-white hover:bg-white hover:text-black focus-visible:outline focus-visible:outline-offset-2 focus-visible:outline-white"
    >
      <FontAwesomeIcon icon={active ? faCompress : faExpand} aria-hidden="true" />
    </button>
  );
}

export default FullscreenButton;
