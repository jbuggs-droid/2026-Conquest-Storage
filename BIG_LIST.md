# Big List

## Deferred / Not For Current Pass

- Change the opening video. Current build uses `LoC-Open-3-black.mp4`; future swaps TBD.
- Change text and add music to the pre-game setup menu.
- Set default values for the pre-game menu. Values TBD.
- Add BuggsTech Paradox win condition:
  - Activates in Year 10 in both Normal and Champions modes.
  - Activation is announced by a BLITZ-style banner in the BLITZ lane.
  - Banner copy TBD; draft direction: `BuggsTech Paradox active; conditions primed for surprise win...will you trigger it?`
  - Banner should include the BuggsTech logo somewhere.
  - After Year 10 begins, any player meeting all conditions immediately wins when ending their attack turn:
    - Win five underdog attacks in a row, starting Year 10.
    - Be tied with another player for number of cities, and that tied city count exceeds the Cities to Win value.
    - Have eliminated at least one player.
    - Have given Allies points to ATK, DEF, and Neutral over the course of the game; track from Year 1 if possible.

## Stabilization Notes

- Completed: Route delegated End Trade through `beginShippingPhase()` so AI Shipping turns start automatically.
- Completed: Add missing Development / Board Review / Victory phase help fallbacks to prevent Phase Guidance runtime errors.
- Completed: Harden Return to Setup cleanup for phase, overlays, shipping state, attack overlays, production timers, and trade AI timers.
- Completed: Standard banners now use rev266-style map anchoring; toplane/middlelane follow the map area during window scroll.
- Completed: BLITZ banner keeps the GLORIOUSLY OBNOXIOUS treatment but now constrains itself to the map window's horizontal borders.
- Completed: Standard banners now use the rev266 injected v85 skin: small gold kicker title, large cream subtitle, full gold border, and dark gold gradient Continue button. BLITZ and dedication remain custom.
- Completed: BLITZ and Dedication Continue buttons now use the v85 button treatment while keeping their custom banner bodies.
- Completed: Saved reusable v85 banner/button reference CSS as `v85-banner-skin-reference.css`; side-by-side comparison remains in `banner-style-comparison.html`.
- Completed: Attack suspense uses the war quote pool in toplane; ordinary phase/year/placement announcements route to middlelane unless explicitly marked otherwise.
- Completed: Year handoff now leaves Attack immediately via `yearTransition`, hiding attack controls before Year 2 Development begins.
- Completed: Bomb-run video asset is present in the workspace as `bomb run with audio.mp4`; the HTML source already points to it.
- Completed: Bomb runs can launch through the committed ATTACK path even when normal ATT math is 0, so non-adjacent valid enemy targets are not blocked by the no-zero normal attack rule.
- Completed: Stockpile-destroying bomb runs set the bomber cooldown and terminal turn state before forced stockpile relocation, so the turn should end after relocation completes.
- Completed: Factory is now a valid bomb-run target in the 5-6 band with Stockpile; if both are present, the hit target is chosen 50/50.
- Completed: Bomb-run result banners now include `Factory destroyed.` and surviving bomber cooldown until `Year N`.
- Completed: Add Year indicator beside the ATT vs DEF force readout in the Attack panel.
- Completed: Normal attacks no longer auto-select or require a hidden source territory.
- Completed: Captured defender mobile units transfer with the territory by default; no new attacker mobile units appear unless a current Bring Forces committed package exists.
- Completed: Bring Forces committed units now land on a conquered territory only after the attack result banner is dismissed; if the attack loses, the already-committed units stay destroyed.
- Completed: Bring Forces win replaces duplicate defender mobile unit types only for the units brought; unrelated defender mobile units transfer.
- Completed: Naval Bring Forces now moves the committed boat's docked-coast bookkeeping from source to conquered territory on a win, instead of leaving a phantom boat at origin.
- Completed: Shipping boat moves now update the same docked-coast bookkeeping, keeping visible boat docks aligned with boat inventory counts.
- Completed: Boat rendering/docking now uses adjacent water tiles, not naval land-neighbor links, so boats should not render on land and successful naval attacks should dock on the coast nearest the attack approach.
- Completed: Stockpile markers are preserved during battle suspense for pending stockpile captures, preventing the stockpile icon from disappearing early and spoiling the attack outcome.
- Completed: End Conquest / End Attack Turn now requires an `End Conquest?` confirmation banner before the turn is actually ended.
- Completed: Endgame victory sequence now runs game-ending BLITZlane banner -> BLITZlane Lord of Conquest fanfare banner -> BLITZlane tribute picker -> regular middlelane Thanks banner -> under-map Back to Menu button.
- Completed: Victory audio assets copied into workspace as `LoC-winning-Fanfare.mp3`, `LoC-80s-tears-for-fears.wav`, and `LoC-80s-wav-ending-tribute.wav`.
- Completed: Setup/menu title changed to `Conquest 2026`, demo-interactions copy removed, and `LoC-80s-play-at-your-own-risk.wav` copied into workspace as setup-menu loop music.
- Completed: Intro dismissal/end now starts the setup-menu music loop, and entering Territory Selection fades it down over one second before stopping it.
- Completed: Preserved C64 map names/order in `MAP_ASSET_MANIFEST.md`; rough photo assets removed.
- Completed: Map implementation policy locked: digital source guides geometry, C64 names stay, generated maps produce thumbnails, and maps appear in setup only after playable geometry exists.
- Completed: Ingested clean digital C64 screenshots for all 20 maps into `map-sources/digital/`.
- Completed: Generated playable geometry for all 20 C64 maps in `generated/c64-generated-maps.js`, with a standalone preview at `generated/c64-map-preview.html`.
- Completed: Setup map selector now includes the generated C64 map names and prefers generated geometry over the earlier rough `N America 1` wiring pilot.
- Completed: Setup map thumbnail window is implemented in the right setup pane and renders from generated/playable map geometry, not source screenshots.
- Completed: Added setup option `AI Style: Normal / Aggressive!`.
- Completed: Added high-z under-map AI action panel that appears only while AI is active and hides the normal Attack/Development controls during AI turns.
- Completed: Added first-pass Development AI: it considers resources, territory threat pressure, Champions caps, and AI style, then builds one useful asset or passes.
- Completed: Added first-pass Attack AI: it evaluates legal targets, Bring Forces packages, confidence level, Normal vs Aggressive thresholds, then calls the existing attack engine for resolution.
- Completed: Winning Fanfare is unskippable in code and locks the Victory Continue button until completion; tribute tracks unlock Skip Tribute after 10 seconds.
- Completed: Fixed post-victory attack flow leak: result-banner landing callback is in scope, and map clicks in armed Attack/planning mode now preview targets instead of resolving attacks. Normal attacks resolve only from the ATTACK button.
- Completed: Champions force count values set to Bomber +0, Flak/AA +1, Factory +1.
- Completed: Force Inspector shows Champions-only rows for Bomber, AA/Flak, Factory, and Factory Output while in Champions mode.
- Completed: AI flow policy locked in: AI-to-AI Trade/Shipping continues automatically; AI-to-human Shipping handoff and pending AI-to-human Trade proposals use blocking middlelane handoff banners.
- Watch: Several duplicate IDs still appear in static analysis because some IDs exist both in the original HTML shell and in later `innerHTML` templates. They did not produce browser errors in the smoke pass, but this should be revisited during a larger refactor.
- Watch: Champion announcement still needs the separate design/content pass the user called out.
- Watch: Generated C64 map geometry needs browser/playtest validation for territory counts, adjacency feel, and naval coastline behavior.
- Watch: New Development/Attack AI needs playtest validation across Normal and Champions modes, especially naval Bring Forces choices and post-result continuation timing.
- Watch: Victory audio should be smoke-tested in browser because browser autoplay policy may still block playback if a victory is triggered without recent user interaction.
