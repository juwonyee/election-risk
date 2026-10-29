"""Offline tests: run with `python3 -m unittest discover tests` from the repo root."""
import copy
import json
import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "engine"))
from erisk_engine import book, card, compute, markets, report, rerank, universe, validate  # noqa: E402

SO = ROOT / "examples" / "SO"


class Pricing(unittest.TestCase):
    def test_pava_makes_ladder_non_increasing(self):
        self.assertEqual(markets.pava_decreasing([0.6, 0.7, 0.3]), [0.65, 0.65, 0.3])

    def test_midpoint_and_thin(self):
        q = markets._price(0.60, 0.64, 0.5, 4000, "contracts")
        self.assertEqual(q["prob"], 0.62)
        self.assertTrue(q["low_liquidity"])

    def test_unusable_spread_falls_back_to_last_trade(self):
        q = markets._price(0.05, 0.95, 0.4, 20000, "contracts")
        self.assertEqual((q["prob"], q["quote"]), (0.4, "last_trade"))

    def test_race_normalized_and_placeholders_ignored(self):
        ev = {"ladder": False, "markets": [
            {**markets._price(0.48, 0.50, None, 5e5, "USD"), "strike": None},
            {**markets._price(0.53, 0.55, None, 4e5, "USD"), "strike": None},
            {**markets._price(0.0, 1.0, None, 0, "USD"), "strike": None}]}
        out = markets._finish(ev, True)
        self.assertAlmostEqual(sum(m["prob"] for m in out["markets"] if m["prob"] is not None), 1.0, places=3)


class Validate(unittest.TestCase):
    def test_example_is_valid(self):
        mf = json.loads((SO / "markets.json").read_text(encoding="utf-8"))
        self.assertTrue(validate.validate(mf)["ok"])

    def test_missing_formula_is_named(self):
        mf = json.loads((SO / "markets.json").read_text(encoding="utf-8"))
        mf["entries"][0]["impact"]["formula"] = ""
        res = validate.validate(mf)
        self.assertFalse(res["ok"])
        self.assertTrue(any("formula" in e for e in res["errors"]))

    def test_unpriced_type_rejected(self):
        mf = json.loads((SO / "markets.json").read_text(encoding="utf-8"))
        mf["entries"][0]["type"] = "unpriced"
        self.assertFalse(validate.validate(mf)["ok"])


