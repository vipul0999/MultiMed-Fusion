import { test } from "@playwright/test";

import { runWorkbookUiCase } from "./workbook-ui";


test("tc24", async ({ page, browser, request, context, baseURL }) => {
  await runWorkbookUiCase(24, { page, browser, request, context, baseURL });
});
