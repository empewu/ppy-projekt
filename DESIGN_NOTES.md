# Design Notes

Design rationale, balance findings, and the roadmap for the RPG. Companion to
`CLAUDE.md` (which covers architecture). Written so future work doesn't have to
re-derive *why* things are the way they are.

## The arc of the rebalance

The game started with hardcoded item stats and a flat combat loop where one
build was strictly best. Work proceeded in phases, each simulated before moving
on:

1. **Tunable parameters** — every number moved into `balance.toml` behind a
   validating loader, so balance is data, not code.
2. **Stat-scaling damage, weapon types, Endurance defence** — attacks scale with
   a governing stat; weapons have melee/ranged/magic types.
3. **Enemy weaknesses/resistances + combat retune** — enemies favour/punish
   damage types, creating rock-paper-scissors pressure.
4. **Soft lock-in rings + economy attrition** — choices have opportunity cost.
5. **Data-driven starting kits, starting gold, save versioning.**
6. **Endurance (tank) gear progression + per-location enemy variety** — all four
   attributes became viable builds.

Then three player-experience problems were identified and fixed (below).

## Problems identified and shipped fixes

### #1 — Invisible combat math  *(shipped)*
Enemy weaknesses/resistances existed but were invisible, so the
matchup system might as well not have been there. **Fix:** `describe_matchup`
prints a one-line hint when an enemy appears — green "vulnerable to your X
attacks", red "resists your X attacks", silent when neutral.

- **Rationale for reading *equipped* weapons** (not the enemy's raw stats): the
  hint is then always actionable ("your current sword is bad here") rather than
  an info-dump of hidden numbers. A player with mixed damage types sees only
  what's relevant to their loadout.
- **Rationale for staying silent on neutral:** avoids nagging; a hint appearing
  *means* something.

### #2 — Shallow combat  *(shipped, via alchemy)*
Combat was only "attack / flee" — no decisions. **Fix:** consumable potions add
an in-fight choice (heal vs. buff vs. just attack).

### #3 — Purposeless loot  *(shipped, via alchemy)*
Monster parts were loot with no use. **Fix:** they became crafting ingredients,
with each tier given a distinct role (common → heal, rare → defend, magical →
empower). Loot descriptions now name what each part brews.

## Alchemy design decisions (and why)

- **Using an item costs your turn** (the enemy still strikes). This is the
  single most important decision — it makes healing/buffing a *tempo* choice, not
  a free reset, and it structurally prevents degeneracy (see findings). Cancelling
  the item menu is free; only actually using one spends the turn.
- **Buffs are fight-scoped** (reset when the fight ends), so they're a per-fight
  tactical investment, not permanent power creep on the character.
- **Craft-only** — potions never enter the trader's buy pool and are priced
  *below* their ingredients, so there's no craft-to-sell money exploit. They
  remain sellable (at a loss) so they're not dead weight.
- **Stoneskin is a flat per-hit reduction, not +defence.** Defence here is
  percentile (`100/(100+def)`), which barely blunts low flat enemy damage even at
  large values — a "+20 defence" potion saved ~1 HP/hit in testing. A flat −N per
  hit (floored at 1) is intuitive and actually impactful. Tuning defensive
  effects, prefer flat reduction over +defence.
- **Part tiers gate the buffs.** Magical parts (Elixir) and rare parts
  (Stoneskin) are scarce, so the strong fight-long buffs are naturally
  rate-limited; common parts (Health) are plentiful.

## Balance findings (from `tools/balance_sim.py` + live play)

- With the **natural drop-gated supply**, a player reaches the boss with ~1
  Elixir, 1 Stoneskin, 2 Health. That's a modest safety buffer at the boss
  (~+10 HP), not a free win — every build already beats the boss unaided.
- **The turn-cost makes buff-stacking self-defeating.** Drinking 6 Elixirs is
  *slower and no safer* than drinking 1–2, because each drink-turn is a hit
  taken. There is no degenerate "chug everything" strategy — the optimum is 1–2
  buffs. This is why #2's "costs your turn" rule matters so much.
- **No invulnerability:** Stoneskin floors hits at 1, so even infinite stacks
  can't make you immune. Elixir stacking wastes turns. Infinite Health only lets
  you out-sustain by turning a fight into a slog (tedious, not trivial, and only
  via deliberate grinding).
- **Trash fights are untouched:** a 1–3 turn enemy isn't worth a potion (the
  turn cost dominates), so potions are saved for the boss — exactly where the
  depth belongs.
- On a **medium fight**, an Elixir roughly *breaks even* (the drink-turn offsets
  the damage gain); it only pulls ahead over **long fights** like the boss.
  Confirmed live: a melee build vs. a melee-resisting Slime ended at ~the same
  HP with or without the Elixir.

Conclusion: the system is **self-balancing**. No tuning was needed. If the boss
should stay tense for a fully-prepared player, raise the boss's numbers rather
than nerf potions — but that punishes players who don't craft, so it's not
recommended.

## Roadmap / open ideas

Not yet done; rough priority order:

- **Surface effective damage/defence in the stats screen** — the inventory shows
  raw weapon power, but not the matchup-adjusted, post-mitigation numbers a
  player actually deals/takes. Extends the #1 "make the math visible" theme.
- **A second boss / more encounter variety** — now that the matchup system is
  visible and readable, there's room for an enemy that explicitly checks a
  specific damage type, or a boss with a phase change.
- **More consumable variety** — e.g. an antidote/cleanse if status effects are
  ever added; a throwable that deals flat damage (a ranged option for melee
  builds against their resisted matchups).
- **Status effects** (poison/burn) — would deepen combat further and give
  ranged/magic builds a distinct identity beyond raw numbers.
- **Persist the design loop** — `tools/balance_sim.py` and
  `tests/test_playthrough.py` should be run (and extended) whenever
  `balance.toml` changes; consider wiring them into CI.
