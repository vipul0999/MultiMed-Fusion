import { test } from "@playwright/test";

import { runWorkbookUiCase } from "./workbook-ui";


test("tc45", async ({ page, browser, request, context, baseURL }) => {
  await runWorkbookUiCase(45, { page, browser, request, context, baseURL });
});
