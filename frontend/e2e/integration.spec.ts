import {
  test as base,
  expect,
  type Page,
  type APIRequestContext,
} from "@playwright/test";

const api =
  (process.env.QA_BASE_URL || "http://127.0.0.1:8000").replace(/\/$/, "") +
  "/api";
type Ledger = {
  id: string;
  members: { id: string; name: string }[];
  url: string;
};
const test = base.extend<{ ledger: Ledger }>({
  ledger: async ({ request }, use, info) => {
    const response = await request.post(`${api}/groups`, {
      data: {
        name: `QA ${info.testId}`,
        currency: "USD",
        description: "Isolated browser acceptance fixture",
      },
    });
    expect(response.ok()).toBeTruthy();
    const group = await response.json();
    const members = [];
    try {
      for (const name of ["Alice", "Bob", "Carol"]) {
        const member = await request.post(`${api}/groups/${group.id}/members`, {
          data: { name },
        });
        expect(member.ok()).toBeTruthy();
        members.push(await member.json());
      }
      await use({ id: group.id, members, url: `${api}/groups/${group.id}` });
    } finally {
      await request.delete(`${api}/groups/${group.id}`);
    }
  },
});
async function visit(page: Page, ledger: Ledger, path?: string) {
  await page.goto(`/groups/${ledger.id}`);
  await expect(
    page.getByRole("button", { name: "Remove Alice" }),
  ).toBeVisible();
  if (path) {
    await page.getByRole("link", { name: path, exact: true }).click();
  }
}
async function seed(
  request: APIRequestContext,
  ledger: Ledger,
  description = "Dinner",
  category = "Food & drinks",
) {
  const response = await request.post(`${ledger.url}/expenses`, {
    data: {
      description,
      amount_minor: 1200,
      payer_id: ledger.members[0].id,
      category,
      date: "2026-10-20",
      split_type: "equal",
      split_values: Object.fromEntries(ledger.members.map((m) => [m.id, 1])),
    },
  });
  expect(response.ok()).toBeTruthy();
  return response.json();
}
async function expenseDialog(
  page: Page,
  title = "Browser lunch",
  amount = "12.00",
) {
  await page.getByRole("button", { name: "Add expense", exact: true }).click();
  const dialog = page.getByRole("dialog");
  await dialog.getByLabel("What was it for?").fill(title);
  await dialog.getByLabel("Amount (USD)", { exact: true }).fill(amount);
  await dialog.getByLabel("Paid by").selectOption({ label: "Alice" });
  return dialog;
}

