# LoC Handoff

## Workspace

- Main working file: `/Users/julianbuggs/Documents/Codex/2026-04-26/analyze-the-the-attached-file-look/LoC-ultimate-rev1.html`
- Big List: `/Users/julianbuggs/Documents/Codex/2026-04-26/analyze-the-the-attached-file-look/BIG_LIST.md`
- Banner sample: `/Users/julianbuggs/Documents/Codex/2026-04-26/analyze-the-the-attached-file-look/banner-lanes-sample.html`
- Intro video: `/Users/julianbuggs/Documents/Codex/2026-04-26/analyze-the-the-attached-file-look/LoC-Open-3-black.mp4`
- Bomb-run video: `/Users/julianbuggs/Documents/Codex/2026-04-26/analyze-the-the-attached-file-look/bomb run with audio.mp4`
- Map name/order manifest: `/Users/julianbuggs/Documents/Codex/2026-04-26/analyze-the-the-attached-file-look/MAP_ASSET_MANIFEST.md`
- Extracted reference docs: `/Users/julianbuggs/Documents/Codex/2026-04-26/analyze-the-the-attached-file-look/extracted_docs/`

Do not edit the original Downloads files unless Julian explicitly asks. The workspace copy is the build target.

## Source Of Truth

- `LoC refactor in Cursor.docx` is the primary roadmap/source of truth.
- `Conquest 2026.docx` is secondary.
- If docs/spec and current code conflict, ask before changing behavior.

## Current User Decisions

- Dedication runs before intro video.
- Intro video is `LoC-Open-3-black.mp4`.
- Bomb-run video is `bomb run with audio.mp4`.
- All standard banners are center-justified, including Shipping.
- Board Review is the unified flow: tile resource cycling plus up to 3 random redistributes, then Proceed to Territory Selection.
- Manual Resource Edit in setup is removed.
- Old top/header Redistribute Resources button is removed.
- Boat/illegal coast rule is not finalized: force-move to nearest legal coast; destroy only if a duplicate is accidentally made. Need definition of nearest legal coast before implementing.
- Debug output should remain visible during testing.

## Completed Patches

- Stabilized global/lexical bridges for later script blocks:
  - `tradeOffers`, `tradeNextOfferId`, `players`, `territories`, `roundNum`, `phase`, `attackState`, `developmentState`, `attackMode`, `attackSourceIdx`, `selected`, `turnOrder`, `currentPlayerId`, `shippingState`, `attackShippingState`, `shippingMoved`.
- Added `showToast` alias.
- Added dedication overlay before intro, with Julian's special thanks text.
- Updated intro source to `LoC-Open-3-black.mp4`.
- Added Board Review panel and flow.
- Standard banner system:
  - Rev266-style map-anchored standard banners.
  - Toplane aligns to map top edge.
  - Middlelane centers within map area.
  - Standard banners reposition on scroll, resize, and interval.
  - Standard banners use the rev266 injected v85 skin: small gold kicker title, large cream subtitle, full gold border, and dark gold gradient Continue button.
  - BLITZ and Dedication retain their custom banner bodies but share the v85 Continue button treatment.
  - Reference files: `banner-style-comparison.html` and `v85-banner-skin-reference.css`.
  - Special BLITZ banner remains separate but is constrained to the horizontal borders of the map window.
- Setup/menu:
  - Browser/page title and visible top title now read `Conquest 2026`.
  - Demo-interactions copy block removed from the setup screen.
  - `LoC-80s-play-at-your-own-risk.wav` copied into workspace as `LoC-80s-play-at-your-own-risk.wav`.
  - Intro movie dismissal/end starts the setup-menu music loop; entering Territory Selection fades it down over one second, then stops/resets it.
  - Rough C64 photo assets were removed from the workspace; map order/names are preserved in `MAP_ASSET_MANIFEST.md`.
  - Map policy: incoming digital source guides playable geometry; menu thumbnails should be generated from completed playable maps; keep C64 names; show maps in setup only after geometry is playable.
  - `N America 1` pilot is now a rough playable setup map option using hand-authored C64-style region geometry.
  - `N America 1` uses explicit water regions and a shared region-grid builder so land adjacency and coastal water adjacency are generated from the same geometry.
  - All 20 C64 map names now have generated digital map geometry/thumbnail data in `generated/c64-generated-maps.js`.
  - Setup now shows a map thumbnail preview in the right setup pane for generated C64 maps.
  - Setup now includes `AI Style: Normal / Aggressive!`.
- AI:
  - Added a high-z under-map `AI Action` panel. It appears when AI is active and hides the normal Attack/Development controls beneath it; it disappears again on human turns.
  - Added first-pass Development AI. It evaluates owned territory, threat pressure, available resources, and Champions caps, then builds one useful asset or passes. It narrates the build in the under-map AI panel and uses brief toplane quotes.
  - Added first-pass Attack AI. It evaluates legal targets, optional Bring Forces packages, normal vs `Aggressive!` thresholds, and confidence (`high`, `medium`, `low`, `longshot`). It commits Bring Forces through the existing combat state, then calls the existing `resolveAttack()` engine so battle outcome, repaint, item disposition, and result banners remain centralized.
  - `Aggressive!` is global: it favors riskier attacks, more Bring Forces use, and more attack-oriented development choices.
