import PageShell from "../components/PageShell";

function NotFound() {
  return (
    <PageShell>
      <h1 className="text-xl font-semibold text-white sm:text-2xl">Page not found</h1>
      <div className="border border-white/40 p-6 text-sm text-[#E0E0E0]">Check the address or return to the scoreboard.</div>
    </PageShell>
  );
}

export default NotFound;