test("group creation starts an empty workspace and persists after refresh", async ({
  page,
  request,
}) => {
  let id: string | undefined;
  try {
    await page.goto("/groups");
    await page.getByRole("button", { name: "New group", exact: true }).click();
    await expect(
      page.getByRole("button", { name: "Create group", exact: true }),
    ).toBeDisabled();
    await page.getByLabel("Group name").fill("   ");
    await expect(
      page.getByRole("button", { name: "Create group", exact: true }),
    ).toBeDisabled();
    await page.getByLabel("Group name").fill("Browser-created group");
    await page.getByLabel("Group currency").selectOption("USD");
    await page
      .getByRole("button", { name: "Create group", exact: true })
      .click();
    await expect(page.getByRole("dialog")).toHaveCount(0);
    await page.getByRole("button", { name: /Browser-created group/ }).click();
    id = new URL(page.url()).pathname.split("/").pop();
    await page.reload();
    await expect(
      page.getByRole("heading", { name: "Browser-created group", exact: true }),
    ).toBeVisible();
    await expect(
      page.getByText("Good company starts here", { exact: true }),
    ).toBeVisible();
  } finally {
    if (id) await request.delete(`${api}/groups/${id}`);
  }
});
test("group editing persists the name and description", async ({
  page,
  ledger,
}) => {
  await visit(page, ledger);
  await page.getByRole("button", { name: "Edit group", exact: true }).click();
  await expect(page.getByLabel("Group currency")).toBeDisabled();
  await page.getByLabel("Group name").fill("   ");
  await expect(
    page.getByRole("button", { name: "Save changes", exact: true }),
  ).toBeDisabled();
  await page.getByLabel("Group name").fill("Renamed isolated group");
  await page.getByLabel("A little description").fill("Updated description");
  await page.getByRole("button", { name: "Save changes", exact: true }).click();
  await expect(page.getByRole("dialog")).toHaveCount(0);
  await page.reload();
  await expect(
    page.getByRole("heading", { name: "Renamed isolated group", exact: true }),
  ).toBeVisible();
  await expect(
    page.getByText("Updated description", { exact: true }),
  ).toBeVisible();
});
test("group deletion supports cancellation and removes the group", async ({
  page,
  ledger,
  request,
}) => {
  await visit(page, ledger);
  page.once("dialog", (d) => d.dismiss());
  await page.getByRole("button", { name: "Delete group", exact: true }).click();
  expect((await request.get(ledger.url)).ok()).toBeTruthy();
  page.once("dialog", (d) => d.accept());
  await page.getByRole("button", { name: "Delete group", exact: true }).click();
  await expect
    .poll(async () => (await request.get(ledger.url)).status())
    .toBe(404);
});
test("member creation rejects normalized duplicates and allows unreferenced removal", async ({
  page,
  ledger,
}) => {
  await visit(page, ledger);
  for (const name of ["Dave", "  ALICE  "]) {
    await page.getByRole("button", { name: "Add member", exact: true }).click();
    await page.getByLabel("Member name").fill(name);
    await page
      .getByRole("dialog")
      .getByRole("button", { name: "Add member", exact: true })
      .click();
    if (name === "Dave") await expect(page.getByRole("dialog")).toHaveCount(0);
    else {
      await expect(page.getByRole("dialog").getByRole("alert")).toBeVisible();
      await page.keyboard.press("Escape");
    }
  }
  page.once("dialog", (d) => d.accept());
  await page.getByRole("button", { name: "Remove Dave" }).click();
  await expect(page.getByRole("button", { name: "Remove Dave" })).toHaveCount(
    0,
  );
});
test("member referenced by expense cannot be removed", async ({
  page,
  request,
  ledger,
}) => {
  await seed(request, ledger);
  await visit(page, ledger);
  page.once("dialog", (d) => d.accept());
  await page.getByRole("button", { name: "Remove Alice" }).click();
  await expect(page.getByRole("alert")).toContainText("referenced");
  await expect(
    page.getByRole("button", { name: "Remove Alice" }),
  ).toBeVisible();
});
for (const method of ["Equally", "Exact amounts", "Percentages"]) {
  test(`expense creation with ${method} stores exact shares and rounding`, async ({
    page,
    request,
    ledger,
  }) => {
    await visit(page, ledger);
    const dialog = await expenseDialog(page, "Split test", "1.00");
    await dialog.getByRole("button", { name: method, exact: true }).click();
    if (method === "Equally") {
      for (const name of ["Alice", "Bob", "Carol"])
        await dialog
          .locator(".split-person")
          .filter({ hasText: name })
          .getByRole("checkbox")
          .uncheck();
      await dialog
        .getByRole("button", { name: "Add expense", exact: true })
        .click();
      await expect(dialog.getByRole("alert")).toContainText(
        "at least one participant",
      );
      for (const name of ["Alice", "Bob", "Carol"])
        await dialog
          .locator(".split-person")
          .filter({ hasText: name })
          .getByRole("checkbox")
          .check();
    } else {
      for (const name of ["Alice", "Bob", "Carol"])
        await dialog
          .getByLabel(
            `${name} ${method === "Exact amounts" ? "share" : "percentage"}`,
          )
          .fill("0");
      await dialog
        .getByRole("button", { name: "Add expense", exact: true })
        .click();
      await expect(dialog.getByRole("alert")).toContainText(
        method === "Exact amounts" ? "Exact shares must equal" : "100%",
      );
      expect(
        await (await request.get(`${ledger.url}/expenses`)).json(),
      ).toEqual([]);
    }
    if (method !== "Equally")
      for (const [i, name] of ["Alice", "Bob", "Carol"].entries())
        await dialog
          .getByLabel(
            `${name} ${method === "Exact amounts" ? "share" : "percentage"}`,
          )
          .fill(
            method === "Exact amounts"
              ? ["0.34", "0.33", "0.33"][i]
              : ["50", "25", "25"][i],
          );
    await dialog
      .getByRole("button", { name: "Add expense", exact: true })
      .click();
    await expect(dialog).toHaveCount(0);
    await expect(
      page.getByRole("button", { name: "Edit Split test" }),
    ).toBeVisible();
    const expenses = await (await request.get(`${ledger.url}/expenses`)).json();
    expect(expenses).toHaveLength(1);
    expect(
      expenses[0].shares.reduce(
        (sum: number, share: any) => sum + share.amount_minor,
        0,
      ),
    ).toBe(100);
    expect(
      expenses[0].shares
        .map((share: any) => share.amount_minor)
        .sort((a: number, b: number) => a - b),
    ).toEqual(method === "Percentages" ? [25, 25, 50] : [33, 33, 34]);
  });
}
test("expense editing updates browser and server", async ({
  page,
  request,
  ledger,
}) => {
  await seed(request, ledger);
  await visit(page, ledger);
  await page.getByRole("button", { name: "Edit Dinner" }).click();
  await page.getByLabel("What was it for?").fill("Edited dinner");
  await page.getByLabel("Amount (USD)", { exact: true }).fill("-1");
  await page.getByRole("button", { name: "Save changes", exact: true }).click();
  await expect(page.getByRole("dialog").getByRole("alert")).toContainText(
    "positive amount",
  );
  expect(
    (await (await request.get(`${ledger.url}/expenses`)).json())[0]
      .amount_minor,
  ).toBe(1200);
  await page.getByLabel("Amount (USD)", { exact: true }).fill("15.00");
  await page.getByRole("button", { name: "Save changes", exact: true }).click();
  await expect(page.getByRole("dialog")).toHaveCount(0);
  await expect(
    page.getByRole("button", { name: "Edit Edited dinner" }),
  ).toBeVisible();
  expect(
    (await (await request.get(`${ledger.url}/expenses`)).json())[0]
      .amount_minor,
  ).toBe(1500);
});
test("expense deletion cancellation preserves record and confirmation removes it", async ({
  page,
  request,
  ledger,
}) => {
  await seed(request, ledger);
  await visit(page, ledger);
  page.once("dialog", (d) => d.dismiss());
  await page.getByRole("button", { name: "Delete Dinner" }).click();
  await expect(page.getByRole("button", { name: "Edit Dinner" })).toBeVisible();
  page.once("dialog", (d) => d.accept());
  await page.getByRole("button", { name: "Delete Dinner" }).click();
  await expect(page.getByRole("button", { name: "Edit Dinner" })).toHaveCount(
    0,
  );
  expect(await (await request.get(`${ledger.url}/expenses`)).json()).toEqual(
    [],
  );
});
test("balances display payer credit and debtor suggestions", async ({
  page,
  request,
  ledger,
}) => {
  await seed(request, ledger);
  await visit(page, ledger, "Balances");
  await expect(page.getByText("owes Alice").first()).toBeVisible();
  const balance = await (await request.get(`${ledger.url}/balances`)).json();
  expect(
    balance.members
      .map((m: any) => m.net_minor)
      .sort((a: number, b: number) => a - b),
  ).toEqual([-400, -400, 800]);
});
for (const amount of ["4.00", "1.00"]) {
  test(`${amount === "4.00" ? "full" : "partial"} settlement persists history and reduces balances`, async ({
    page,
    request,
    ledger,
  }) => {
    await seed(request, ledger);
    await visit(page, ledger, "Settlements");
    await page
      .getByRole("button", { name: "Record payment", exact: true })
      .first()
      .click();
    await page.getByLabel("Who paid?").selectOption({ label: "Bob" });
    await page.getByLabel("Who received?").selectOption({ label: "Alice" });
    await page.getByLabel("Payment amount (USD)").fill(amount);
    await page.getByLabel("Note (optional)").fill("Browser repayment");
    await page
      .getByRole("dialog")
      .getByRole("button", { name: "Record payment", exact: true })
      .click();
    await expect(page.getByRole("dialog")).toHaveCount(0);
    await page.reload();
    await expect(
      page.getByRole("cell", { name: "Browser repayment" }),
    ).toBeVisible();
    const balance = await (await request.get(`${ledger.url}/balances`)).json();
    expect(balance.members.find((m: any) => m.name === "Bob").net_minor).toBe(
      -400 + Number(amount) * 100,
    );
  });
}
test("analytics reflects real category and spending totals", async ({
  page,
  request,
  ledger,
}) => {
  await seed(request, ledger);
  await visit(page, ledger, "Analytics");
  await expect(page.locator(".stat").first()).toContainText("$12.00");
  const analytics = await (await request.get(`${ledger.url}/analytics`)).json();
  expect(analytics.total_minor).toBe(1200);
  expect(analytics.by_category).toEqual([
    { category: "Food & drinks", amount_minor: 1200 },
  ]);
});
test("search and category filtering combine without changing totals", async ({
  page,
  request,
  ledger,
}) => {
  await seed(request, ledger, "Dinner", "Food & drinks");
  await seed(request, ledger, "Bus ride", "Travel");
  await visit(page, ledger, "Expenses");
  const totalsBefore = await (
    await request.get(`${ledger.url}/analytics`)
  ).json();
  await page.getByLabel("Search expenses").fill("DIN");
  await expect(page.getByRole("button", { name: "Edit Dinner" })).toBeVisible();
  await expect(page.getByRole("button", { name: "Edit Bus ride" })).toHaveCount(
    0,
  );
  await page.getByLabel("Filter by category").selectOption("Travel");
  await expect(
    page.getByText("No matching expenses", { exact: true }),
  ).toBeVisible();
  await page.getByLabel("Search expenses").clear();
  await expect(
    page.getByRole("button", { name: "Edit Bus ride" }),
  ).toBeVisible();
  await expect(page.getByRole("button", { name: "Edit Dinner" })).toHaveCount(
    0,
  );
  await page.getByLabel("Filter by category").selectOption("");
  await expect(
    page.getByRole("button", { name: /^Edit (Dinner|Bus ride)$/ }),
  ).toHaveCount(2);
  expect(await (await request.get(`${ledger.url}/analytics`)).json()).toEqual(
    totalsBefore,
  );
  // Mutations must continue to work with an active filter, not only after reset.
  await page.getByLabel("Filter by category").selectOption("Travel");
  await page.getByRole("button", { name: "Edit Bus ride" }).click();
  await page.getByLabel("What was it for?").fill("Bus tickets");
  await page.getByRole("button", { name: "Save changes", exact: true }).click();
  await expect(page.getByRole("dialog")).toHaveCount(0);
  await expect(
    page.getByRole("button", { name: "Edit Bus tickets" }),
  ).toBeVisible();
  expect(
    (await (await request.get(`${ledger.url}/expenses`)).json()).some(
      (expense: { description: string }) =>
        expense.description === "Bus tickets",
    ),
  ).toBeTruthy();
  page.once("dialog", (dialog) => dialog.accept());
  await page.getByRole("button", { name: "Delete Bus tickets" }).click();
  await expect(
    page.getByText("No matching expenses", { exact: true }),
  ).toBeVisible();
  await page.getByLabel("Filter by category").selectOption("");
  await expect(page.getByRole("button", { name: "Edit Dinner" })).toBeVisible();
  const remaining = await (await request.get(`${ledger.url}/expenses`)).json();
  expect(remaining).toHaveLength(1);
  expect(remaining[0].description).toBe("Dinner");
});
test("form validation rejects invalid money and incorrect split totals", async ({
  page,
  ledger,
  request,
}) => {
  await visit(page, ledger);
  const dialog = await expenseDialog(page, "Invalid amount", "0");
  await dialog
    .getByRole("button", { name: "Add expense", exact: true })
    .click();
  await expect(dialog.getByRole("alert")).toContainText("positive amount");
  await dialog.getByLabel("Amount (USD)", { exact: true }).fill("12");
  await dialog
    .getByRole("button", { name: "Percentages", exact: true })
    .click();
  for (const name of ["Alice", "Bob", "Carol"])
    await dialog.getByLabel(`${name} percentage`).fill("10");
  await dialog
    .getByRole("button", { name: "Add expense", exact: true })
    .click();
  await expect(dialog.getByRole("alert")).toContainText("100%");
  expect(await (await request.get(`${ledger.url}/expenses`)).json()).toEqual(
    [],
  );
});
test("settlement validation rejects self-payment and excess repayment", async ({
  page,
  request,
  ledger,
}) => {
  await seed(request, ledger);
  await visit(page, ledger, "Settlements");
  await page
    .getByRole("button", { name: "Record payment", exact: true })
    .first()
    .click();
  await page.getByLabel("Who paid?").selectOption({ label: "Bob" });
  await page.getByLabel("Who received?").selectOption({ label: "Bob" });
  await page.getByLabel("Payment amount (USD)").fill("1");
  await page
    .getByRole("dialog")
    .getByRole("button", { name: "Record payment", exact: true })
    .click();
  await expect(page.getByRole("dialog").getByRole("alert")).toContainText(
    "different members",
  );
  await page.getByLabel("Who received?").selectOption({ label: "Alice" });
  await page.getByLabel("Payment amount (USD)").fill("5");
  await page
    .getByRole("dialog")
    .getByRole("button", { name: "Record payment", exact: true })
    .click();
  await expect(
    page.getByRole("dialog").getByRole("alert").first(),
  ).toBeVisible();
  expect(await (await request.get(`${ledger.url}/settlements`)).json()).toEqual(
    [],
  );
});
test("loading and recoverable HTTP error states", async ({ page, ledger }) => {
  let release: () => void = () => {};
  const gate = new Promise<void>((resolve) => (release = resolve));
  await page.route("**/api/groups", async (route) => {
    await gate;
    await route.fulfill({
      status: 503,
      contentType: "application/json",
      body: JSON.stringify({ detail: "QA unavailable" }),
    });
  });
  await page.goto("/");
  await expect(page.getByRole("status")).toContainText(
    "Getting your workspace ready",
  );
  release();
  await expect(page.getByRole("alert")).toContainText("QA unavailable");
  await page.unroute("**/api/groups");
  await page.getByRole("button", { name: "Try again", exact: true }).click();
  await expect(page.getByRole("alert")).toHaveCount(0);
  await expect(page.getByLabel("Active group")).toBeVisible();
});
test("responsive mobile navigation and keyboard dialog dismissal", async ({
  page,
  ledger,
  request,
}) => {
  // A valid maximum-length name must wrap rather than widen the page.
  const longName = "G".repeat(80);
  expect(
    (
      await request.put(ledger.url, {
        data: { name: longName, description: "Long group name regression" },
      })
    ).ok(),
  ).toBeTruthy();
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto(`/groups/${ledger.id}`);
  await expect(
    page.getByRole("button", { name: "Remove Alice" }),
  ).toBeVisible();
  expect(
    await page.evaluate(() => document.documentElement.scrollWidth),
  ).toBeLessThanOrEqual(390);
  await expect(
    page.getByRole("heading", { name: longName, exact: true }),
  ).toBeVisible();
  await page.getByRole("button", { name: "Open navigation" }).click();
  await page.getByRole("link", { name: "Expenses", exact: true }).click();
  await expect(
    page.getByRole("heading", { name: "Expenses", exact: true }),
  ).toBeVisible();
  expect(
    await page.evaluate(() => document.documentElement.scrollWidth),
  ).toBeLessThanOrEqual(390);
  await page.getByRole("button", { name: "Add expense", exact: true }).click();
  await expect(page.getByLabel("What was it for?")).toBeFocused();
  expect(
    await page.evaluate(() => document.documentElement.scrollWidth),
  ).toBeLessThanOrEqual(390);
  await page.keyboard.press("Escape");
  await expect(page.getByRole("dialog")).toHaveCount(0);
});
test("navigation preserves selected group across workspace routes (#67)", async ({
  page,
  ledger,
  request,
}) => {
  await seed(request, ledger);
  await visit(page, ledger);
  for (const path of [
    "Expenses",
    "Balances",
    "Settlements",
    "Analytics",
    "Overview",
  ]) {
    await page.getByRole("link", { name: path, exact: true }).click();
    await expect(page.getByLabel("Active group")).toHaveValue(ledger.id);
  }
  await page.reload();
  await page.getByLabel("Active group").selectOption(ledger.id);
  await page.getByRole("link", { name: "Expenses", exact: true }).click();
  await expect(page.getByRole("button", { name: "Edit Dinner" })).toBeVisible();
});

