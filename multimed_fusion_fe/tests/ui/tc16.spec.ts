import { test } from "@playwright/test";

import { runWorkbookUiCase } from "./workbook-ui";


test("tc16", async ({ page, browser, request, context, baseURL }) => {
  await runWorkbookUiCase(16, { page, browser, request, context, baseURL });
});