class Compute(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        shutil.copytree(SO, self.tmp / "SO", ignore=shutil.ignore_patterns("results", "report.html", "summary.md"))

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_run_writes_summary_and_report(self):
        ws = self.tmp / "SO"
        data = compute.run(ws)
        self.assertEqual(len(data["results"]), 2)
        self.assertIn("+$660M", (ws / "summary.md").read_text(encoding="utf-8"))
        html = report.build(data)
        self.assertIn("Southern Company", html)
        self.assertNotIn("http://cdn", html)

    def test_falls_back_to_cross_check_venue(self):
        mf = json.loads((SO / "markets.json").read_text(encoding="utf-8"))
        e = copy.deepcopy(next(x for x in mf["entries"] if x["type"] == "race"))
        cc = e["market"]["cross_check"]
        mk = {(cc["source"], t): {"venue": cc["source"], "ticker": t, "prob": 0.5, "low_liquidity": False,
                                  "volume": 1e5, "volume_unit": "USD"} for t in cc["tickers"].values()}
        r, problem = compute.compute_entry(e, mf, mk)
        self.assertIsNone(problem)
        self.assertTrue(any("using Polymarket" in n for n in r["notes"]))


    def test_headline_card_and_red_team(self):
        ws = self.tmp / "SO"
        mf = json.loads((ws / "markets.json").read_text(encoding="utf-8"))
        race = next(x for x in mf["entries"] if x["type"] == "race")
        race["market"]["outcomes"][0].update({"p_policy": 0.45, "route": "make: alone", "source": "https://x.org"})
        (ws / "markets.json").write_text(json.dumps(mf), encoding="utf-8")
        data = compute.run(ws)
        r = next(x for x in data["results"] if x["type"] == "race")
        self.assertAlmostEqual(r["election_swing"], 0.45)
        self.assertEqual(data["headlines"]["election"]["id"], race["id"])
        self.assertIn("<svg", card.build(data))
        self.assertIn("Risk Officer", (ws / "summary.md").read_text(encoding="utf-8"))
        self.assertTrue(any("thin market" in f for f in data["red_team"]))
        b = data["board"]
        self.assertEqual(b["election"]["id"], race["id"])
        self.assertIn("+0.45 if", compute.swing_text(r))
        self.assertEqual([s["analyst"] for s in b["signals"]], ["Exposure", "Policy", "Market", "Red Team"])

    def test_one_off_says_once_in_summary(self):
        ws = self.tmp / "SO"
        mf = json.loads((ws / "markets.json").read_text(encoding="utf-8"))
        mf["entries"][0]["impact"]["one_off"] = True
        (ws / "markets.json").write_text(json.dumps(mf), encoding="utf-8")
        compute.run(ws)
        self.assertIn("+$660M once (", (ws / "summary.md").read_text(encoding="utf-8"))

    def test_no_market_no_card(self):
        self.assertIsNone(card.build({"board": compute.board([], 0, "X")}))

    def test_every_run_ends_in_a_verdict_and_a_card(self):
        data = compute.run(self.tmp / "SO")
        b = data["board"]
        self.assertTrue(all(b[k]["level"] in compute.LEVELS for k in ("election", "policy")))
        self.assertIsNotNone(b["card"])
        self.assertIn("<svg", card.build(data))
        self.assertIn("Save card as PNG", report.build(data))

    def test_verdict_levels_and_reason_below_bar(self):
        def row(kind, share, chance, swing, meaningful):
            r = {"id": kind + str(share), "type": kind, "event_plain": "a law passes", "meaningful": meaningful,
                 "impact": {"central": share * 1e9, "low": 0, "high": 0, "status": "estimated"},
                 "impact_pct": {"central": share, "low": 0, "high": 0}, "chance": chance,
                 "election_swing": swing, "volume": 1e6, "price": {"venue": "Kalshi", "prob": chance}}
            if kind == "race":
                r["outcomes"] = [{"last": "Democrats", "p_policy": 0.05, "price": {"prob": 0.9}},
                                 {"last": "Republicans", "p_policy": 0.0, "price": {"prob": 0.1}}]
            return r
        self.assertEqual(compute.verdict([row("direct", -0.30, 0.08, 0, True)], "policy", "X")["level"], "high")
        self.assertEqual(compute.verdict([row("direct", -0.13, 0.08, 0, True)], "policy", "X")["level"], "medium")
        self.assertEqual(compute.verdict([row("direct", -0.02, 0.08, 0, True)], "policy", "X")["level"], "low")
        self.assertEqual(compute.verdict([], "election", "X")["level"], "no market")
        v = compute.verdict([row("race", 0.15, 0.045, 0.05, False)], "election", "X")
        self.assertTrue(v["below_bar"])
        self.assertIn("only 5% even if Democrats win", v["text"])

    def test_range_flag_only_when_the_verdict_flips(self):
        def row(central, low, high):
            return {"id": "d", "type": "direct", "event_plain": "a law passes.", "meaningful": True,
                    "impact": {"central": central * 1e9, "low": low * 1e9, "high": high * 1e9, "status": "verified"},
                    "impact_pct": {"central": central, "low": low, "high": high}, "chance": 0.10,
                    "election_swing": 0, "volume": 1e6, "price": {"venue": "Kalshi", "prob": 0.10}}
        self.assertEqual(compute.range_flips([row(-0.30, -0.25, -0.90)]), [])  # 3x wide, HIGH throughout
        flips = compute.range_flips([row(-0.30, -0.10, -0.40)])
        self.assertEqual(len(flips), 1)
        self.assertIn("Policy risk HIGH would be MEDIUM at the low end (−$100M) of the impact range for: a law "
                      "passes.", flips[0])
        self.assertNotIn("high end", flips[0])

    def test_unsourced_chance_counts_as_zero(self):
        data = compute.run(self.tmp / "SO")
        self.assertTrue(any("no source link" in f for f in data["red_team"]))
        outs = [o for r in data["results"] if r["type"] == "race" for o in r["outcomes"] if o.get("unsourced")]
        self.assertTrue(outs and all(o["p_policy"] == 0 and o["p_policy_given"] > 0 for o in outs))


class Universe(unittest.TestCase):
    def ev(self, id_, title, close, volume=5000, category="", tags=()):
        return {"id": id_, "title": title, "category": category, "tags": list(tags),
                "outcomes": [{"label": "Yes", "price": 0.5, "volume": volume, "close": close}]}

    def test_us_race_kept_side_and_foreign_dropped(self):
        c = universe.classify
        self.assertEqual(c(self.ev("kalshi:GOVPARTYNY-26", "New York Governor winner?", "2027-11-03",
                                   category="Elections")), "election")
        self.assertIsNone(c(self.ev("kalshi:X", "Kentucky's 1st District margin of victory", "2027-11-03",
                                    category="Elections")))
        self.assertIsNone(c(self.ev("kalshi:Y", "Bulgarian presidential election winner?", "2027-11-15",
                                    category="Elections")))
        self.assertIsNone(c(self.ev("kalshi:Z", "Tiny race", "2027-11-03", volume=10, category="Elections")))

    def test_no_control_characters_in_engine_sources(self):
        # A \b typed into a non-raw string once became a literal backspace and silently disabled 32 patterns.
        for f in (ROOT / "engine" / "erisk_engine").glob("*.py"):
            self.assertNotIn(b"\x08", f.read_bytes(), f.name)

    def test_policy_words_match_whole_words_only(self):
        c = universe.classify
        pol = lambda t, cat="Politics": c(self.ev("kalshi:P", t, "2027-01-04", category=cat))
        self.assertEqual(pol("Will the SAVE Act become law?"), "policy")
        self.assertEqual(pol("Will the FDA approve retatrutide?"), "policy")
        self.assertEqual(pol("Will Trump eliminate capital gains taxes on crypto?"), "policy")
        self.assertEqual(pol("US-Iran nuclear deal?"), "policy")
        self.assertEqual(pol("How many reconciliation bills will become law in 2026?"), "policy")
        self.assertIsNone(pol("Brentford vs Nottingham Forest", "Sports"))
        self.assertIsNone(pol("NHL: EDM Oilers Total Points", "Sports"))
        self.assertIsNone(pol("Sunderland vs Brentford"))
        self.assertIsNone(pol("Will Macron call a referendum?"))
        self.assertEqual(c(self.ev("polymarket:i", "Indiana enacts data center moratorium by...?", "2026-12-31",
                                   tags=("politics",))), "policy")
        self.assertEqual(c(self.ev("polymarket:w", "Weed rescheduled by...?", "2026-12-31",
                                   tags=("pop-culture", "politics"))), "policy")
        self.assertIsNone(c(self.ev("polymarket:b", "Bill Belichick fired?", "2026-12-31", tags=("sports",))))

    def test_us_contests_with_odd_tags_or_close_dates_are_elections(self):
        c = universe.classify
        self.assertEqual(c(self.ev("kalshi:GOVPARTYNM-26", "New Mexico Governor winner? | In 2026", "2027-01-01",
                                   category="Elections")), "election")
        self.assertEqual(c(self.ev("kalshi:KXMAYORLA-26", "Los Angeles Mayor winner? | In 2026", "2027-06-02",
                                   category="Elections")), "election")
        self.assertIsNone(c(self.ev("kalshi:T", "Toronto Mayor winner? | In 2026", "2027-06-02",
                                    category="Elections")))
        self.assertEqual(c(self.ev("polymarket:h", "Which party will win the House in 2026?", "2026-11-03",
                                   tags=("midterms", "global-elections"))), "election")
        self.assertIsNone(c(self.ev("polymarket:r", "Peggy Flanagan runs behind Amy Klobuchar by...?", "2026-11-03",
                                    tags=("midterms",))))

    def test_leaving_a_trade_deal_is_policy_leaving_a_seat_is_not(self):
        c = universe.classify
        self.assertEqual(c(self.ev("kalshi:KXUSMCA-26", "Will Trump try to leave the USMCA?", "2027-01-01",
                                   category="Politics")), "policy")
        self.assertIsNone(c(self.ev("kalshi:A", "Will Cory Mills leave the House?", "2026-11-03",
                                    category="Elections")))
        self.assertIsNone(c(self.ev("kalshi:B", "Will John Fetterman leave the Democratic party?", "2026-11-03",
                                    category="Elections")))

    def test_policy_needs_a_policy_word(self):
        c = universe.classify
        self.assertEqual(c(self.ev("polymarket:a", "Law banning sports prediction markets enacted in 2026",
                                   "2027-01-01", tags=["politics"])), "policy")
        self.assertIsNone(c(self.ev("polymarket:b", "Where will Trump and Putin meet next?", "2027-01-01",
                                    tags=["politics"])))
        self.assertEqual(c(self.ev("polymarket:c", "California Housing Bond Proposition", "2026-11-04",
                                   tags=["politics", "california-midterm"])), "election")


class Book(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        os.environ["ERISK_OUT"] = str(self.tmp)
        (self.tmp / "_markets").mkdir()
        (self.tmp / "_markets" / "elections.md").write_text(
            "# x\n\nkalshi:GOVPARTYCA-26 | California Governor winner? | vol 1,000,000 | closes 2027-11-03 | a\n"
            "kalshi:KXATTYGENGA-26 | Georgia Attorney General winner? | vol 50,000 | closes 2027-11-03 | a\n",
            encoding="utf-8")
        (self.tmp / "_markets" / "house-districts.md").write_text(
            "kalshi:KXHOUSERACE-CA01-26 | CA-01 House winner? | vol 9,000 | closes x | a\n", encoding="utf-8")
        (self.tmp / "_book").mkdir()
        (self.tmp / "_book" / "CA-governor.md").write_text(
            "# California Governor\nMarkets: kalshi:GOVPARTYCA-26, polymarket:ca-gov\n\n## Becerra (D)\n"
            "| Tag | Position | Route | p | Source |\n|---|---|---|---|---|\n"
            "| utilities | Freeze rates | make: same party, strong | 0.35 | https://x.org |\n", encoding="utf-8")

    def tearDown(self):
        os.environ.pop("ERISK_OUT", None)
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_status_find_info(self):
        st = book.status()
        self.assertEqual((st["markets"], st["covered"], st["to_research"]), (2, 1, 1))
        self.assertEqual(book.status(include_house=True)["markets"], 3)
        rows = book.find("utilities", "CA")["rows"]
        self.assertEqual(rows[0]["p"], "0.35")
        self.assertEqual(book.find("utilities", "GA")["count"], 0)
        self.assertTrue(book.SEAT.search("Texas Senate winner? | In 2026"))
        self.assertFalse(book.SEAT.search("Oregon State House winner?"))
        self.assertEqual(book.info()["source"], "built here")

    def test_maintainers_book_keeps_its_build_date(self):
        d = book.book_dir()
        pkg = {"built_by": "election-risk maintainers", "built_on": "2026-01-02", "fingerprint": book.fingerprint()}
        (d / "SOURCE.json").write_text(json.dumps(pkg), encoding="utf-8")  # unzipped by hand
        self.assertEqual((book.info()["source"], book.info()["last_edit"]), ("downloaded", "2026-01-02"))
        (d / "SOURCE.json").write_text(json.dumps({"source": "downloaded", "built_by": pkg}), encoding="utf-8")
        self.assertEqual(book.info()["last_edit"], "2026-01-02")
        next(d.glob("*.md")).write_text("| edited |\n", encoding="utf-8")  # re-researched after download
        self.assertNotEqual(book.info()["last_edit"], "2026-01-02")

    def test_download_needs_consent(self):
        self.assertFalse(book.download(False)["ok"])


class Rerank(unittest.TestCase):
    INDEX = {"built": "test", "events": [
        {"event": "KXLALIGAGAME-DEP", "title": "Atletico vs Deportivo", "sub_title": ""},
        {"event": "KXDEPORTATIONS-27", "title": "Deportations in 2026?", "sub_title": ""},
        {"event": "KXSCOTUSCASE-DHS", "title": "Will SCOTUS rule for DHS on deportations?", "sub_title": ""}]}

    def setUp(self):
        self.saved = (markets.load_index, rerank.http_json, os.environ.get("OPENROUTER_API_KEY"))
        markets.load_index = lambda venue, refresh=False: self.INDEX
        self.calls = []

    def tearDown(self):
        markets.load_index, rerank.http_json, key = self.saved
        if key is None:
            os.environ.pop("OPENROUTER_API_KEY", None)
        else:
            os.environ["OPENROUTER_API_KEY"] = key

    def fake_api(self, scores):
        def post(url, headers=None, body=None, **kw):
            self.calls.append(body)
            qs = body["questions"]
            return {"answers": {k: {"type": "noul", "noul": scores[q["instructions"].split("\n")[0]]}
                                for k, q in qs.items()}, "usage": {"cost": 0.0001}}
        return post

    def search(self):
        return markets.search(["deport"], [], venue="kalshi", about="number of US deportations")

    def test_no_key_keeps_keyword_order_and_calls_nothing(self):
        os.environ.pop("OPENROUTER_API_KEY", None)
        rerank.http_json = self.fake_api({})
        res = self.search()
        self.assertEqual([r["event"] for r in res["results"]], [e["event"] for e in self.INDEX["events"]])
        self.assertNotIn("rerank", res)
        self.assertEqual(self.calls, [])

    def test_key_orders_by_relevance(self):
        os.environ["OPENROUTER_API_KEY"] = "test"
        rerank.http_json = self.fake_api({"Prediction market: Atletico vs Deportivo": 0.02,
                                          "Prediction market: Deportations in 2026?": 0.7,
                                          "Prediction market: Will SCOTUS rule for DHS on deportations?": 0.2})
        res = self.search()
        self.assertEqual([r["event"] for r in res["results"]],
                         ["KXDEPORTATIONS-27", "KXSCOTUSCASE-DHS", "KXLALIGAGAME-DEP"])
        self.assertEqual(res["results"][0]["relevance"], 0.7)
        self.assertEqual(res["rerank"]["scored"], 3)
        self.assertEqual(self.calls[0]["state"], {"topic": "number of US deportations"})

    def test_api_failure_is_a_gap_not_an_error(self):
        os.environ["OPENROUTER_API_KEY"] = "test"

        def broken(*a, **kw):
            raise OSError("no network")
        rerank.http_json = broken
        res = self.search()
        self.assertEqual(len(res["results"]), 3)
        self.assertNotIn("relevance", res["results"][0])
        self.assertEqual(res["gaps"][0]["source"], "OpenRouter (Jev)")

    def test_chunks_requests(self):
        os.environ["OPENROUTER_API_KEY"] = "test"
        rerank.http_json = lambda url, headers=None, body=None, **kw: (
            self.calls.append(body) or {"answers": {k: {"noul": 0.5} for k in body["questions"]}})
        hits = [{"title": f"Market {i}", "sub_title": ""} for i in range(rerank.CHUNK * 2 + 1)]
        ordered, cost = rerank.order("topic", hits)
        self.assertEqual(len(self.calls), 3)
        self.assertEqual(len(ordered), len(hits))
        self.assertEqual(cost, 0.0)


if __name__ == "__main__":
    unittest.main()
