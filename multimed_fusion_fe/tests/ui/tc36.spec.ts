import { test } from "@playwright/test";

import { runWorkbookUiCase } from "./workbook-ui";


test("tc36", async ({ page, browser, request, context, baseURL }) => {
  await runWorkbookUiCase(36, { page, browser, request, context, baseURL });
});