- Added standalone banner sample: `banner-lanes-sample.html`.
- Attack suspense:
  - Uses toplane.
  - Randomly selects from original `WAR_QUOTES` plus rev266 `EXTRA_ATTACK_QUOTES`.
- Phase/year/placement/result standard banners route to middlelane unless explicitly passed `lane: "top"`.
- Trade:
  - AI Trade sequence starts on Trade phase.
  - Human-to-AI direct trade cannot be forced by clicking both sides; AI now evaluates offer.
  - AI-to-human Accept/Reject panel appears only when there is an active proposal.
  - AI-to-AI trade steps are automatic; if AI negotiation creates pending AI-to-human proposals, a middlelane `AI Trade Complete!` handoff banner blocks until Continue/Enter.
- Shipping:
  - Delegated End Trade now enters Shipping through `beginShippingPhase()`.
  - AI Shipping calls refined `window.aiTakeOneShippingMove()` path and has fallback pass-through to avoid hangs.
  - AI-to-AI Shipping turns auto-advance; when an AI finishes and the next Shipping player is human, a middlelane `AI Shipping Complete!` banner blocks until Continue/Enter.
  - Boat moves now update `dockedBoats` together with `items.boats`, preventing stale coast markers/phantom boats after a boat sails.
- Year handoff:
  - End of Year 1 now enters `yearTransition`, hides Attack controls, then proceeds to Year 2 Development after banner.
- Bombing:
  - `bomb run with audio.mp4` copied into the workspace next to the HTML.
  - Bombing target math is present: valid enemy targets are flak, city, bomber, factory, or defender stockpile; hit bands are 1-2 bomber/flak, 3-4 city, 5-6 stockpile/factory, with invalid bands rerolled/fallbacked.
  - If both stockpile and factory exist in the 5-6 band, the hit target is chosen 50/50.
  - Committed bomber launches bypass the normal ATT=0 lockout, so non-adjacent valid bombing targets can proceed.
  - Stockpile bomb runs now set terminal attack state before forced stockpile relocation so the player's turn should end after relocation.
  - Bomb-run result banners include factory destruction and surviving bomber cooldown until `Year N`.
- Champions force count values:
  - Bomber: +0
  - Flak/AA: +1
  - Factory: +1
- Force Inspector in Champions mode shows Bomber, AA/Flak, Factory, and Factory Output rows for selected land territories.
- Attack panel now shows `Year N` beside the ATT vs DEF force readout.
- Attack source leak fix:
  - Normal attacks no longer auto-select, require, or store a hidden source territory.
  - Captured defender boats/horses/weapons transfer with the territory by default.
  - The only way boats/horses/weapons land in a conquered territory is a current Bring Forces committed package.
  - Committed Bring Forces units are removed at commit time, destroyed on loss, and applied to the captured territory only after the result banner is dismissed on a win.
  - On a Bring Forces win, duplicate defender mobile unit types matching the brought units are replaced; unrelated defender units transfer.
  - Naval Bring Forces carries the committed boat's dock bookkeeping from source to the captured territory. On win the boat redocks at the conquered coast; on loss the already-removed boat stays destroyed.
  - Boat dock/render helpers now use adjacent water tiles from `allNeighbors`, not `navalNeighbors` land links. This prevents boats from rendering on land and selects a target coast nearest the attack approach where possible.
  - Pending stockpile-capture markers are held through battle suspense so a stockpile icon does not disappear before the result banner reveals the attack outcome.
  - Stale `invadeSourceIdx`, `invadeOverride`, `invadeDelta`, and `invadeCommittedFor` are cleared when a normal non-committed attack resolves.
  - Result-banner committed landing callback is now hoisted so Continue does not throw `applyCommittedLanding is not defined`.
  - Territory clicks in armed Attack/planning mode now only preview/select targets; normal attack resolution is gated to the ATTACK button.
