import { test } from "@playwright/test";

import { runWorkbookUiCase } from "./workbook-ui";


test("tc20", async ({ page, browser, request, context, baseURL }) => {
  await runWorkbookUiCase(20, { page, browser, request, context, baseURL });
});
