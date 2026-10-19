import { describe, it, expect } from "vitest";
import { calculateShares, createMockService } from "./mockService";
describe("mockService financial behavior", () => {
  it("allocates an uneven cent deterministically by member id", () => {
    expect(calculateShares(100, { c: 1, b: 1, a: 1 }, "equal")).toEqual([
      { member_id: "a", amount_minor: 34 },
      { member_id: "b", amount_minor: 33 },
      { member_id: "c", amount_minor: 33 },
    ]);
  });
  it("rejects exact and percentage totals that do not match", () => {
    expect(() => calculateShares(100, { a: 99 }, "exact")).toThrow("Exact");
    expect(() => calculateShares(100, { a: 9999 }, "percentage")).toThrow(
      "100%",
    );
  });
  it("keeps balance sum zero after a partial settlement", async () => {
    const s = createMockService();
    const b = await s.balances("g1");
    expect(b.members.reduce((n, m) => n + m.net_minor, 0)).toBe(0);
    const suggestion = b.suggestions[0];
    await s.createSettlement("g1", {
      ...suggestion,
      amount_minor: 1,
      date: "2026-10-20",
      note: "",
    });
    const next = await s.balances("g1");
    expect(next.members.reduce((n, m) => n + m.net_minor, 0)).toBe(0);
    expect(
      next.members.find((m) => m.member_id === suggestion.from_member_id)!
        .net_minor,
    ).toBe(
      b.members.find((m) => m.member_id === suggestion.from_member_id)!
        .net_minor + 1,
    );
  });
  it("protects historical participants from removal and supports group cascades", async () => {
    const s = createMockService();
    await expect(s.removeMember("g1", "m1")).rejects.toThrow("activity");
    await s.deleteGroup("g1");
    await expect(s.listExpenses("g1")).rejects.toThrow("not found");
  });
  it("supports exact and basis-point percentage splitting", () => {
    expect(
      calculateShares(101, { a: 3000, b: 7000 }, "percentage").reduce(
        (n, s) => n + s.amount_minor,
        0,
      ),
    ).toBe(101);
    expect(
      calculateShares(101, { a: 50, b: 51 }, "exact")[1].amount_minor,
    ).toBe(51);
  });
});
describe("regression #37: per-group Unicode member uniqueness", () => {
  it("trims names, rejects case-fold equivalents, allows names in other groups", async () => {
    const s = createMockService();
    const first = await s.addMember("g1", " Straße ");
    expect(first.name).toBe("Straße");
    await expect(s.addMember("g1", " STRASSE ")).rejects.toThrow(
      "already exists",
    );
    await expect(s.addMember("g1", "straße")).rejects.toThrow("already exists");
    expect(
      (await s.listMembers("g1")).filter((m) => m.name === "Straße"),
    ).toHaveLength(1);
    await expect(s.addMember("g2", "STRASSE")).resolves.toMatchObject({
      name: "STRASSE",
    });
    await expect(s.addMember("g1", "   ")).rejects.toThrow("required");
  });
});
