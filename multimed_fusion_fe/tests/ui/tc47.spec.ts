import { test } from "@playwright/test";

import { runWorkbookUiCase } from "./workbook-ui";


test("tc47", async ({ page, browser, request, context, baseURL }) => {
  await runWorkbookUiCase(47, { page, browser, request, context, baseURL });
});