- End Conquest / End Attack Turn now routes through a middlelane `End Conquest?` confirmation banner with `End Conquest` and `Keep Fighting` buttons.
- Return to Setup cleanup hardened for overlays, phase, shipping state, attack overlays, trade AI timers, and production timers.
- Phase Guidance updated for Board Review, Development, Victory, and Year Transition.
- Victory sequence:
  - Audio assets copied into workspace: `LoC-winning-Fanfare.mp3`, `LoC-80s-tears-for-fears.wav`, `LoC-80s-wav-ending-tribute.wav`.
  - Game-ending banner appears first in BLITZ style / BLITZ lane, Continue-only.
  - Victory banner text: `A Lord of Conquest has been proclaimed!`
  - Victory banner uses BLITZ style / BLITZ lane, plays `LoC-winning-Fanfare.mp3`, and locks Continue until the fanfare ends.
  - Victory Continue opens BLITZlane tribute picker: `(winner), pick your musical tribute.`
  - Tribute buttons: `80s tribute` -> `LoC-80s-tears-for-fears.wav`; `Classic tribute` -> `LoC-80s-wav-ending-tribute.wav`.
  - Tribute skip unlocks after 10 seconds; skip/completion shows regular middlelane `Thanks for playing!` with a normal `Continue` button. Continue clears the banner and reveals an under-map `Back to Menu` button.
  - Browser smoke needed: verify audio starts under real victory conditions; autoplay policy can still block playback if victory is reached without a recent user gesture.

## Verification So Far

- Main HTML parse check: 11 scripts, 0 syntax errors.
- Main HTML parse check after victory-sequence patch: 11 scripts, 0 syntax errors.
- Main HTML parse check after End Conquest / stockpile suspense / boat dock patch: 11 scripts, 0 syntax errors.
- Main HTML script-block parse check after AI style / Development AI / Attack AI patch: 12 scripts, 0 syntax errors.
- Bomb-run video asset confirmed present in workspace.
- Banner sample parse check: 1 script, 0 syntax errors.
- Browser smoke passed after stabilization:
  - reload
  - dedication
  - intro skip
  - setup confirm
  - Board Review
  - Proceed to Territory Selection
  - no workspace console errors
- Banner sample opened in browser with no sample-file console errors.
- Rough map photo assets deleted from `map-sources/`; map names/order remain in `MAP_ASSET_MANIFEST.md`.
- Clean digital C64 map screenshots ingested into `map-sources/digital/` for all 20 original map names.
- Generated playable geometry for all 20 C64 maps:
  - Source script: `scripts/extract_c64_maps.py`
  - Runtime data: `generated/c64-generated-maps.js`
  - Standalone preview: `generated/c64-map-preview.html`
- Main game now loads `generated/c64-generated-maps.js`; setup map selector includes the generated C64 map names and prefers generated geometry when selected.
- Menu music fade parse check: setup music now fades on Territory Selection entry instead of cutting off immediately.
- `N America 1` pilot map parse check: main HTML still parses 11 inline scripts with 0 syntax errors.

## Current Watch Items

- Need a new playthrough validation of Year 1 -> Year 2 after the latest year-transition patch.
- Need a reload/new playthrough to validate the latest bomber patches; the currently open browser state predates these code edits unless reloaded.
- Confirm that stockpile forced relocation after a bomb run advances to the next player/phase after Continue.
- Verify the attack source/mobile capture fix in a fresh reload: normal AI/human attack win should inherit defender horse/weapon/boat, and should not create extra attacker units unless Bring Forces was explicitly committed.
- Verify after reload that a player cannot trigger Attack 2/3 by clicking enemy territories in planning/preview mode; clicks should update preview only until ATTACK is pressed.
- Verify after reload that successful boat attacks move the source boat to the conquered coast, and failed boat attacks destroy the committed boat/cargo without leaving an origin duplicate.
- Verify after reload that boat icons never render on land and conquered boats dock on the coast nearest the naval approach.
- Verify after reload that stockpile markers remain visible during battle suspense, then disappear only with the revealed stockpile-looted result.
- Verify after reload that End Conquest cancellation keeps the current attack turn active.
- Champion announcement still needs design/content work.
- Duplicate IDs appear in static analysis because some IDs exist in both original shell and later `innerHTML` templates. No observed smoke-test errors, but refactor later.
- AI-to-human offers exist only if AI conditions produce an offer. If the user expects more frequent offers, tune `aiMakeOneOffer`.
- Boat forced-coast relocation still needs rules detail.
- Banner content/lane spec is not fully enumerated yet; Julian will provide exact lane content later.
- Pre-game menu updates deferred:
  - change opening video
  - change setup text/add music
  - set default values, values TBD
- Map selector thumbnail work is still deferred:
  - generate/attach setup thumbnails from generated geometry
  - right-column thumbnail should align with the map option row
  - thumbnail width should match the right column, height should be 1.5x standard banner height
- Generated C64 maps need browser/playtest validation:
  - confirm territory count/feel
  - confirm adjacency feels faithful
  - confirm coastline and boat docking behavior
  - tune extraction radius/script if a specific map has bad adjacency

## Recommended Next Steps

1. Reload the main workspace HTML.
2. Play through Year 1 again and specifically verify:
   - last attacker losing first attack ends that attack turn
   - if that was the last attacker, Attack UI disappears
   - Year 2 banner appears in middlelane
   - Development panel appears after Continue
3. Verify banner scroll behavior:
   - toplane suspense quote follows map top while scrolling
   - middlelane phase/result banners follow map area while scrolling
4. Then move to champion announcement polish or boat forced-coast relocation once rules are clarified.
