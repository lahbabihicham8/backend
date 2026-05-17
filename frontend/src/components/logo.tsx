export function Logo() {
  return (
    <div className="flex items-center gap-3" aria-label="Khafeefa">
      <div className="grid size-12 place-items-center rounded-full bg-[var(--khafeefa-olive)] text-2xl font-bold text-[var(--warm-cream)]">
        ن
      </div>
      <div>
        <p className="text-2xl font-bold leading-none text-[var(--ink)]">خفيفة</p>
        <p className="font-[var(--font-latin)] text-xs font-semibold uppercase tracking-[0.2em] text-[var(--muted)]">
          khafeefa
        </p>
      </div>
    </div>
  );
}
