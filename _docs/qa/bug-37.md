# Independent QA issue37

Memory segment PASS. Independently executed pytest:27 passed,1 deprecation warning,0.80s. Independent TestClient scenario confirmed Alice201 then alice/paddedALICE422, string detail response, member count and original ID unchanged; Straße201 then STRASSE422; separate group Alice201. Backend fix may be published separately before ORM stage.

Full issue remains pending SQLite/restart and integrated dialog verification. Mock Unicode behavior is handled separately by frontend author; no unexecuted parity claim.

Frontend segment PASS: independent `npm test` after Unicode case-folding change:10 tests passed,2 files,3.00s. Reviewed mock regression: trimmed Straße then STRASSE/straße rejected without extra member; other group STRASSE accepted; whitespace rejected. Unicode case folding dependency is pinned in package lock.

SQLite/restart segment PASS: independent fresh migrated temporary database created Straße, engine disposed/reconstructed against same file, padded STRASSE422 and original member ID/list retained. Full backend suite53 passed. Integrated active-dialog duplicate segment pending stage5.
