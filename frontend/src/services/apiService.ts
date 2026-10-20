import type {
  Analytics,
  Balances,
  Expense,
  Group,
  Member,
  Service,
  Settlement,
} from "./types";
export class ApiError extends Error {
  constructor(
    message: string,
    public readonly status: number,
  ) {
    super(message);
    this.name = "ApiError";
  }
}
function detailMessage(detail: unknown): string | undefined {
  if (typeof detail === "string") return detail;
  if (Array.isArray(detail))
    return detail
      .map((item) =>
        typeof item === "object" && item !== null && "msg" in item
          ? String(item.msg)
          : String(item),
      )
      .join("; ");
}
export function createApiService(
  baseUrl = "/api",
  fetcher: typeof fetch = (...args) => fetch(...args),
): Service {
  const base = baseUrl.replace(/\/$/, "");
  async function request<T>(
    path: string,
    method = "GET",
    data?: unknown,
  ): Promise<T> {
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 15000);
    try {
      const response = await fetcher(`${base}${path}`, {
        method,
        signal: controller.signal,
        headers:
          data === undefined
            ? undefined
            : { "Content-Type": "application/json" },
        body: data === undefined ? undefined : JSON.stringify(data),
      });
      if (response.status === 204) return undefined as T;
      const body = await response.json().catch(() => null);
      if (!response.ok)
        throw new ApiError(
          detailMessage(body?.detail) ||
            `The request could not be completed (${response.status}). Please try again.`,
          response.status,
        );
      if (body === null)
        throw new ApiError(
          "The server returned an unreadable response. Please try again.",
          response.status,
        );
      return body as T;
    } catch (error) {
      if (error instanceof ApiError) throw error;
      if (controller.signal.aborted)
        throw new ApiError(
          "The server took too long to respond. Please try again.",
          0,
        );
      throw new ApiError(
        "Cannot reach the local server. Check that the backend is running on port 8000, then try again.",
        0,
      );
    } finally {
      clearTimeout(timeout);
    }
  }
  const group = (id: string) => `/groups/${encodeURIComponent(id)}`;
  return {
    listGroups: () => request<Group[]>("/groups"),
    createGroup: (data) => request<Group>("/groups", "POST", data),
    updateGroup: (id, data) =>
      request<Group>(group(id), "PUT", {
        name: data.name,
        description: data.description,
      }),
    deleteGroup: (id) => request<void>(group(id), "DELETE"),
    listMembers: (id) => request<Member[]>(`${group(id)}/members`),
    addMember: (id, name) =>
      request<Member>(`${group(id)}/members`, "POST", { name }),
    removeMember: (id, memberId) =>
      request<void>(
        `${group(id)}/members/${encodeURIComponent(memberId)}`,
        "DELETE",
      ),
    listExpenses: (id) => request<Expense[]>(`${group(id)}/expenses`),
    createExpense: (id, data) =>
      request<Expense>(`${group(id)}/expenses`, "POST", data),
    updateExpense: (id, expenseId, data) =>
      request<Expense>(
        `${group(id)}/expenses/${encodeURIComponent(expenseId)}`,
        "PUT",
        data,
      ),
    deleteExpense: (id, expenseId) =>
      request<void>(
        `${group(id)}/expenses/${encodeURIComponent(expenseId)}`,
        "DELETE",
      ),
    balances: (id) => request<Balances>(`${group(id)}/balances`),
    listSettlements: (id) => request<Settlement[]>(`${group(id)}/settlements`),
    createSettlement: (id, data) =>
      request<Settlement>(`${group(id)}/settlements`, "POST", data),
    analytics: (id) => request<Analytics>(`${group(id)}/analytics`),
  };
}
export const apiService = createApiService(
  import.meta.env.VITE_API_BASE_URL || "/api",
);