test("expense creation saves selected payer, participants, category and date (#50)", async ({
  page,
  request,
  ledger,
}) => {
  await visit(page, ledger);
  const dialog = await expenseDialog(page, "Museum tickets", "9.00");
  await dialog.getByLabel("Paid by").selectOption({ label: "Bob" });
  await dialog
    .getByLabel("Category")
    .selectOption("Entertainment");
  await dialog.getByLabel("Date", { exact: true }).fill("2026-10-18");
  await dialog
    .locator(".split-person")
    .filter({ hasText: "Carol" })
    .getByRole("checkbox")
    .uncheck();
  await dialog
    .getByRole("button", { name: "Add expense", exact: true })
    .click();
  await expect(dialog).toHaveCount(0);
  await expect(
    page.getByRole("button", { name: "Edit Museum tickets" }),
  ).toBeVisible();
  const expenses = await (await request.get(`${ledger.url}/expenses`)).json();
  expect(expenses).toHaveLength(1);
  expect(expenses[0]).toMatchObject({
    description: "Museum tickets",
    amount_minor: 900,
    payer_id: ledger.members[1].id,
    category: "Entertainment",
    date: "2026-10-18",
  });
  expect(
    expenses[0].shares
      .map((share: { member_id: string }) => share.member_id)
      .sort(),
  ).toEqual([ledger.members[0].id, ledger.members[1].id].sort());
});

