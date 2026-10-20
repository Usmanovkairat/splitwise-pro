import { describe, it, expect, vi } from "vitest";
import { createApiService, ApiError } from "./apiService";
const json = (data: unknown, status = 200) =>
  new Response(JSON.stringify(data), {
    status,
    headers: { "Content-Type": "application/json" },
  });
describe("typed API adapter", () => {
  it("uses the API base and encoded resource identifiers", async () => {
    const fetcher = vi.fn().mockResolvedValue(json([]));
    const api = createApiService("/api/", fetcher);
    expect(await api.listExpenses("g/a")).toEqual([]);
    expect(fetcher).toHaveBeenCalledWith(
      "/api/groups/g%2Fa/expenses",
      expect.objectContaining({ method: "GET" }),
    );
  });
  it("serializes integer minor units and basis points without conversion", async () => {
    const data = {
      description: "Lunch",
      amount_minor: 101,
      payer_id: "m1",
      category: "Food & drinks",
      date: "2026-10-20",
      split_type: "percentage" as const,
      split_values: { m1: 5000, m2: 5000 },
    };
    const fetcher = vi
      .fn()
      .mockResolvedValue(
        json({ ...data, id: "e1", group_id: "g1", shares: [] }, 201),
      );
    const api = createApiService("/api", fetcher);
    await api.createExpense("g1", data);
    expect(fetcher).toHaveBeenCalledWith(
      "/api/groups/g1/expenses",
      expect.objectContaining({
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
      }),
    );
  });
  it("accepts successful 204 deletes without trying to parse JSON", async () => {
    const fetcher = vi
      .fn()
      .mockResolvedValue(new Response(null, { status: 204 }));
    await expect(
      createApiService("/api", fetcher).deleteGroup("g1"),
    ).resolves.toBeUndefined();
  });
  it("keeps creation currency but strips runtime extra fields from group updates (#38)", async () => {
    const fetcher = vi.fn().mockImplementation(() => Promise.resolve(json({})));
    const api = createApiService("/api", fetcher);
    const formData = {
      name: "Almaty weekend",
      description: "Shared travel costs",
      currency: "KZT",
    };
    await api.createGroup(formData);
    await api.updateGroup("g1", formData);
    expect(
      fetcher.mock.calls.map(([url, options]) => ({
        url,
        method: options.method,
        data: JSON.parse(options.body),
      })),
    ).toEqual([
      { url: "/api/groups", method: "POST", data: formData },
      {
        url: "/api/groups/g1",
        method: "PUT",
        data: { name: formData.name, description: formData.description },
      },
    ]);
  });
  it("preserves actionable domain validation errors and status", async () => {
    const fetcher = vi
      .fn()
      .mockResolvedValue(
        json({ detail: "A member with this name already exists." }, 422),
      );
    await expect(
      createApiService("/api", fetcher).addMember("g1", "Alice"),
    ).rejects.toMatchObject({
      name: "ApiError",
      status: 422,
      message: "A member with this name already exists.",
    });
  });
  it("handles structured validation errors and unreadable error responses", async () => {
    const fetcher = vi
      .fn()
      .mockResolvedValueOnce(
        json({ detail: [{ msg: "Amount must be positive" }] }, 422),
      )
      .mockResolvedValueOnce(new Response("Unavailable", { status: 503 }));
    const api = createApiService("/api", fetcher);
    await expect(api.listGroups()).rejects.toThrow("Amount must be positive");
    await expect(api.listGroups()).rejects.toThrow("(503)");
  });
  it("explains network errors without silently falling back to demo data", async () => {
    const fetcher = vi.fn().mockRejectedValue(new TypeError("Failed to fetch"));
    await expect(
      createApiService("/api", fetcher).listGroups(),
    ).rejects.toThrow("backend is running on port 8000");
  });
  it("sends each resource operation to the matching contract endpoint", async () => {
    const fetcher = vi.fn().mockImplementation(() => Promise.resolve(json({})));
    const api = createApiService("/api", fetcher);
    await api.createGroup({ name: "Trip", currency: "USD", description: "" });
    await api.updateGroup("g1", { name: "Home", description: "" });
    await api.listMembers("g1");
    await api.removeMember("g1", "m1");
    await api.balances("g1");
    await api.analytics("g1");
    await api.listSettlements("g1");
    await api.createSettlement("g1", {
      from_member_id: "m1",
      to_member_id: "m2",
      amount_minor: 100,
      date: "2026-10-20",
      note: "",
    });
    const paths = fetcher.mock.calls.map((call) => [call[0], call[1].method]);
    expect(paths).toEqual([
      ["/api/groups", "POST"],
      ["/api/groups/g1", "PUT"],
      ["/api/groups/g1/members", "GET"],
      ["/api/groups/g1/members/m1", "DELETE"],
      ["/api/groups/g1/balances", "GET"],
      ["/api/groups/g1/analytics", "GET"],
      ["/api/groups/g1/settlements", "GET"],
      ["/api/groups/g1/settlements", "POST"],
    ]);
  });
  it("exposes a typed error for callers", () => {
    expect(new ApiError("Validation failed", 422).status).toBe(422);
  });
});
