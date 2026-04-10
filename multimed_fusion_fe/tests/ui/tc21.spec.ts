import { test } from "@playwright/test";

import { runWorkbookUiCase } from "./workbook-ui";


test("tc21", async ({ page, browser, request, context, baseURL }) => {
  await runWorkbookUiCase(21, { page, browser, request, context, baseURL });
});