test("data persistence restores saved expenses and settlements in a reopened page (#68)", async ({
  page,
  request,
  ledger,
  context,
}) => {
  await seed(request, ledger);
  await visit(page, ledger, "Settlements");
  await page
    .getByRole("button", { name: "Record payment", exact: true })
    .first()
    .click();
  await page.getByLabel("Who paid?").selectOption({ label: "Bob" });
  await page.getByLabel("Who received?").selectOption({ label: "Alice" });
  await page.getByLabel("Payment amount (USD)").fill("1.00");
  await page.getByLabel("Note (optional)").fill("Persisted repayment");
  await page
    .getByRole("dialog")
    .getByRole("button", { name: "Record payment", exact: true })
    .click();
  await expect(page.getByRole("dialog")).toHaveCount(0);
  const reopened = await context.newPage();
  try {
    await visit(reopened, ledger, "Expenses");
    await expect(
      reopened.getByRole("button", { name: "Edit Dinner" }),
    ).toBeVisible();
    await reopened.reload();
    await expect(
      reopened.getByRole("button", { name: "Edit Dinner" }),
    ).toBeVisible();
    await reopened
      .getByRole("link", { name: "Settlements", exact: true })
      .click();
    await expect(
      reopened.getByRole("cell", { name: "Persisted repayment" }),
    ).toBeVisible();
    const balances = await (await request.get(`${ledger.url}/balances`)).json();
    expect(
      balances.members.find((member: { name: string }) => member.name === "Bob")
        .net_minor,
    ).toBe(-300);
  } finally {
    await reopened.close();
  }
});
