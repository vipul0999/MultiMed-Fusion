import { test } from "@playwright/test";

import { runWorkbookUiCase } from "./workbook-ui";


test("tc32", async ({ page, browser, request, context, baseURL }) => {
  await runWorkbookUiCase(32, { page, browser, request, context, baseURL });
});
